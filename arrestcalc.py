import json
import time
import sys
from string import punctuation
import requests

API_BASE_URL = "https://api.torn.com/"
API_ARRESTS_URL = ["user/?selections=log&log=8165&from=", "&to=", "&key="]


def api_key_input():
    """Request API Key from user using input. Performs basic checks to validate key.
    Returns a string containing the API key."""

    print("An API key with -FULL- API access is required to pull logs.")
    key_input = input("Enter Key: ")
    key_input.strip()

    if len(key_input) == 16:
        for char in punctuation:
            if char in key_input:
                print("Invalid Key. Exiting..")
                sys.exit()
        return key_input
    else:
        print("Invalid Key. Exiting..")
        sys.exit()


def choose_timeframe():
    print("Time frame options:\n1 - 7 days\n2 - 30 days\n3 - 1 Year\n4 - All Time")
    selection = int(input("Option #: "))
    if selection > 0 and selection < 5:
        current_time = int(time.time())
        if selection == 1:
            return current_time - 604800
        elif selection == 2:
            return current_time - 2592000
        elif selection == 3:
            return current_time - 31536000
        elif selection == 4:
            return 0
    else:
        print("Invalid option. Exiting..")
        sys.exit()


def request_multipage_data(api_key):
    """Torn's API limits the number of rows in the response to 100.
    Performs multiple requests, changing the timestamp, then returns a single object.
    """

    multipage_data = dict()
    first_run = True
    from_time = choose_timeframe()
    time_marker = int(time.time())
    download_counter = 0
    mode_url = API_ARRESTS_URL
    mode_descriptor = "log"

    print("Downloaded " + str(download_counter) + " arrest logs..", end="\r")

    while True:
        response = requests.get(
            API_BASE_URL
            + mode_url[0]
            + str(from_time)
            + mode_url[1]
            + str(time_marker)
            + mode_url[2]
            + api_key
        )  # Make request to the API
        # print(response.url)
        data = json.loads(response.content)
        event_counter = 0
        if data[mode_descriptor] is not None:  # Check that the API returned data
            if first_run:  # First run downloads all rows without extra checks
                multipage_data = data
                event_counter = len(multipage_data[mode_descriptor]) - 1
                first_run = False
            else:
                for key in iter(
                    data[mode_descriptor]
                ):  # Iterate through keys and check them against our data to prevent duplicates
                    if key not in multipage_data[mode_descriptor]:
                        multipage_data[mode_descriptor].update(
                            {key: data[mode_descriptor][key]}
                        )
                        event_counter += 1

            timestamp_split = response.text.split(
                '"timestamp":'
            )  # Get the last row on the page and set the new time marker to the timestamp
            time_marker = int(timestamp_split[len(timestamp_split) - 1].split(",")[0])
        else:
            break

        download_counter += event_counter
        print(
            "Downloaded " + str(download_counter) + " arrest logs..",
            end="\r",
        )
        time.sleep(30)  # Sleep to prevent API from sending the same result back
    print("Finished. Downloaded " + str(download_counter + 1) + " logs!")

    return multipage_data


api_key = api_key_input()
arrests = request_multipage_data(api_key)

total = 0
for arrest in arrests["log"]:
    total += int(arrests["log"][arrest]["data"]["wanted_reward"])

# Old file loading of manually copied logs
# with open("arrests.txt", "r") as file:
#     for line in file:
#         index0 = line.find("wanted_reward")
#         index1 = line.find("for their $")
#         index2 = line.find(" wanted reward")

#         if alt_mode:
#             try:
#                 arrests.append(line.split()[4].replace("$", "").replace(",", "").strip())
#             except IndexError:
#                 pass

#         elif index1 != -1:
#             arrests.append(line[index1 + 11 : index2].replace(",", "").strip())

#         if index0 != -1:
#             alt_mode = True

print("")
print("Arrests Made: " + str(len(arrests["log"])))
print("Average Reward: {:,.0f}".format(total / len(arrests["log"])))
print("Total Reward: {:,}".format(total))
print("Energy spent: " + str(len(arrests["log"]) * 25))
print("Reward per energy: " + "{:,.0f}".format(total / (len(arrests["log"]) * 25)))
print(
    "Reward per 150 energy: "
    + "{:,.0f}".format(total / (len(arrests["log"]) * 25) * 150)
)

arrests = []

with open("arrests.txt", "r") as file:
    for line in file:
        index1 = line.find("for their $")
        index2 = line.find(" wanted reward")
        if index1 != -1:
            arrests.append(line[index1 + 11 : index2].replace(",", "").strip())

total = 0
for arrest in arrests:
    total += int(arrest)

print("Arrests Made: " + str(len(arrests)))
print("Average Reward: {:,.0f}".format(total / len(arrests)))
print("Total Reward: {:,}".format(total))
print("Energy spent: " + str(len(arrests) * 25))
print("$ per energy: " + "{:,.0f}".format(total / (len(arrests) * 25)))
print("$ per 150 energy: " + "{:,.0f}".format(total / (len(arrests) * 25) * 150))

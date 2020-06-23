import requests
import json
import os
from sys import exit
from operator import itemgetter

#Flight Times
argentinaTime = 167
canadaTime = 41
caymanTime = 35
chinaTime = 242
hawaiiTime = 134
japanTime = 225
mexicoTime = 26
safricaTime = 297
switzerlandTime = 175
uaeTime = 271
ukTime = 159

# Flowers
# item = ['Name', itemNumber, cost, BazaarPrice, Profit(BazaarPrice-cost), flightMinutes, perMinuteProfit]
dahlia = ['Dahlia-MEX', 260, 300, None, None, mexicoTime, None]
crocus = ['Crocus-CAN', 263, 600, None, None, canadaTime, None]
bananaOrchid = ["Banana Orchid-CAY", 617, 4000, None, None, caymanTime, None]
orchid = ["Orchid-HAW", 264, 700, None, None, hawaiiTime, None]
edelweiss = ["Edelweiss-SWI", 272, 900, None, None, switzerlandTime, None]
ceibo = ["Ceibo-ARG", 271, 500, None, None, argentinaTime, None]
heather = ["Heather-UK", 267, 5000, None, None, ukTime, None]
cherryBlossom = ["Cherry Blossom-JAP", 277, 500, None, None, japanTime, None]
africanViolet = ["African Violet-SAF", 282, 2000, None, None, safricaTime, None]
peony = ["Peony-CHI", 276, 5000, None, None, chinaTime, None]
tribulus = ["Tribulus-UAE", 385, 6000, None, None, uaeTime, None]

# Plushies
# item = ['Name', itemNumber, cost, BazaarPrice, Profit(BazaarPrice-cost), flightMinutes, perMinuteProfit]
jaguar = ['Jaguar-MEX', 258, 10000, None, None, mexicoTime, None]
wolverine = ['Wolverine-CAN', 261, 30, None, None, canadaTime, None]
stingray = ["Stingray-CAY", 618, 400, None, None, caymanTime, None]
chamois = ["Chamois-SWI", 273, 400, None, None, switzerlandTime, None]
monkey = ["Monkey-ARG", 269, 400, None, None, argentinaTime, None]
nessie = ["Nessie-UK", 266, 200, None, None, ukTime, None]
redfox = ["Red Fox-UK", 268, 1000, None, None, ukTime, None]
lion = ["Lion-SAF", 281, 400, None, None, safricaTime, None]
panda = ["Panda-CHI", 274, 400, None, None, chinaTime, None]
camel = ["Camel-UAE", 384, 14000, None, None, uaeTime, None]

flowers = [dahlia, crocus, bananaOrchid, orchid, edelweiss, ceibo, heather,
           cherryBlossom, africanViolet, peony, tribulus]

plushies = [jaguar, wolverine, stingray, chamois, monkey, nessie, redfox, lion, panda, camel]

def getSettings():
    apiKey = "NONE"
    capacity = 0
    airstrip = False
    
    if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ttpSettings.txt')):
        try:
            settingsFile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ttpSettings.txt'))
            settingsContent = settingsFile.readlines()
            settingsFile.close()
        except Exception as err:
            print("Error reading file..")
            print(str(err))
            input()

        apiKey = settingsContent[0].split('=')[1].strip()
        capacity = int(settingsContent[1].split('=')[1].strip())
        airstrip = settingsContent[2].split('=')[1].strip()

        if airstrip == "true" or airstrip == "True":
            airstrip = True
        if airstrip == "false" or airstrip == "False":
            airstrip = False
    else:
        print("No settings file detected..")
        print("Please enter your Torn API key: ")
        apiKey = input()
        print("How many items can you carry?")
        capacity = int(input())
        print("Do you own a PI airstrip? y/n")
        airstripYN = input()
        
        if airstripYN == "y" or airstripYN == "Y" or airstripYN == "yes" or airstripYN == "Yes" or airstripYN == "YES":
            airstrip = True

        print("API Key: " + str(apiKey))
        print("Capacity: " + str(capacity))
        print("Airstrip: " + str(airstrip))
        print("Creating settings file..")
        try:
            settingsFile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ttpSettings.txt'), 'w')
            settingsFile.write('apiKey = ' + apiKey + "\n")
            settingsFile.write('capacity = ' + str(capacity) + "\n")
            settingsFile.write('airstrip = ' + str(airstrip))
            settingsFile.close()
            print("Any of these settings can be changed in the 'ttpSettings.txt' file.")
        except Exception as err:
            print("Error creating file..")
            print(str(err))
            input()
            exit()

    return apiKey, capacity, airstrip


def retrieveValues(targetList, settings):
    for x in targetList:
        print('Requesting data for item: ' + str(x[1]) + ' (' + str(x[0]) + ')' + '..')
        try:
            res = requests.get("http://api.torn.com/market/" + str(x[1]) + 
                "?selections=&key=" + settings[0])
            res.raise_for_status()
        except Exception as err:
            print("Connection to Torn failed, please try again..")
            input()
            exit()

        result = json.loads(res.text)
        try:
            x[3] = int(result['bazaar'][0]['cost'])
        except KeyError:
            print("API Key is invalid!\nPlease edit the settings file with a valid key.")
            print(result)
            print("Press any key to exit..")
            input()
            exit()

def calcProfits(targetList):
    for x in targetList:
        x[4] = x[3] - x[2]
        x[6] = x[4]/(x[5]*2)

settings = getSettings()

retrieveValues(flowers, settings)
retrieveValues(plushies, settings)

if settings[2]:
    for f in flowers:
        f[5] = int(round(f[5] * 0.7))
    for p in plushies:
        p[5] = int(round(p[5] * 0.7))

calcProfits(flowers)
calcProfits(plushies)

flowers.sort(key=itemgetter(6), reverse=True)
plushies.sort(key=itemgetter(6), reverse=True)

print()
print('---Cap: ' + str(settings[1]) + '-------------FLOWERS-----------------------')
print('{:<18s}{:^12s}{:>12s}{:>9s}'.format('Flower', 'Profit/Min', 'TotalProfit', 'TripTime'))
print('-' * 53)
for x in flowers:
    print('{:<18s}{:>9s}{:>14s}{:>10s}'.format(x[0],"${:,.0f}".format(x[6]*settings[1]), "${:,.0f}".format(x[4]*settings[1]), str(x[5]*2//60) + "hr " + str(x[5]*2%60) +"mn"))

print('')

print('---Cap: ' + str(settings[1]) + '-------------PLUSHIE-----------------------')
print('{:<18s}{:^12s}{:>12s}{:>9s}'.format('Plushie', 'Profit/Min', 'TotalProfit', 'TripTime'))
print('-' * 53)

for x in plushies:
    print('{:<18s}{:>9s}{:>14s}{:>10s}'.format(x[0],"${:,.0f}".format(x[6]*settings[1]), "${:,.0f}".format(x[4]*settings[1]), str(x[5]*2//60) + "hr " + str(x[5]*2%60) +"mn"))
	
input()

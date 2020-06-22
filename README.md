# TornScripts
Miscellaneous scripts for Torn.com

### Torn Personal Stats Aide
(Userscript) Displays the graph data on the personal stats page in text form for quick reading.

![Text is added to the title bar above the graph](https://raw.githubusercontent.com/SixPraxis/TornScripts/master/images/aideComparison.png)
__________
### Torn Arrest Helper
(Userscript) Adds a filter button to the hospital page that will only show players that are hospitalized due to a safe crime. These players are more likely to have been out of jail for extended amounts of time, therefore being more likely to meet the arrest threshold. The script also adds a button to quickly go to the player's Times Jailed graph, which lets you see the last time they were arrested.

![Filter button up top, jailed graph button next to the reason](https://raw.githubusercontent.com/SixPraxis/TornScripts/master/images/filterExample.png)
__________
### Torn Travel Profit
Dependencies: requests

(Python) Downloads the lowest current bazaar price for flowers and plushies then does the math to provide the profit per minute, total profit, and trip time of each item. The items are sorted by profit per minute. This does require your Torn API key to make the bazaar price requests. There are options for item capacity and to decrease flight times if you have an airstrip. The requests package available on pip is required.

![Torn Travel Profit output](https://raw.github.com/SixPraxis/TornScripts/master/images/travelProfit.png)
__________

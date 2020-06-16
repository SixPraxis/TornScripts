// ==UserScript==
// @name         Torn Personal Stats Aide
// @version      1.0.1
// @description  Displays total of a stat within the selected time frame
// @author       HotSoup [860380]
// @match        https://www.torn.com/personalstats.php*
// @updateURL    https://raw.githubusercontent.com/SixPraxis/TornScripts/master/TornStatsAide.js
// @downloadURL  https://raw.githubusercontent.com/SixPraxis/TornScripts/master/TornStatsAide.js
// ==/UserScript==
(function() {
    'use strict';

    var debug = false;

    function debugLog(logMessage){
    	if (debug){
    		console.log("TPSA: " + logMessage);
    	}
    }

    var observer = new MutationObserver(checkForTable);
    var observer2 = new MutationObserver(chartChange);
    var observer3 = new MutationObserver(chartChange);
    const config = { attributes: true, childList: true, subtree: true};
    var timeSetting = "";
    var statSetting = "";
    var playerId = "";

    function calcDayDiff(date1, date2){
    	debugLog("FUNCTION - calcDayDiff");
    	date1 = date1.split(" ");
    	date2 = date2.split(" ");
    	let months = ["Jan", "Feb", "March", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    	
    	date1[1] = date1[1].replace(/[\.,]/g, "");
    	date2[1] = date2[1].replace(/[\.,]/g, "");
    	
    	let dateObj1 = new Date();
    	let dateObj2 = new Date();
    	dateObj1.setMonth(months.indexOf(date1[0]));
    	dateObj1.setDate(date1[1]);
    	dateObj1.setFullYear(date1[2]);
    	dateObj2.setMonth(months.indexOf(date2[0]));
    	dateObj2.setDate(date2[1]);
    	dateObj2.setFullYear(date2[2]);

    	let dayDiff = (dateObj1.getTime() - dateObj2.getTime())/86400000;
    	let dayDiffString = "";
    	if (dayDiff != 1){
    		dayDiffString = dayDiff + " days";
    	} else {
    		dayDiffString = dayDiff + " day";
    	}
    	return dayDiffString;
    }

    function calcDiff(){
    	debugLog("FUNCTION - calcDiff");
    	timeSetting = document.getElementsByClassName("toggler")[0].innerHTML;
    	statSetting = document.getElementsByClassName("toggler")[1].innerHTML;
    	playerId = document.getElementsByClassName("user___1Fh_v")[0].innerHTML.match(/(?<=\[).+?(?=\])/);

    	let table = document.getElementsByTagName("tbody")[0];
    	let date1 = table.getElementsByTagName("tr")[0].getElementsByTagName("td")[0].innerHTML;
    	let date2 = "";
    	let value1 = parseInt(table.getElementsByTagName("tr")[0].getElementsByTagName("td")[1].innerHTML.replace(/[\.,]/g, ""));
    	let value2 = -1;

    	let tableRows = table.getElementsByTagName("tr");
    	let value3 = tableRows[tableRows.length-1].getElementsByTagName("td")[1].innerHTML.replace(/[\.,]/g, "");

    	for (let i = 0; i < tableRows.length; i++){
    		let tempValue = tableRows[i].getElementsByTagName("td")[1].innerHTML.replace(/[\.,]/g, "");
    		if (tempValue != value1 && tableRows.length > 0){
    			date2 = tableRows[i-1].getElementsByTagName("td")[0].innerHTML;
    			value2 = tempValue;
    			break;
    		}
    	}

     	let titleDiv = document.getElementsByClassName("title___hNtZa")[1];
     	let timeFrame = document.getElementsByClassName("toggler")[0].innerHTML;

    	if (value2 == -1){
    		titleDiv.innerHTML = statSetting + " | " + "0 occurences in the last " + timeFrame;
    	} else {
    		titleDiv.innerHTML = statSetting + " in " + timeFrame + ": " + (value1 - value3) + " | " +"Most Recent: " + date2 + " - " + calcDayDiff(date1, date2) + " ago";
    	}
    }

    function observeDiv(){
    	debugLog("FUNCTION - observeDiv");
    	let reactDiv = document.getElementById("react-root");
    	observer.observe(reactDiv, config);
    	let chartDiv = document.getElementsByClassName("dropDowns___1DlpB")[0];
    	observer2.observe(chartDiv, config);
    	let userDiv = document.getElementsByClassName("users___qNm7E")[0];
    	observer3.observe(userDiv, config);
    }

    function checkForTable(){
    	debugLog("FUNCTION - checkForTable");
    	let table = document.getElementsByTagName("tbody");
    	if (table.length > 0){
    		observer.disconnect();
    		calcDiff();
    	}
    }

    async function chartChange(){
    	debugLog("FUNCTION - chartChange");
    	let togglers = document.getElementsByClassName("toggler");
    	if(timeSetting != togglers[0].innerHTML || statSetting != togglers[1].innerHTML){
    		await new Promise(r => setTimeout(r, 500));
    		calcDiff();
    	} else if (document.getElementsByClassName("user___1Fh_v")[0].innerHTML.match(/(?<=\[).+?(?=\])/) != playerId){
    		await new Promise(r => setTimeout(r, 500));
    		calcDiff();
    	}
    }

   	window.onload = observeDiv;

})();
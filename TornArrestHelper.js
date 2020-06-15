// ==UserScript==
// @name         Torn Arrest Helper
// @version      1.0
// @description  Helps find likely arrest targets from the hospital page
// @author       SixPraxis - [860380]
// @match        https://www.torn.com/hospitalview.php*
// @match        https://www.torn.com/personalstats.php*
// ==/UserScript==

(function() {
    'use strict';

    var filterBtn = document.createElement("button");
    filterBtn.innerHTML = "Arrest Helper Filter";
    filterBtn.setAttribute("class",  "city t-clear h c-pointer  m-icon line-h24 right last");
    filterBtn.onclick = filterUsers;

    var observer = new MutationObserver(checkForTable);
    const config = { attributes: false, childList: true, subtree: true};

    function addButton(){
    	var linksTopDiv = document.getElementById("top-page-links-list");
    	var linksFooterDiv = linksTopDiv.getElementsByClassName("links-footer")[0];
    	linksTopDiv.insertBefore(filterBtn, linksFooterDiv);
    }

    function filterUsers(){
        let userTable = document.getElementsByClassName("user-info-list-wrap")[0];
        let userRows = userTable.getElementsByClassName("reason");
        var badRows = [];

        for (let i = 0; i < userRows.length; i++ ){
        	if (userRows[i].innerHTML.includes("arson") || userRows[i].innerHTML.includes("Mauled by a guard dog") || userRows[i].innerHTML.includes("hitman mission")){
        		let nameAnchor = userRows[i].parentElement.parentElement.getElementsByClassName("user name")[0];
        		let userID = nameAnchor.getAttribute("href").slice(18);
        		let graphURL = "/personalstats.php?ID=" + userID + "&stats=jailed&from=1%20month";
        		
        		let jailedBtn = document.createElement("button");
        		jailedBtn.innerHTML = "Jailed Graph";
        		
        		let jailedAnchor = document.createElement("a");
        		jailedAnchor.appendChild(jailedBtn);
        		jailedAnchor.href = graphURL;
        		jailedAnchor.setAttribute("style", "margin-left:10px");
        		
        		userRows[i].appendChild(jailedAnchor);
        	} else {
        		badRows.push(userRows[i].closest("li"));
        	}
        }
        badRows.forEach(function(item, index, array){
        	item.remove();
        })
    }

    function calcDiff(table){
    	let value1 = parseInt(table.getElementsByTagName("tr")[0].getElementsByTagName("td")[1].innerHTML.replace(/[\.,]/, ""));
    	let value2 = parseInt(table.getElementsByTagName("tr")[15].getElementsByTagName("td")[1].innerHTML.replace(/[\.,]/, ""));
    	let value3 = parseInt(table.getElementsByTagName("tr")[30].getElementsByTagName("td")[1].innerHTML.replace(/[\.,]/, ""));
    	let titleDiv = document.getElementsByClassName("title___hNtZa")[1];
    	let timeFrame = document.getElementsByClassName("toggler")[0].innerHTML;
    	titleDiv.innerHTML = titleDiv.innerHTML + " | " + (value1-value3) + " in the last " + timeFrame + " | " + (value1-value2) + " in half that time";
    }

    function observeDiv(){
    	let reactDiv = document.getElementById("react-root");
    	observer.observe(reactDiv, config);
    }

    function checkForTable(){
    	let table = document.getElementsByTagName("tbody");
    	if (table.length > 0){
    		observer.disconnect();
    		calcDiff(table[0]);
    	}
    }

    if (document.URL.includes("hospitalview")){
    	window.onload = addButton;
    }

    if (document.URL.includes("stats=jailed")){
    	window.onload = observeDiv;
    }
})();
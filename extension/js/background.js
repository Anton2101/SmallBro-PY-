var url, socket = new WebSocket("ws://127.0.0.1:8080");
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
	if(changeInfo.url !== undefined) {
 		socket.send(changeInfo.url);
	}
});

chrome.tabs.onActivated.addListener(function(activeInfo) {
  chrome.tabs.get(activeInfo.tabId, function(tab){
  	if(tab.url !== undefined) {
    	socket.send(tab.url);
  	}
  });
});

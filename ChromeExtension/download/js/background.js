/**
 在后台运行的js
 */

var limit_tabs_count = 100;  // 限制打开tab页的个数
var global_switch = true;
var time = 50;  	       // 创建tab页的时间间隔
var tab_count = 0;         // 当前打开tab页的个数

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (typeof message == "string") {
        createTab(message);
        sendResponse('response');
    }
});

// 创建chrometabs
function createTab(url) {

    (function (url) {
        setTimeout(function () {
            main(url);
        }, time);
    })(url);

    function main(url) {
        if (!global_switch) {
            return;
        }
        chrome.tabs.create({
            //windowId: wId,
            index: 100,
            url: url,
            active: false,
            pinned: false
            //openerTabId: tId
        }, function (tab) {
            tab_count++;
            var len = tab_count;
            if (len > limit_tabs_count) {
                global_switch = false;
                var txt = "操作完成，打开" + len + "个页面";
                notice(txt);
            }
        });
    }
}

// 桌面提醒
function notice(txt) {
    var notification = new Notification("我的消息", {
            body: txt,
            //iconUrl : 'https://www.baidu.com/img/bdlogo.png',
            icon: 'images/icon.png',
            tag: {}
        }
    );
    notification.onclose = function () {
        console.log("close");
    }
}

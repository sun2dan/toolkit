var mustHave = ["陕西师范大学", "陕师大"];  // 必须出现的学校名称，必须有一个
var keywords = ["试题", "作业", "资料", "课件", "整理", "年", "期末", "考试"];  			// 必须出现的文件类型，必须有一个
var notContains = ["考研", "论文"];  // 不能出现的文字
var time = 50000;


// 入口
filter();

/*
	1、判断当前页是否可用
	2、判断推荐是否可用
*/
function filter(){
	validateCurrentDoc();
	validateCurrentLink();
}

// 验证当前文档是否可以下载
function validateCurrentDoc(){
	var hs = document.getElementsByClassName("with-top-banner");
	if(hs.length > 0){
		var spans = hs[0].getElementsByTagName("span");
		if(spans.length > 0){
			var title = spans[0].innerHTML;
			
			if(filterUsefulTitle(title)){
				download();
			}
		}
	}
}

// 验证当前页的推荐是否可以打开下载
function validateCurrentLink(){

	var arr = document.getElementsByTagName("ul");
	var links = [];

	for (var i=0; i<arr.length ; i++ ){
		var ul = arr[i];
		var attr = ul.getAttribute("alog-group");

		// 相关文档推荐
		if(attr == "view.relatedoc.doc"){
			links.push(ul.getElementsByTagName("a"));
		}else if(attr == "view.otherlikedoc.doc"){
			links.push(ul.getElementsByTagName("a"));
		}
	}
	//var links = Array.prototype.concat(links1, links2);
	for (var i = links.length - 1; i >= 0; i--) {
		filterUsefulLink(links[i]);
	};
}

// 过滤出有用的链接
function filterUsefulLink(links){
	for (var i = links.length - 1; i >= 0; i--) {
		var a = links[i];
		//console.info(a.title);
		if(filterUsefulTitle(a.title)){
			// 如果可用，打开新标签页
			//console.info(a.href);
			createTab(a.href);
		}
	}
}

// 判断标题的可用性
function filterUsefulTitle(title){
	if(!title){
		return false;
	}

	return validate(mustHave) && validate(keywords) && !validate(notContains);

	function validate(arr){
		var b = false;
		for (var i=0; i < arr.length; i++ ){
			if(title.indexOf(arr[i]) > -1){
				b = true;	
				break;
			}
		}
		return b;
	}
}

// 触发下载按钮
function download(){
	window.addEventListener("load", function(){
		main();
	});

	// 下载函数
	function main(){
		var btns = document.getElementsByClassName("reader-download");
		if(btns.length < 0){
			return;
		}

		for (var i = btns.length - 1; i >= 0; i--) {
			var b = btns[i];
			if(b.getAttribute("data-toolsbar-log") == "download"){
				b.click();
				setTimeout(function(){
					hasDownload();
					identifyImage();
				}, time);
				break;
			}
		};
	}
}

// 是否已经下载过了 -- 通过验证码窗口来判断
function hasDownload(){
	var a = "vcode-ipt";

	var html = document.getElementsByTagName("body")[0].innerHTML;

	if(html.indexOf('你已转存过此文档至') > -1){
		window.close();

	}

	return true;

	// 获取验证码窗口：一般的都有两个，下载过的只有一个
	var vipts = document.getElementsByClassName(a);
	if(vipts.length == 1){
		window.close();
	}else if(vipts.length == 2){

	}

}

// 创建chrometabs
function createTab(url){
	chrome.runtime.sendMessage(url, function(response){
	});
}


chrome.contextMenus.create({
  type: 'normal',
  title: '打开JSON Editor',
  id: "1",
  onclick: function(){
    var id =  chrome.i18n.getMessage("@@extension_id");
    var path ='chrome-extension://'+id+'/index.html';
    window.open(path);
  }
});

var s = document.createElement('script');
s.src = chrome.extension.getURL('wgxpath.install.js');
alert(s.src);
s.onload = function() { 
    wgxpath.install();
    this.parentNode.removeChild(this);
};
(document.head||document.documentElement).appendChild(s);

function copyText(browserinfo_string) {
    var range = document.createRange();
    range.selectNode(browserinfo_string); 
    window.getSelection().addRange(range); 
    document.execCommand("copy");
    window.getSelection().removeAllRanges();
    }

function copyURL() {
    navigator.clipboard.writeText(window.location.href);
}
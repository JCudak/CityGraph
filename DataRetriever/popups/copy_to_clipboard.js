function copyToClipboard(info) {
    var copyText = document.createElement('textarea');
    copyText.value = info;
    document.body.appendChild(copyText);
    copyText.select();
    document.execCommand('copy');
    document.body.removeChild(copyText);
    var message = document.getElementById('copy-message');
    message.style.display = 'block';
}

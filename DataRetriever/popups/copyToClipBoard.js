function copyToClipboard(node_id) {
    const copyText = document.createElement('textarea');
    copyText.value = node_id;
    document.body.appendChild(copyText);
    copyText.select();
    document.execCommand('copy');
    document.body.removeChild(copyText);
    const message = document.getElementById('copy-message-' + node_id);
    message.style.display = 'block';
}

function openPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var win = window.open(triggeringLink.href, name, 'height=400,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}
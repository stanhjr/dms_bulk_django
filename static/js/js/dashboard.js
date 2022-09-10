window.onload = () => {
    if ($('a[href="#popup-notification"]').length) {
        document.querySelector('a[href="#popup-notification"]').click()
    }
}

$('#notification-accept').click(() => $.magnificPopup.close())
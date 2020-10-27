'use strict'

var notifier = new Notifier();

$(() => {
    makeResizableDiv('.setting-panel');
    makeResizableDiv('.info-panel');

    $(".node").hover(
        function () {
            $(".info-panel > .information > img").attr('src', CONFIG.IMAGES[$(this).attr('id')]);
        },
        function () {
            $(".info-panel > .information > img").attr('src', '');
        });

    infoMessages();
});

function showImage(id) {

}

function infoMessages() {
    let allInfoMessages = messages.info.uses.recursiveValues();
    setInterval(() => {
        notifier.info(allInfoMessages[
            Math.floor(Math.random() * allInfoMessages.length)
        ]);
    }, CONFIG.SHOW_MESSAGES_INTERVAL);
}
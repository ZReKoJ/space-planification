'use strict'

var notifier = new Notifier();

$(() => {
    makeResizableDiv('.setting-panel');
    makeResizableDiv('.info-panel');

    $(".info-panel > .information > img").hide();

    $(".node").hover(
        function () {
            $(".info-panel > .information > img").attr('src', CONFIG.IMAGES[$(this).attr('id')]).show();
        },
        function () {
            $(".info-panel > .information > img").attr('src', '').hide();
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
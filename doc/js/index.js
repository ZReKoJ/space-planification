'use strict'

var notifier = new Notifier();

$(() => {
    makeResizableDiv('.setting-panel');
    makeResizableDiv('.info-panel');

    infoMessages();
});

function infoMessages() {
    let allInfoMessages = messages.info.uses.recursiveValues();
    setInterval(() => {
        notifier.info(allInfoMessages[
            Math.floor(Math.random() * allInfoMessages.length)
        ]);
    }, CONFIG.SHOW_MESSAGES_INTERVAL);
}
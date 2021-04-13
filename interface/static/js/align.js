// Keeping track of which line is highlighted.
let highlighted = null;
// Making this a function so that this crude styling can be changed later. :-)
function highlight(text) {
    const active_text_classes = [
        'border', 'border-warning', 'rounded',
        'bg-light',
        'lead',
        'p-1', 'mx-1'
    ];
    if (highlighted) {
        for (const active_class of active_text_classes) {
            highlighted.classList.remove(active_class);
        }
    }
    for (const active_class of active_text_classes) {
        text.classList.add(active_class);
    }
    text.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
    highlighted = text;
}
// The "main" of this script.
{
    // Set up handlers for click on text
    for (const word of document.getElementsByClassName('align-text')) {
        word.addEventListener('click', (e) => {
            document.getElementById("audio").currentTime = parseFloat(word.dataset.begin);
        });
    }
    // Set up handlers for time change in audio.
    // Note: This event can fire several times a second, so keep this handler light.
    // https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/timeupdate_event
    document.getElementById('audio').ontimeupdate = (event) => {
        // // Don't run this more than every 100 ms.
        // if (new Date() - lastRan < 100) return;
        // lastRan = new Date();
        const whatTime = parseFloat(document.getElementById("audio").currentTime.toFixed(3));
        // Find the right text. For now, O(n) loop is fine; we have at most a few hundred verses in a sarga.
        let seenLine = null;
        for (const text of document.getElementsByClassName('align-text')) {
            const thisTextStart = parseFloat(text.dataset.begin);
            if (seenLine == null || thisTextStart <= whatTime) {
                seenLine = text;
            } else {
                break;
            }
        }
        if (seenLine) highlight(seenLine);
    }
}
/* ************************************************************************* */
// Styling of Active Text
/* ************************************************************************* */

// Keeping track of which line is highlighted.
let highlighted = null;
let highlighted_sentence = null;

// Making this a function so that this crude styling can be changed later. :-)
function highlight(text) {
    const active_text_classes = [
        'border', 'border-warning', 'rounded', // Border
        'bg-light',                            // Background
        'lead',                                // Text
        'px-1', 'mx-1'                         // Margins and Padding
    ];
    const active_sentence_classes = [
        'd-block'                              // Block Display
    ];

    if (highlighted) {
        for (const active_class of active_text_classes) {
            highlighted.classList.remove(active_class);
        }
    }
    if (highlighted_sentence) {
        for (const active_class of active_sentence_classes) {
            highlighted_sentence.classList.remove(active_class);
        }
    }

    for (const active_class of active_text_classes) {
        text.classList.add(active_class);
    }
    for (const active_class of active_sentence_classes) {
        text.parentNode.classList.add(active_class);
    }

    text.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
    highlighted = text;
    highlighted_sentence = text.parentNode;
}

/* ************************************************************************* */
// Main

{
    const audio_element = document.getElementById("audio");
    const text_elements = document.getElementsByClassName('align-text');

    // Set up handlers for click on text
    for (const text of text_elements) {
        text.addEventListener('click', (event) => {
            audio_element.currentTime = parseFloat(text.dataset.begin);
        });
    }
    // Set up handlers for time change in audio.
    // Note: This event can fire several times a second, so keep this handler light.
    // https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/timeupdate_event
    audio_element.ontimeupdate = (event) => {
        // // Don't run this more than every 100 ms.
        // if (new Date() - lastRan < 100) return;
        // lastRan = new Date();
        const whatTime = parseFloat(audio_element.currentTime.toFixed(3));
        // Find the right text. For now, O(n) loop is fine; we have at most a few hundred verses in a sarga.
        let seenLine = null;
        for (const text of text_elements) {
            const thisTextStart = parseFloat(text.dataset.begin);
            if (seenLine == null || thisTextStart <= whatTime) {
                seenLine = text;
            } else {
                break;
            }
        }
        if (seenLine) highlight(seenLine);
    }

    /* ************************************************ */
    //  Keyboard Shorctuts
    /* ************************************************ */

    // document.onkeyup = function(e) {
    //     switch (e.key) {
    //         case ' ':
    //             e.preventDefault();
    //             // Space => Toggle Play/Pause
    //             if (audio_element.paused) {
    //                 audio_element.play();
    //                 console.log("Play");
    //             } else {
    //                 audio_element.pause();
    //                 console.log("Pause");
    //             }
    //             break;

    //         default:
    //             break;
    //     }
    // }
}
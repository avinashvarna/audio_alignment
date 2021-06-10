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
    // Element Selectors
    const audio_element = document.getElementById("audio");
    const text_elements = document.getElementsByClassName('align-text');

    const loop_toggle_button = document.querySelector('#loop-toggle');
    const loop_start_button = document.querySelector('#loop-start');
    const loop_end_button = document.querySelector('#loop-end');
    const loop_toggle_label = document.querySelector('#loop-toggle-label');

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
        // Loop Logic
        const loop_active = loop_toggle_button.checked;
        if (loop_active && !audio_element.paused) {
            const loop_start = parseFloat(loop_start_button.dataset.time);
            const loop_end = parseFloat(loop_end_button.dataset.time);

            if ((loop_start != null) && (loop_end != null)) {
                if (loop_start < loop_end) {
                    if (audio_element.currentTime >= loop_end) {
                        console.log("End of loop reached. Restarting ..");
                        audio_element.currentTime = loop_start;
                    }
                }
            }
        }

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
    //  Loop Management
    /* ************************************************ */

    loop_toggle_button.addEventListener('click', function() {
        const loop_active = loop_toggle_button.checked;

        if (loop_active) {
            loop_toggle_label.classList.remove("btn-warning");
            loop_toggle_label.classList.add("btn-success");
            loop_toggle_label.innerHTML = 'Loop (ON)';
            console.log("Loop turned ON");
        } else {
            loop_toggle_label.classList.remove("btn-success");
            loop_toggle_label.classList.add("btn-warning");
            loop_toggle_label.innerHTML = 'Loop (OFF)';
            console.log("Loop turned OFF");
        }

        loop_start_button.dataset.time = null;
        loop_start_button.innerHTML = 'A';
        loop_start_button.disabled = !loop_active;

        loop_end_button.dataset.time = null;
        loop_end_button.innerHTML = 'B';
        loop_end_button.disabled = !loop_active;
    });

    loop_start_button.addEventListener('click', function() {
        loop_start_button.dataset.time = audio_element.currentTime.toFixed(2);
        loop_start_button.innerHTML = loop_start_button.dataset.time;
        console.log(`Loop Start: ${loop_start_button.dataset.time}`);
    });

    loop_end_button.addEventListener('click', function() {
        loop_end_button.dataset.time = audio_element.currentTime.toFixed(2);
        loop_end_button.innerHTML = loop_end_button.dataset.time;
        console.log(`Loop End: ${loop_end_button.dataset.time}`);
    });

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
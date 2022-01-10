/* ************************************************************************* */
// Styling of Active Text
/* ************************************************************************* */

// Keeping track of which line is highlighted.
let highlighted = null;
let highlighted_sentence = null;

// Making this a function so that this crude styling can be changed later. :-)
function highlight(text_element) {
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
        text_element.classList.add(active_class);
    }
    for (const active_class of active_sentence_classes) {
        text_element.parentNode.classList.add(active_class);
    }

    text_element.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
    highlighted = text_element;
    highlighted_sentence = text_element.parentNode;
}

function human_time(seconds) {
    var seconds = parseFloat(seconds);
    var iso_time = new Date(seconds * 1000).toISOString();
    return (seconds > 3600) ? iso_time.substr(11, 8) : iso_time.substr(14, 5);
}

/* ************************************************************************* */
// Main

{
    let active_element = null;

    // Local Storage
    const storage = window.localStorage;

    // Element Selectors
    const audio_element = document.getElementById("audio");
    const text_elements = document.getElementsByClassName('align-text');

    const loop_toggle_button = document.querySelector('#loop-toggle');
    const loop_start_button = document.querySelector('#loop-start');
    const loop_end_button = document.querySelector('#loop-end');
    const loop_toggle_label = document.querySelector('#loop-toggle-label');

    const mode_selector = document.querySelector('#repeat-mode-select');
    const url_params = new URLSearchParams(window.location.search);

    // Anuccharana Mode Variables
    storage.removeItem("current_unit_end");
    // URL params takes preference
    if(url_params.has("mode")) {
        storage.setItem("mode", url_params.get("mode"));
	}
    if (!storage.getItem("mode")) {
        storage.setItem("mode", "paragraph-1");
    }
    mode_selector.value = storage.getItem("mode");
    var current_iteration = 1;


    // Set up handlers for click on text
    for (const text_element of text_elements) {
        text_element.addEventListener('click', (event) => {
            audio_element.currentTime = parseFloat(text_element.dataset.begin);

            const current_mode = storage.getItem("mode");
            const repeat_unit = current_mode.split("-")[0];
            const active_semantic_units = {
                paragraph: text_element.parentNode.parentNode,
                sentence: text_element.parentNode,
                word: text_element,
            }
            const current_unit = active_semantic_units[repeat_unit];
            storage.setItem("current_unit_begin", current_unit.dataset.begin);
            storage.setItem("current_unit_end", current_unit.dataset.end);
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
        for (const text_element of text_elements) {
            const thisTextStart = parseFloat(text_element.dataset.begin);
            if (active_element == null || thisTextStart <= whatTime) {
                active_element = text_element;
            } else {
                break;
            }
        }
        if (active_element) highlight(active_element);

        // Anuccharana Logic
        const current_mode = storage.getItem("mode");
        const repeat_unit = current_mode.split("-")[0];
        const repeat_times = parseInt(current_mode.split("-")[1]);

        if (active_element) {
            const active_semantic_units = {
                paragraph: active_element.parentNode.parentNode,
                sentence: active_element.parentNode,
                word: active_element,
            }
            const current_unit = active_semantic_units[repeat_unit];
            if (!storage.getItem("current_unit_end")) {
                storage.setItem("current_unit_begin", current_unit.dataset.begin);
                storage.setItem("current_unit_end", current_unit.dataset.end);
            }
            var current_unit_begin = parseFloat(storage.getItem("current_unit_begin"));
            var current_unit_end = parseFloat(storage.getItem("current_unit_end"));

            if (whatTime > current_unit_end) {
                if (current_iteration < repeat_times) {
                    audio_element.currentTime = current_unit_begin;
                    current_iteration += 1;
                } else {
                    current_iteration = 1;
                    storage.setItem("current_unit_begin", current_unit.dataset.begin);
                    storage.setItem("current_unit_end", current_unit.dataset.end);
                }
            }
        }
    }

    /* ************************************************ */
    //  Anuccharana
    /* ************************************************ */

    mode_selector.addEventListener('change', e => {
        storage.setItem("mode", mode_selector.value);

        const current_mode = storage.getItem("mode");
        const repeat_unit = current_mode.split("-")[0];

        if (active_element) {
            const active_semantic_units = {
                paragraph: active_element.parentNode.parentNode,
                sentence: active_element.parentNode,
                word: active_element,
            }
            const current_unit = active_semantic_units[repeat_unit];
            storage.setItem("current_unit_begin", current_unit.dataset.begin);
            storage.setItem("current_unit_end", current_unit.dataset.end);
        }
    });

    /* ************************************************ */
    //  Playback Speed
    /* ************************************************ */

    const speed_input = document.querySelector('#speed');
    const speed_display = document.querySelector('#speed-display');
    const displayvalue = val => {
        return parseFloat(val) + 'x';
    }

    if(url_params.has('speed')) {
        speed_input.value = url_params.get('speed');
    }

    audio_element.playbackRate = speed_input.value;
    speed_display.innerText = displayvalue(audio_element.playbackRate);
    speed_input.addEventListener('change', e => {
        audio_element.playbackRate = speed_input.value;
        speed_display.innerText = displayvalue(speed_input.value);
    });

    /* ************************************************ */
    //  Loop Management
    /* ************************************************ */

    loop_toggle_button.addEventListener('click', function() {
        const loop_active = loop_toggle_button.checked;

        if (loop_active) {
            loop_toggle_label.classList.remove("btn-secondary");
            loop_toggle_label.classList.add("btn-success");
            loop_toggle_label.innerHTML = 'Loop (ON)';
            console.log("Loop turned ON");
        } else {
            loop_toggle_label.classList.remove("btn-success");
            loop_toggle_label.classList.add("btn-secondary");
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
        loop_start_button.dataset.time = audio_element.currentTime.toFixed(3);
        loop_start_button.innerHTML = human_time(loop_start_button.dataset.time);
        console.log(`Loop Start: ${loop_start_button.dataset.time}`);
    });

    loop_end_button.addEventListener('click', function() {
        loop_end_button.dataset.time = audio_element.currentTime.toFixed(3);
        loop_end_button.innerHTML = human_time(loop_end_button.dataset.time);
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
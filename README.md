# audio_alignment

Collection of scripts and utilities to align Sanskrit text and audio.

To use the scripts and perform alignment of text and audio:
1. Install `aeneas` using `pip install aeneas`
2. Install the required libraries - `ffprobe ffmpeg espeak libespeak-dev` (E.g. using `apt` on `Ubuntu`).
3. Use the [`align`](https://github.com/avinashvarna/audio_alignment/blob/main/utils/alignment.py#L16)
function in `utils/alignment.py` to align the text and audio.

For examples, please see `align.py` in the [`rAmAyaNa`](https://github.com/avinashvarna/audio_alignment/tree/main/ramayana)
or [`meghaduta`](https://github.com/avinashvarna/audio_alignment/tree/main/meghaduta) subdirectories.

# Website

Please see the result at the [project page](https://avinashvarna.github.io/audio_alignment/)

# Adding new data

To contribute new data to the project, please follow these [Instructions](https://github.com/avinashvarna/audio_alignment/blob/main/interface/README.md#how-to-add-new-data)

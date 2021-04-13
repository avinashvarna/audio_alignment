# Bootstrap5-powered Interface for Viewing Audio-Text Corpus

## Credits

Original JS logic of [Shreevatsa](https://shreevatsa.net/ramayana/) is copied almost verbatim.

## Features

* Flask application
* Change in audio highlights the section being read, clicking on text to navigates to the relevant location in audio (JS)
* Display of all corpora in a neat accordion (Every directory which has a valid `data.json` file, will appear in the corpus list)
* Flask-Frozen can be used to generate static site
    `python3 freeze.py`

# Structure of `data.json`

```
{
    'name': 'name of the corpus to display',
    'description': 'description of corpus',
    'data': [
        {
            'id': 'text-used-to-refer-to-the-file',
            'name': 'name of the chapter to display in the corpus list',
            'audio_url': 'url that will be used as is (can still be relative',
            'word_alignment': 'path to the file containing word alignment',
            'sentence_alignment': 'path to the file containing sentence alignment, unused'
        }, ...

    ]
}
```

**Extra**:

* Required Corpus Fields: `name`, `data`
* Required Chapter Fields: `id`, `name`, `audio_url`, `word_alignment`
* Corpus `description` can (and in most cases should) contain HTML. This can contain information such as historical information about corpus, text source, audio source, aligned-by etc.
* Chapter's `id` can be any string, but for the aesthetics, should be semantically relevant and URL friendly
* `word_alignment` file path, if not absolute, must be relative to the corpus path (This is path per file, not the path to the directory)

## How to add new data?

To add new data,
* Run the alignment code and generate `word_alignment` (`sentence_alignment` is not required)
* Add a new directory in the `corpus_dir`, (currently the parent directory of the `interface`) (besides others such as ramayana, meghaduta),
* Create `data.json` file inside that directory with relevant information. This would often entail manual creation (for deciding "good" chapter-ids, corpus name, corpus description), although of course, some parts of it can be automated.


### TODO

* "Previous" and "Next" buttons for navigation within a corpus
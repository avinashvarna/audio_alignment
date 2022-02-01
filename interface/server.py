#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 02:52:57 2021

@author: Hrishikesh Terdalkar
"""

###############################################################################

import re
import os
import json

from flask import Flask, render_template, url_for, redirect
from natsort import natsorted

from settings import CONFIG as cfg

###############################################################################


def load_corpora():
    """Load Corpus Information"""
    corpora = {}
    for corpus_data_file in natsorted(cfg.CORPUS_DATA_FILES):
        with open(corpus_data_file, encoding='utf-8') as f:
            corpus_data = json.load(f)

        chapter_list = corpus_data.get('data', [])
        chapters = {}
        prev_id = None

        for chapter in chapter_list:
            if not isinstance(chapter, dict):
                continue

            chapter_id = chapter['id']
            chapter['prev_id'] = prev_id
            chapter['next_id'] = None
            chapters[chapter_id] = chapter

            if prev_id is not None:
                chapters[prev_id]['next_id'] = chapter_id
            prev_id = chapter_id

        corpus_path = os.path.dirname(corpus_data_file)
        corpus_id = os.path.basename(corpus_path)
        corpora[corpus_id] = {
            'id': corpus_id,
            'path': corpus_path,
            'name': corpus_data.get('name', corpus_id),
            'description': corpus_data.get('description', None),
            'accordion': corpus_data.get('accordion', True),
            'data': chapters
        }
    return corpora


###############################################################################

CORPORA = load_corpora()

###############################################################################

webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = cfg.SECRET_KEY
webapp.url_map.strict_slashes = False

###############################################################################
# Corpus Parsing


def zfill(int_or_str, length):
    return str(int_or_str).zfill(length)


def create_hierarchy_from_text(text_path):
    with open(text_path, mode='r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    p_id = 1
    s_id = 1
    w_id = 1
    id_length = 6

    p_tags = []
    s_tags = []
    w_tags = []

    for line in lines:
        if not line.strip():
            p_tags.append({
                "id": f"p{zfill(p_id, id_length)}",
                "tag": "p",
                "data": s_tags
            })
            p_id += 1
            s_id = 1
            w_id = 1
            s_tags = []
        else:
            # Assumption that text within [] will not contain spaces
            words = line.split()
            for word in words:
                ignored_match = re.match(r"\[(.*?)\]", word)
                if ignored_match:
                    w_tags.append({
                        "tag": "span",
                        "text": ignored_match.group(1)
                    })
                    continue

                _w_id = (f'p{zfill(p_id, id_length)}'
                         f's{zfill(s_id, id_length)}'
                         f'w{zfill(w_id, id_length)}')
                w_tags.append({
                    "id": _w_id,
                    "tag": "span",
                    "text": word
                })
                w_id += 1

            _s_id = f'p{zfill(p_id, id_length)}s{zfill(s_id, id_length)}'
            s_tags.append({
                "id": _s_id,
                "tag": "span",
                "data": w_tags
            })

            s_id += 1
            w_id = 1
            w_tags = []
    else:
        p_tags.append({
            "id": f"p{zfill(p_id, id_length)}",
            "tag": "p",
            "data": s_tags
        })

    return p_tags


def create_hierarchy_from_alignment(word_alignment_path):
    with open(word_alignment_path, encoding='utf-8') as f:
        word_alignment = json.load(f)

    # content = list of paragraphs
    # paragraph = list of lines
    content = []
    current_paragraph = []
    current_line = []
    last_s = 1
    last_p = 1
    for fragment in word_alignment['fragments']:
        fragment_id = fragment['id']
        match = re.match(r'^p(\d+)s(\d+)w(\d+)$', fragment_id)
        if match:
            p = int(match.group(1))
            s = int(match.group(2))
            if s > last_s:
                current_paragraph.append(current_line)
                current_line = []
                last_s = s
            if p > last_p:
                current_paragraph.append(current_line)
                content.append(current_paragraph)
                current_paragraph = []
                current_line = []
                last_p = p
                last_s = s
        current_line.append(fragment)

    if current_line:
        current_paragraph.append(current_line)
    if current_paragraph:
        content.append(current_paragraph)

    return content


def create_alignment_times(word_alignment_path):
    with open(word_alignment_path, encoding="utf-8") as f:
        word_alignment = json.load(f)

    alignment_times = {}
    prev_p_id = None
    prev_s_id = None

    for fragment in word_alignment["fragments"]:
        match = re.match(r'^(p\d+)(s\d+)(w\d+)$', fragment["id"])
        if match:
            curr_p_id = match.group(1)
            curr_s_id = f"{match.group(1)}{match.group(2)}"

            if curr_p_id != prev_p_id:
                if prev_p_id is not None:
                    alignment_times[prev_p_id]["end"] = fragment["begin"]
                prev_p_id = curr_p_id
                alignment_times[curr_p_id] = {
                    "begin": fragment["begin"]
                }

            if curr_s_id != prev_s_id:
                if prev_s_id is not None:
                    alignment_times[prev_s_id]["end"] = fragment["begin"]
                prev_s_id = curr_s_id
                alignment_times[curr_s_id] = {
                    "begin": fragment["begin"]
                }

        alignment_times[fragment["id"]] = {
            "begin": fragment["begin"],
            "end": fragment["end"]
        }

    alignment_times[curr_p_id]["end"] = fragment["end"]
    alignment_times[curr_s_id]["end"] = fragment["end"]

    return alignment_times

###############################################################################


@webapp.context_processor
def inject_globals():
    """Available in each path"""
    return {
        'title': 'Audio Alignment',
    }

###############################################################################
# Views


@webapp.route("/corpus/")
@webapp.route("/corpus/<string:corpus_id>/")
@webapp.route("/corpus/<string:corpus_id>/<string:chapter_id>/")
def show_corpus(corpus_id=None, chapter_id=None):
    """Corpus View"""
    data = {}
    data['corpora'] = CORPORA
    data['corpus'] = {}
    data['chapter'] = {}
    data['accordion'] = True

    if corpus_id is not None:
        if corpus_id not in CORPORA:
            return redirect(url_for('show_corpus'))

    if chapter_id is not None:
        corpus_path = CORPORA[corpus_id]['path']
        if chapter_id not in CORPORA[corpus_id]['data']:
            return redirect(url_for('show_corpus', corpus=corpus_id))

        corpus = CORPORA[corpus_id]
        chapter = corpus['data'][chapter_id]

        if not corpus['accordion']:
            data['accordion'] = False

        data['corpus'] = corpus
        data['chapter'] = chapter
        data['title'] = f"{corpus['name']} &bull; {chapter['name']}"
        data['audio'] = chapter['audio_url']

        word_alignment_file = os.path.join(
            corpus_path, chapter['word_alignment']
        )

        if chapter.get('text') is not None:
            chapter_text_file = os.path.join(corpus_path, chapter['text'])
            chapter_hierarchy = create_hierarchy_from_text(chapter_text_file)
            alignment_times = create_alignment_times(word_alignment_file)

            data['structure_from'] = 'text'
            data['hierarchy'] = chapter_hierarchy
            data['alignment'] = alignment_times
        else:
            data['structure_from'] = 'alignment'
            hierarchy = create_hierarchy_from_alignment(word_alignment_file)
            data['hierarchy'] = hierarchy

    return render_template("corpus.html", data=data)


@webapp.route("/help/")
def show_help():
    data = {'title': 'Help'}
    return render_template("help.html", data=data)


@webapp.route("/")
def home():
    return render_template("about.html")

###############################################################################


if __name__ == '__main__':
    import socket

    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = '8484'

    webapp.run(host=host, port=port, debug=True)

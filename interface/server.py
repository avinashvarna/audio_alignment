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
        if "id" in fragment:
            fragment_id = fragment['id']
            match = re.match(r'^p(\d+)s(\d+)w(\d+)$', fragment_id)
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

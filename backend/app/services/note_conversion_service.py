#!/usr/bin/env python3

import re

def convert_to_atomic_notes(content):
    # TODO: Update based on ML techniques
    lines = content.split('\n')
    atomic_notes = []
    current_note = None

    for line in lines:
        if line.startswith('#'):
            if current_note:
                atomic_notes.append(current_note)
            level = len(re.match(r'^#+', line).group())
            title = line.lstrip('#').strip()
            current_note = {'title': title, 'content': '', 'level': level}
        elif current_note:
            current_note['content'] += line + '\n'

    if current_note:
        atomic_notes.append(current_note)

    # Generate backlinks
    for i, note in enumerate(atomic_notes):
        for other_note in atomic_notes[i+1:]:
            if note['title'].lower() in other_note['content'].lower():
                other_note['content'] += f"\n\nSee also: [[{note['title']}]]"
            if other_note['title'].lower() in note['content'].lower():
                note['content'] += f"\n\nSee also: [[{other_note['title']}]]"

    return atomic_notes

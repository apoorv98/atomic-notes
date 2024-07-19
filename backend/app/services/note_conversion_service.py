#!/usr/bin/env python3

import re

def convert_to_atomic_notes(content):
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

    return atomic_notes

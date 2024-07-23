#!/usr/bin/env python3

import pytest
from app.services.note_conversion_service import convert_to_atomic_notes

def test_convert_to_atomic_notes():
    content = """# Main Topic

## Subtopic 1
This is some content for subtopic 1.

## Subtopic 2
This is some content for subtopic 2.

### Sub-subtopic 2.1
More detailed information here.
"""

    atomic_notes = convert_to_atomic_notes(content)
    assert len(atomic_notes) == 4
    assert atomic_notes[0]['title'] == 'Main Topic'
    assert atomic_notes[1]['title'] == 'Subtopic 1'
    assert atomic_notes[2]['title'] == 'Subtopic 2'
    assert atomic_notes[3]['title'] == 'Sub-subtopic 2.1'

def test_convert_to_atomic_notes_with_backlinks():
    content = """# Main Topic

## Subtopic 1
This is some content for subtopic 1.
See also: [[Subtopic 2]]

## Subtopic 2
This is some content for subtopic 2.
Related to [[Subtopic 1]]
"""

    atomic_notes = convert_to_atomic_notes(content)
    assert len(atomic_notes) == 3
    assert '[[Subtopic 2]]' in atomic_notes[1]['content']
    assert '[[Subtopic 1]]' in atomic_notes[2]['content']

def test_convert_to_atomic_notes_empty_content():
    content = ""
    atomic_notes = convert_to_atomic_notes(content)
    assert len(atomic_notes) == 0

def test_convert_to_atomic_notes_single_note():
    content = "# Single Note\n\nThis is a single note without subtopics"
    atomic_notes = convert_to_atomic_notes(content)
    assert len(atomic_notes) == 1
    assert atomic_notes[0]['title'] == 'Single Note'
    assert 'This is a single note wihtout subtopics' in atomic_notes[0]['content']

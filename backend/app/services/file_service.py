#!/usr/bin/env python3

from app.models.note import Note
from app import db

def create_note(user_id, title, content):
    note = Note(user_id=user_id, title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return note

def get_note(note_id):
    return Note.query.get(note_id)

def update_note(note_id, title, content):
    note = Note.query.get(note_id)
    if note:
        note.title = title
        note.content = content
        db.session.commit()
    return note

def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return True

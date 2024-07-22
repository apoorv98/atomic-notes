#!/usr/bin/env python3

from app.models.note import Note
from app import db

def create_note(user_id, title, content):
    note = Note(user_id=user_id, title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return note

def get_note(note_id):
    return db.session.get(Note, note_id)

def get_all_notes(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    return [{
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat(),
        'updated_at': note.updated_at.isoformat()
    } for note in notes]

def update_note(note_id, title, content):
    note = db.session.get(Note, note_id)
    if note:
        note.title = title
        note.content = content
        db.session.commit()
    return note

def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return True

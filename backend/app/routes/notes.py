#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.file_service import create_note, get_note, get_all_notes, update_note, delete_note
from app.services.note_conversion_service import convert_to_atomic_notes

notes = Blueprint('notes', __name__)

@notes.route('', methods=['POST'])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    data = request.get_json()
    note = create_note(user_id, data['title'], data['content'])
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content}), 201

@notes.route('', methods=['GET'])
@jwt_required
def get_all():
    user_id = get_jwt_identity()
    notes = get_all_notes(user_id)
    return jsonify(notes)

@notes.route('/<int:note_id>', methods=['GET'])
@jwt_required()
def read(note_id):
    note = get_note(note_id)
    if note:
        return jsonify({'id': note.id, 'title': note.title, 'content': note.content})
    return jsonify({'error': 'Note not found'}), 404

@notes.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def update(note_id):
    data = request.get_json()
    note = update_note(note_id, data['title'], data['content'])
    if note:
        return jsonify({'id': note.id, 'title': note.title, 'content': note.content})
    return jsonify({'error': 'Note not found'}), 404

@notes.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete(note_id):
    if delete_note(note_id):
        return '', 204
    return jsonify({'error': 'Note not found'}), 404

@notes.route('/<int:note_id>/convert', methods=['POST'])
@jwt_required()
def convert(note_id):
    current_user_id = get_jwt_identity()
    note = get_note(note_id)

    if not note or note.use_id != current_user_id:
        return jsonify({'message': 'Note not found or unauthorized'}), 404

    atomic_notes = convert_to_atomic_notes(note.content)

    if atomic_notes:
        for atomic_note in atomic_notes:
            create_note(current_user_id, atomic_note['title'], atomic_note['content'])

    return jsonify({'message': 'Note split to atomic notes successfully', 'atomic_notes': atomic_notes}), 200

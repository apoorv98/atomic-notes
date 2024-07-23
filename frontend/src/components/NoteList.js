import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import axios from "axios";

const NoteList = () => {
    const [notes, setNotes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const { logout } = useAuth();

    useEffect(() => {
        fetchNotes();
    }, []);

    const fetchNotes = async () => {
        try {
            // const token = localStorage.getItem("token");
            // if (!token) {
            //     navigate("/login");
            //     return;
            // }
            const response = await axios.get("/api/notes", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });
            setNotes(response.data);
            setLoading(false);
        } catch (err) {
            setError("Failed to fetch notes. Please try again.");
            setLoading(false);
        }
    };

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    const createNewNote = async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await axios.post(
                "/api/notes",
                {
                    title: "New Note",
                    content: "Start writing your note here...",
                },
                { headers: { Authorization: `Bearer ${token}` } },
            );
            navigate(`/notes/${response.data.id}`);
        } catch (err) {
            setError("Failed to create a new note. Please try again.");
        }
    };

    if (loading) return <div className="text-center mt-8">Loading...</div>;

    return (
        <div className="max-w-4xl mx-auto mt-8">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Your Notes</h2>
                <button
                    onClick={handleLogout}
                    className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                >
                    Logout
                </button>
                <button
                    onClick={createNewNote}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                    Create New Note
                </button>
            </div>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            {notes.length === 0 ? (
                <p className="text-gray-600">
                    You don't have any notes yet. Create one to get started!
                </p>
            ) : (
                <ul className="bg-white shadow overflow-hidden sm:rounded-md">
                    {notes.map((note) => (
                        <li
                            key={note.id}
                            className="border-b border-gray-200 last:border-b-0"
                        >
                            <Link
                                to={`/notes/${note.id}`}
                                className="block hover:bg-gray-50"
                            >
                                <div className="px-4 py-4 sm:px-6">
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm font-medium text-indigo-600 truncate">
                                            {note.title}
                                        </p>
                                        <div className="ml-2 flex-shrink-0 flex">
                                            <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                {new Date(
                                                    note.updated_at,
                                                ).toLocaleDateString()}
                                            </p>
                                        </div>
                                    </div>
                                    <div className="mt-2 sm:flex sm:justify-between">
                                        <div className="sm:flex">
                                            <p className="flex items-center text-sm text-gray-500">
                                                {note.content.substring(0, 100)}
                                                ...
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default NoteList;

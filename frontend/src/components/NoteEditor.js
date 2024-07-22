import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const NoteEditor = () => {
    const [note, setNote] = useState({ title: "", content: "" });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [saving, setSaving] = useState(false);
    const [atomicNotes, setAtomicNotes] = useState([]);
    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchNote = async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    navigate("/login");
                    return;
                }
                if (id !== "new") {
                    const response = await axios.get(`/api/notes/${id}`, {
                        headers: { Authorization: `Bearer ${token}` },
                    });
                    setNote(response.data);
                }
                setLoading(false);
            } catch (err) {
                setError("Failed to fetch note. Please try again.");
                setLoading(false);
            }
        };

        fetchNote();
    }, [id, navigate]);

    const handleSave = async () => {
        try {
            setSaving(true);
            const token = localStorage.getItem("token");
            if (id === "new") {
                await axios.post("/api/notes", note, {
                    headers: { Authorization: `Bearer ${token}` },
                });
            } else {
                await axios.put(`/api/notes/${id}`, note, {
                    headers: { Authorization: `Bearer ${token}` },
                });
            }
            setSaving(false);
            navigate("/notes");
        } catch (err) {
            setError("Failed to save note. Please try again.");
            setSaving(false);
        }
    };

    const handleDelete = async () => {
        if (window.confirm("Are you sure you want to delete this note?")) {
            try {
                const token = localStorage.getItem("token");
                await axios.delete(`/api/notes/${id}`, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                navigate("/notes");
            } catch (err) {
                setError("Failed to delete note. Please try again.");
            }
        }
    };

    const handleConvertToAtomic = async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await axios.post(
                `/api/notes/${id}/convert`,
                {},
                {
                    headers: { Authorization: `Bearer ${token}` },
                },
            );
            setAtomicNotes(response.data);
        } catch (err) {
            setError(
                "Failed to convert note to atomic notes. Please try again.",
            );
        }
    };

    if (loading) return <div className="text-center mt-8">Loading...</div>;

    return (
        <div className="max-w-4xl mx-auto mt-8">
            <div className="mb-4">
                <input
                    type="text"
                    value={note.title}
                    onChange={(e) =>
                        setNote({ ...note, title: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Note Title"
                />
            </div>
            <div className="mb-4">
                <textarea
                    value={note.content}
                    onChange={(e) =>
                        setNote({ ...note, content: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="10"
                    placeholder="Note Content"
                />
            </div>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            <div className="flex justify-between">
                <button
                    onClick={handleSave}
                    disabled={saving}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    {saving ? "Saving..." : "Save Note"}
                </button>
                <button
                    onClick={handleConvertToAtomic}
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    Convert to Atomic Notes
                </button>
                {id !== "new" && (
                    <button
                        onClick={handleDelete}
                        className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Delete Note
                    </button>
                )}
            </div>
            {atomicNotes.length > 0 && (
                <div className="mt-8">
                    <h3 className="text-xl font-bold mb-4">Atomic Notes</h3>
                    <ul className="space-y-4">
                        {atomicNotes.map((atomicNote, index) => (
                            <li
                                key={index}
                                className="border border-gray-300 rounded-md p-4"
                            >
                                <h4 className="font-bold">
                                    {atomicNote.title}
                                </h4>
                                <p>{atomicNote.content}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default NoteEditor;

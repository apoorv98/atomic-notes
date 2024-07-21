import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import NoteList from "./components/NoteList";
import NoteEditor from "./components/NoteEditor";

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold text-gray-900">Atomic Notes</h1>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/notes" element={<NoteList />} />
              <Route path="/notes/:id" element={<NoteEditor />} />
              <Route path="/" element={<NoteList />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
};

export default App;

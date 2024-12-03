// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import NotesPage from './components/Notes/NotesPage';
import CreateNote from './components/Notes/CreateNote';
import EditNote from './components/Notes/EditNote';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/notes" element={<NotesPage />} />
        <Route path="/notes/new" element={<CreateNote />} />
        <Route path="/notes/:id/edit" element={<EditNote />} />
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
  );
};

export default App;

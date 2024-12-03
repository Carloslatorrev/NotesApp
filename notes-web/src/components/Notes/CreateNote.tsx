// src/components/Notes/CreateNote.tsx
import React, { useState } from 'react';
import { TextField, Button, Container, CircularProgress, Typography } from '@mui/material';
import { createNote } from '../../services/notesService';
import { useNavigate } from 'react-router-dom';

const CreateNote: React.FC = () => {
  const [title, setTitle] = useState<string>('');
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleCreateNote = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createNote(title, content);
      navigate('/notes');
    } catch (err: any) {
      setError('No se pudo crear la nota.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Crear Nota
      </Typography>
      <form onSubmit={handleCreateNote}>
        <TextField
          label="Título"
          variant="outlined"
          fullWidth
          margin="normal"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <TextField
          label="Contenido"
          variant="outlined"
          fullWidth
          margin="normal"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          multiline
          rows={4}
          required
        />
        {error && <Typography color="error">{error}</Typography>}
        <Button type="submit" variant="contained" color="primary" fullWidth disabled={loading}>
          {loading ? <CircularProgress size={24} color="inherit" /> : 'Crear Nota'}
        </Button>
      </form>
    </Container>
  );
};

export default CreateNote;

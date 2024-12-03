// src/components/Notes/EditNote.tsx
import React, { useEffect, useState } from 'react';
import { TextField, Button, Container, CircularProgress, Typography } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { getNote, updateNote } from '../../services/notesService';

const EditNote: React.FC = () => {
  const [title, setTitle] = useState<string>('');
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();

  const fetchNote = async () => {
    if (id) {
      setLoading(true);
      try {
        const note = await getNote(id);
        setTitle(note.title);
        setContent(note.content);
      } catch (err) {
        setError('No se pudo cargar la nota.');
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    fetchNote();
  }, [id]);

  const handleUpdateNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    setLoading(true);
    setError(null);

    try {
      await updateNote(id, title, content);
      navigate('/notes');
    } catch (err: any) {
      setError('No se pudo actualizar la nota.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Editar Nota
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        <form onSubmit={handleUpdateNote}>
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
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Actualizar Nota'}
          </Button>
        </form>
      )}
    </Container>
  );
};

export default EditNote;

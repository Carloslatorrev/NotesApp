// src/components/Notes/NotesPage.tsx
import React, { useEffect, useState } from 'react';
import { Button, Container, Grid, Typography, CircularProgress, Card, CardContent, CardActions } from '@mui/material';
import { getNotes, deleteNote } from '../../services/notesService';
import { useNavigate } from 'react-router-dom';

const NotesPage: React.FC = () => {
  const [notes, setNotes] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  
  const fetchNotes = async () => {
    setLoading(true);
    setError(null);
    try {
      const fetchedNotes = await getNotes();
      setNotes(fetchedNotes);
    } catch (err) {
      setError('No se pudieron cargar las notas.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  
  const handleDelete = async (id: string) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar esta nota?')) {
      setLoading(true);
      try {
        await deleteNote(id);
        fetchNotes(); 
      } catch (err) {
        setError('Hubo un problema al eliminar la nota.');
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        Mis Notas
      </Typography>
      {loading && <CircularProgress />}
      {error && <Typography color="error">{error}</Typography>}
      <Grid container spacing={2}>
        {notes.map((note) => (
          <Grid item xs={12} sm={6} md={4} key={note.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{note.title}</Typography>
                <Typography variant="body2">{note.content}</Typography>
                <Typography variant="caption" color="textSecondary">{new Date(note.createdAt).toLocaleString()}</Typography>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => navigate(`/notes/${note.id}/edit`)}>Editar</Button>
                <Button size="small" color="error" onClick={() => handleDelete(note.id)}>Eliminar</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Button variant="contained" color="primary" onClick={() => navigate('/notes/new')} fullWidth>
        Crear Nota
      </Button>
    </Container>
  );
};

export default NotesPage;

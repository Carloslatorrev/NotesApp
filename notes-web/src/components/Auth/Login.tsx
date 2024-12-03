import React, { useState } from 'react';
import { TextField, Button, CircularProgress, Typography, Container } from '@mui/material';
import { login } from '../../services/authService';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await login(email, password);
      console.log('Respuesta del login:', response); 
      if (response && response.access_token) {
        
        localStorage.setItem("token", response.access_token);

        
        navigate('/notes');
      } else {
        setError('No se encontró el token en la respuesta');
      }
    } catch (err: any) {
      console.error(err);
      setError('Inicio de sesión fallido. Verifica tus credenciales.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterRedirect = () => {
    navigate('/register'); 
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Iniciar Sesión
      </Typography>
      <form onSubmit={handleLogin}>
        <TextField
          label="Correo electrónico" 
          variant="outlined"
          fullWidth
          margin="normal"
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          required
        />
        <TextField
          label="Contraseña"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <Typography color="error">{error}</Typography>}
        <Button type="submit" variant="contained" color="primary" fullWidth disabled={loading}>
          {loading ? <CircularProgress size={24} color="inherit" /> : 'Iniciar sesión'}
        </Button>
      </form>

      <Button 
        variant="text" 
        color="secondary" 
        onClick={handleRegisterRedirect} 
        fullWidth
        style={{ marginTop: '10px' }}
      >
        Registrar
      </Button>
    </Container>
  );
};

export default Login;

import axios, { AxiosError } from 'axios';
import { getToken } from './authService';  

const API_URL = "http://127.0.0.1:8000/notes"; 


export const getNotes = async () => {
  try {
    const token = getToken();  
    if (!token) throw new Error('No token found');

    const response = await axios.get(API_URL, {
      headers: {
        'Authorization': `Bearer ${token}`,  
      },
    });

    return response.data;
  } catch (error) {
    
    if ((error as AxiosError).response) {
      const axiosError = error as AxiosError;
      
      if (axiosError.response?.status === 404) {
        return [];
      }
    }
    
    throw new Error('No se pudieron cargar las notas.');
  }
};


export const getNote = async (id: string) => {
  try {
    const token = getToken();
    if (!token) throw new Error('No token found');

    const response = await axios.get(`${API_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    return response.data;
  } catch (error) {
    throw new Error('No se pudo obtener la nota.');
  }
};


export const createNote = async (title: string, content: string) => {
  try {
    const token = getToken();
    if (!token) throw new Error('No token found');

    const response = await axios.post(API_URL, { title, content }, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    return response.data;
  } catch (error) {
    throw new Error('No se pudo crear la nota.');
  }
};


export const updateNote = async (id: string, title: string, content: string) => {
  try {
    const token = getToken();
    if (!token) throw new Error('No token found');

    const response = await axios.put(`${API_URL}/${id}`, { title, content }, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    return response.data;
  } catch (error) {
    throw new Error('No se pudo actualizar la nota.');
  }
};


export const deleteNote = async (id: string) => {
  try {
    const token = getToken();
    if (!token) throw new Error('No token found');

    const response = await axios.delete(`${API_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    return response.data;
  } catch (error) {
    throw new Error('No se pudo eliminar la nota.');
  }
};

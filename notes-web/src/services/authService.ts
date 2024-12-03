import axios from "axios";

const API_URL = "http://127.0.0.1:8000/auth";


export const register = async (username: string, password: string, email: string) => {
    const response = await axios.post(`${API_URL}/register`, { username, password, email });
    return response.data; 
};


export const login = async (email: string, password: string) => {
    const response = await axios.post(`${API_URL}/login`, { email, password });
    localStorage.setItem("user", JSON.stringify(response.data)); 
    return response.data; 
};


export const logout = () => {
    localStorage.removeItem("user");
};


export const getToken = () => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    return user?.access_token;  
};


export const getCurrentUser = () => {
    return JSON.parse(localStorage.getItem("user") || "{}");
};

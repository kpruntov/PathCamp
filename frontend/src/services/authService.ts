import axios from 'axios';

const API_URL = '/api';

export const register = (username, email, password) => {
    return axios.post(`${API_URL}/users/`, {
        username,
        email,
        password,
    });
};

export const login = (username, password) => {
    return axios.post(`${API_URL}/login`, {
        username,
        password,
    });
};

export const logout = () => {
    // In a real app, you might want to call a backend endpoint to invalidate the token
    // For now, we'll just remove the token from local storage on the client side
    localStorage.removeItem('user');
    return Promise.resolve();
};

// @trace TASK-021

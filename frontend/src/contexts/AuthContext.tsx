import React, { createContext, useState } from 'react';
import * as authService from '../services/authService';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const storedUser = localStorage.getItem('user');
        return storedUser ? JSON.parse(storedUser) : null;
    });

    const login = async (username, password) => {
        const response = await authService.login(username, password);
        if (response.data.access_token) {
            const userData = { username, token: response.data.access_token };
            setUser(userData);
            localStorage.setItem('user', JSON.stringify(userData));
        }
        return response;
    };

    const logout = () => {
        authService.logout();
        setUser(null);
    };

    const register = (username, email, password) => {
        return authService.register(username, email, password);
    };

    const value = {
        user,
        login,
        logout,
        register,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// @trace TASK-021

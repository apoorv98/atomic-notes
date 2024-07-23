import React, { createContext, useState, useContext, useEffect } from "react";
import axios from "axios";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            verifyToken(token);
        } else {
            setLoading(false);
        }
    }, []);

    const verifyToken = async (token) => {
        try {
            const response = await axios.get("/api/auth/verify", {
                headers: { Authorization: `Bearer ${token}` },
            });
            setUser(response.data.user);
        } catch (error) {
            console.error("Token verification failed:", error);
            localStorage.removeItem("token");
        } finally {
            setLoading(false);
        }
    };

    const login = async (username, password) => {
        try {
            const response = await axios.post("/api/auth/login", {
                username,
                password,
            });
            const { access_token, user } = response.data;
            localStorage.setItem("token", access_token);
            setUser(user);
            return true;
        } catch (error) {
            console.error("Login failed:", error);
            return false;
        }
    };

    const register = async (username, email, password) => {
        try {
            const response = await axios.post("/api/auth/register", {
                username,
                email,
                password,
            });
            const { access_token, user } = response.data;
            localStorage.setItem("token", access_token);
            setUser(user);
            return true;
        } catch (error) {
            console.error("Registration failed:", error);
            return false;
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{ user, login, register, logout, loading }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);

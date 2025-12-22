import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

export default function NavbarAuth() {
    const { isAuthenticated, user } = useAuth();

    if (isAuthenticated && user) {
        return (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span style={{ color: 'var(--ifm-navbar-link-color)' }}>
                    Welcome, {user.name || user.email}
                </span>
            </div>
        );
    }

    return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <a href="/login" className="navbar__link">
                Sign In
            </a>
            <a href="/signup" className="button button--primary button--sm">
                Sign Up
            </a>
        </div>
    );
}

import React, { createContext, useContext, ReactNode, useEffect, useState } from 'react';
import { authClient, useSession, signIn, signOut, signUp } from '../lib/authClient';
import { clearAuthData, getToken, storeToken } from '../utils/tokenStorage';

interface AuthContextType {
  user: any;
  isLoading: boolean;
  isAuthenticated: boolean;
  signIn: any;
  signOut: any;
  signUp: any;
  getToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { data: session, isPending } = useSession();

  // Function to get user info (JWT logic removed)
  const getTokenFromAuthClient = async (): Promise<string | null> => {
    // JWT logic has been removed, returning null
    return null;
  };

  // Ensure session persistence across page refreshes
  useEffect(() => {
    // This useEffect helps maintain session state when the page refreshes
    // The useSession hook from BetterAuth handles the persistence internally
  }, []);

  const value: AuthContextType = {
    user: session?.user,
    isLoading: isPending,
    isAuthenticated: !!session?.user,
    signIn,
    signOut,
    signUp,
    getToken: getTokenFromAuthClient,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
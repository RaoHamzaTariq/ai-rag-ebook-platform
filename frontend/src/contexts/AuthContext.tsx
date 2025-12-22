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

  // Function to get JWT token from BetterAuth client and store it
  const getTokenFromAuthClient = async (): Promise<string | null> => {
    try {
      const tokenResponse = await authClient.token();

      const token = tokenResponse?.data?.token;

      if (token) {
        // Store the token for potential use by other parts of the app
        storeToken(token);
        return token;
      }
      return null;
    } catch (error) {
      console.error('Error getting token from auth client:', error);
      return null;
    }
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
// frontend/src/components/auth/signup-form/index.tsx
import React, { useState } from 'react';
import styles from './styles.module.css';
import { signUp } from '../../../lib/authClient';
import { useNavigate } from 'react-router-dom';

interface SignupFormProps {
  onSignupSuccess?: () => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({ onSignupSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await signUp.email({
        email,
        password,
        name,
        callbackURL: "/dashboard", // Redirect after signup
      });

      if (!response) {
        setError('Failed to create account');
      } else if (onSignupSuccess) {
        onSignupSuccess();
      } else {
        navigate('/dashboard'); // Default redirect
      }
    } catch (err) {
      setError('An error occurred during signup');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.inputGroup}>
        <label htmlFor="name" className={styles.label}>Full Name</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className={styles.input}
          required
          disabled={isLoading}
        />
      </div>

      <div className={styles.inputGroup}>
        <label htmlFor="email" className={styles.label}>Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
          required
          disabled={isLoading}
        />
      </div>

      <div className={styles.inputGroup}>
        <label htmlFor="password" className={styles.label}>Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
          required
          minLength={6}
          disabled={isLoading}
        />
      </div>

      <button type="submit" className={styles.button} disabled={isLoading}>
        {isLoading ? 'Creating account...' : 'Sign Up'}
      </button>
    </form>
  );
};
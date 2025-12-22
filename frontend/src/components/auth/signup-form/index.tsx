// frontend/src/components/auth/signup-form/index.tsx
import React, { useState } from 'react';
import styles from './styles.module.css';
import { signUp } from '../../../lib/authClient';
import { useHistory } from '@docusaurus/router';

interface SignupFormProps {
  onSignupSuccess?: () => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({ onSignupSuccess }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const history = useHistory();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const { data, error } = await signUp.email({
        email,
        password,
        name,
        callbackURL: "/", // Redirect to home after signup
      });

      if (error) {
        setError(error.message || 'Error creating account');
      } else if (onSignupSuccess) {
        onSignupSuccess();
      } else {
        history.push('/'); // Default redirect
      }
    } catch (err: any) {
      setError(err?.message || 'An unexpected error occurred');
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
          placeholder="First Last"
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
          placeholder="you@example.com"
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
          disabled={isLoading}
          minLength={8}
          placeholder="Min. 8 characters"
        />
      </div>

      <button type="submit" className={styles.button} disabled={isLoading}>
        {isLoading ? 'Creating account...' : 'Create Account'}
      </button>
    </form>
  );
};

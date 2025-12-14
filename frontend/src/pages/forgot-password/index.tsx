// frontend/src/pages/forgot-password/index.tsx
import React from 'react';
import styles from './styles.module.css';
import { Link } from 'react-router-dom';

const ForgotPasswordPage: React.FC = () => {
  return (
    <div className={styles.forgotPasswordContainer}>
      <div className={styles.forgotPasswordCard}>
        <h2 className={styles.title}>Forgot Password?</h2>
        <p className={styles.subtitle}>Enter your email to reset your password</p>

        <form className={styles.form}>
          <div className={styles.inputGroup}>
            <label htmlFor="email" className={styles.label}>Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              className={styles.input}
              placeholder="Enter your email"
              required
            />
          </div>

          <button type="submit" className={styles.button}>
            Send Reset Link
          </button>
        </form>

        <div className={styles.footer}>
          <p><Link to="/login" className={styles.link}>Back to Login</Link></p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
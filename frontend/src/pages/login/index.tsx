// frontend/src/pages/login/index.tsx
import React from 'react';
import styles from './styles.module.css';
import { LoginForm } from '../../components/auth/login-form';
import { SocialLogin } from '../../components/auth/social-login';
import { Link } from 'react-router-dom';

const LoginPage: React.FC = () => {
  return (
    <div className={styles.loginContainer}>
      <div className={styles.loginCard}>
        <h2 className={styles.title}>Welcome Back</h2>
        <p className={styles.subtitle}>Sign in to your account to continue</p>

        <LoginForm />

        <div className={styles.divider}>
          <span>or continue with</span>
        </div>

        <SocialLogin />

        <div className={styles.footer}>
          <p>Don't have an account? <Link to="/signup" className={styles.link}>Sign up</Link></p>
          <p><Link to="/forgot-password" className={styles.link}>Forgot password?</Link></p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
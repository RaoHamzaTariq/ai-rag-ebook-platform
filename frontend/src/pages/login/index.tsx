// frontend/src/pages/login/index.tsx
import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';
import { LoginForm } from '../../components/auth/login-form';

const LoginPage: React.FC = () => {
  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className={styles.loginContainer}>
        <div className={styles.loginCard}>
          <h2 className={styles.title}>Welcome Back</h2>
          <p className={styles.subtitle}>Sign in to your account to continue</p>

          <LoginForm />

          <div className={styles.footer}>
            <p>Don't have an account? <Link to="/signup" className={styles.link}>Sign up</Link></p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default LoginPage;
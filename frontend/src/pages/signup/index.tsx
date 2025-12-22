// frontend/src/pages/signup/index.tsx
import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';
import { SignupForm } from '../../components/auth/signup-form';

const SignupPage: React.FC = () => {
  return (
    <Layout title="Sign Up" description="Create an account">
      <div className={styles.signupContainer}>
        <div className={styles.signupCard}>
          <h2 className={styles.title}>Create Account</h2>
          <p className={styles.subtitle}>Sign up to get started with our service</p>

          <SignupForm />

          <div className={styles.footer}>
            <p>Already have an account? <Link to="/login" className={styles.link}>Sign in</Link></p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage;
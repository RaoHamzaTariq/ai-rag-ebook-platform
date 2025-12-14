// frontend/src/pages/signup/index.tsx
import React from 'react';
import styles from './styles.module.css';
import { SignupForm } from '../../components/auth/signup-form';
import { SocialLogin } from '../../components/auth/social-login';
import { Link } from 'react-router-dom';

const SignupPage: React.FC = () => {
  return (
    <div className={styles.signupContainer}>
      <div className={styles.signupCard}>
        <h2 className={styles.title}>Create Account</h2>
        <p className={styles.subtitle}>Sign up to get started with our service</p>

        <SignupForm />

        <div className={styles.divider}>
          <span>or continue with</span>
        </div>

        <SocialLogin />

        <div className={styles.footer}>
          <p>Already have an account? <Link to="/login" className={styles.link}>Sign in</Link></p>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
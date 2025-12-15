// frontend/src/components/auth/social-login/index.tsx
import React from 'react';
import styles from './styles.module.css';

export const SocialLogin: React.FC = () => {
  const handleGoogleLogin = () => {
    // Placeholder for Google login
    console.log('Google login clicked');
  };

  const handleGitHubLogin = () => {
    // Placeholder for GitHub login
    console.log('GitHub login clicked');
  };

  return (
    <div className={styles.socialLoginContainer}>
      <button
        onClick={handleGoogleLogin}
        className={`${styles.socialButton} ${styles.googleButton}`}
      >
        <span className={styles.buttonIcon}>G</span>
        Continue with Google
      </button>
      <button
        onClick={handleGitHubLogin}
        className={`${styles.socialButton} ${styles.githubButton}`}
      >
        <span className={styles.buttonIcon}>GH</span>
        Continue with GitHub
      </button>
    </div>
  );
};
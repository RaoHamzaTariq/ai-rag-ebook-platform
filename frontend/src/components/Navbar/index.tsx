import React from 'react';
import styles from './styles.module.css';

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.navInner}>

        {/* Left: Logo / Title */}
        <a href="/" className={styles.logo}>
          Humanoid Robotics
        </a>

        {/* Right: Navigation Links */}
        <div className={styles.navLinks}>
          <a href="/docs/intro" className={styles.navItem}>Syllabus</a>
          <a href="https://github.com/RaoHamzaTariq/ai-rag-ebook-platform/tree/main/frontend" className={styles.navItem}>GitHub</a>
        </div>

      </div>
    </nav>
  );
}

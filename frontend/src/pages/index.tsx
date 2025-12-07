import React from 'react';
import styles from './index.module.css';
import Navbar from '@site/src/components/Navbar';



// Mock site config (replacing Docusaurus context)
const siteConfig = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Mastering the fusion of AI and the physical world, from real-time control to cognitive humanoid action.',
};

// Chapter data
const chapters = [
  {
    id: '01',
    title: 'Chapter 1: Foundations & Sensing',
    description: 'The principles of Embodied Intelligence, Physical Laws, Real-Time Systems, and internal/external sensing (IMUs, LIDAR, Cameras).',
    link: '/docs/01-foundations',
    icon: '⚡',
  },
  {
    id: '02',
    title: 'Chapter 2: The Robotic Nervous System (ROS 2)',
    description: 'Architecture of Nodes, Topics, Services, and Actions, defining the communication framework for all robot components.',
    link: '/docs/02-ros2',
    icon: '🔗',
  },
  {
    id: '03',
    title: 'Chapter 3: The Digital Twin (Simulation)',
    description: 'Mastering physics simulation with Gazebo and high-fidelity visualization techniques for Sim-to-Real transfer.',
    link: '/docs/03-simulation',
    icon: '🌐',
  },
  {
    id: '04',
    title: 'Chapter 4: Advanced AI & Control (NVIDIA Isaac)',
    description: 'GPU-accelerated pipelines for Visual SLAM and synthetic data generation using Isaac Sim and Omniverse.',
    link: '/docs/04-isaac',
    icon: '🧠',
  },
  {
    id: '05',
    title: 'Chapter 5: Humanoid Action & VLA Integration',
    description: 'Complex challenges of Bipedal Locomotion (ZMP), Manipulation, and Cognitive Reasoning with Vision Language Models.',
    link: '/docs/05-humanoid',
    icon: '🤖',
  },
];

const ChapterCard = ({ chapter }) => (
  <a href={chapter.link} className={styles.chapterCard}>
    <div>
      <div className={styles.chapterIcon}>{chapter.icon}</div>
      <h3 className={styles.chapterTitle}>{chapter.title}</h3>
      <p className={styles.chapterDescription}>{chapter.description}</p>
    </div>
    <span className={styles.chapterStart}>Start Chapter →</span>
  </a>
);

function HomepageHeader() {
  return (
    <header className={styles.header}>
      <div className={styles.headerOverlay}></div>

      <div className={styles.headerInner}>
        <h1 className={styles.siteTitle}>{siteConfig.title}</h1>
        <p className={styles.siteTagline}>{siteConfig.tagline}</p>

        <div className={styles.headerButtons}>
          <a href="/docs/01-foundations" className={styles.primaryButton}>
            Start Reading: Chapter 1 →
          </a>

          <a href="/docs/intro" className={styles.secondaryButton}>
            View Syllabus
          </a>
        </div>
      </div>
    </header>
  );
}

function HomepageChapters() {
  return (
    <section className={styles.chaptersSection}>
      <h2 className={styles.sectionTitle}>The Curriculum</h2>

      <div className={styles.chapterGrid}>
        {chapters.map((chapter) => (
          <ChapterCard key={chapter.id} chapter={chapter} />
        ))}
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <div className={styles.page}>
      <Navbar />        {/* ← NEW */}
      <HomepageHeader />
      <main>
        <HomepageChapters />

        <div className={styles.footerNote}>
          <p>
            This interactive text covers the essential stacks for modern humanoid robotics, including ROS 2, Real-Time Control,
            Physics Simulation, and Vision Language Model (VLM) integration.
          </p>
        </div>
      </main>
    </div>
  );
}

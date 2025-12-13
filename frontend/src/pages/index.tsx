import React, { JSX } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

// Chapter data
const chapters = [
  {
    id: '01',
    title: 'Foundations & Sensing',
    number: 'Chapter 1',
    description: 'The principles of Embodied Intelligence, Physical Laws, Real-Time Systems, and internal/external sensing (IMUs, LIDAR, Cameras).',
    link: '/docs/category/foundations',
    icon: '⚡',
    color: '#6366f1',
  },
  {
    id: '02',
    title: 'ROS 2 Nervous System',
    number: 'Chapter 2',
    description: 'Architecture of Nodes, Topics, Services, and Actions, defining the communication framework for all robot components.',
    link: '/docs/category/the-robotic-nervous-system-ros-2',
    icon: '🔗',
    color: '#8b5cf6',
  },
  {
    id: '03',
    title: 'Digital Twin & Simulation',
    number: 'Chapter 3',
    description: 'Mastering physics simulation with Gazebo and high-fidelity visualization techniques for Sim-to-Real transfer.',
    link: '/docs/category/the-digital-twin-simulation',
    icon: '🌐',
    color: '#06b6d4',
  },
  {
    id: '04',
    title: 'Advanced AI & Control',
    number: 'Chapter 4',
    description: 'GPU-accelerated pipelines for Visual SLAM and synthetic data generation using Isaac Sim and Omniverse.',
    link: '/docs/category/advanced-ai--control-nvidia-isaac',
    icon: '🧠',
    color: '#10b981',
  },
  {
    id: '05',
    title: 'Humanoid Action & VLA',
    number: 'Chapter 5',
    description: 'Complex challenges of Bipedal Locomotion (ZMP), Manipulation, and Cognitive Reasoning with Vision Language Models.',
    link: '/docs/category/humanoid-action--vla-integration',
    icon: '🤖',
    color: '#f59e0b',
  },
];

const ChapterCard = ({ chapter }) => (
  <Link to={chapter.link} className={styles.chapterCard} style={{ '--chapter-color': chapter.color } as React.CSSProperties}>
    <div className={styles.chapterIcon}>{chapter.icon}</div>
    <div className={styles.chapterContent}>
      <span className={styles.chapterNumber}>{chapter.number}</span>
      <h3 className={styles.chapterTitle}>{chapter.title}</h3>
      <p className={styles.chapterDescription}>{chapter.description}</p>
    </div>
    <div className={styles.chapterArrow}>→</div>
  </Link>
);

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroOverlay}></div>
      <div className={styles.heroContent}>
        <h1 className={styles.heroTitle}>
          <span className={styles.heroTitleGradient}>{siteConfig.title}</span>
        </h1>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>

        <div className={styles.heroButtons}>
          <Link className={styles.primaryButton} to="/intro">
            <span>🚀 Start Learning</span>
          </Link>
          <Link className={styles.secondaryButton} to="/category/foundations">
            <span>📖 Read Chapter 1</span>
          </Link>
        </div>

        <div className={styles.heroFeatures}>
          <div className={styles.heroFeature}>
            <span className={styles.featureIcon}>⚡</span>
            <span>Real-Time Control</span>
          </div>
          <div className={styles.heroFeature}>
            <span className={styles.featureIcon}>🤖</span>
            <span>Humanoid Robotics</span>
          </div>
          <div className={styles.heroFeature}>
            <span className={styles.featureIcon}>🧠</span>
            <span>AI Integration</span>
          </div>
        </div>
      </div>
    </header>
  );
}

function HomepageChapters() {
  return (
    <section className={styles.chaptersSection}>
      <div className={styles.container}>
        <h2 className={styles.sectionTitle}>
          <span className={styles.sectionTitleGradient}>The Curriculum</span>
        </h2>
        <p className={styles.sectionSubtitle}>
          A comprehensive journey from foundational physics to advanced humanoid AI systems
        </p>

        <div className={styles.chapterGrid}>
          {chapters.map((chapter) => (
            <ChapterCard key={chapter.id} chapter={chapter} />
          ))}
        </div>
      </div>
    </section>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.featuresSection}>
      <div className={styles.container}>
        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIconLarge}>🎯</div>
            <h3>Practical & Hands-On</h3>
            <p>Learn by building real robotic systems with ROS 2, Gazebo, and NVIDIA Isaac Sim</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIconLarge}>🚀</div>
            <h3>Industry-Standard Tools</h3>
            <p>Master the same tools used by leading robotics companies and research labs</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIconLarge}>💡</div>
            <h3>AI-Powered Learning</h3>
            <p>Interactive AI assistant helps you understand complex concepts and answer questions</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`${siteConfig.title}`}
      description="An AI-Native Textbook for Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <HomepageChapters />
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

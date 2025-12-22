import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-Native Textbook for the Future of Embodied Intelligence',
  favicon: 'img/favicon.ico',

  // Future flags
  future: {
    v4: true,
  },

  // Production URL
  url: 'https://physical-ai-ebook.com',
  baseUrl: '/',

  // Organization info
  organizationName: 'BI Structure',
  projectName: 'physical-ai-ebook',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Internationalization
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: './docs',
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
          // Remove edit links or customize to your repo
          editUrl: undefined,
          showLastUpdateTime: true,
          breadcrumbs: true,
        },
        blog: false, // Disable blog if not needed
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [],

  themeConfig: {
    // Social card
    image: 'img/social-card.jpg',

    // Color mode
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },

    // Navbar configuration
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
        srcDark: 'img/logo-dark.svg',
        width: 32,
        height: 32,
      },
      hideOnScroll: false,
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: '📚 Textbook',
        },
        {
          to: '/docs/intro',
          label: '🚀 Get Started',
          position: 'left',
        },
        {
          type: 'search',
          position: 'right',
        },
        {
          type: 'html',
          position: 'right',
          value: '<div id="navbar-auth-root"></div>',
        },
        {
          href: 'https://github.com/your-org/physical-ai-ebook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    // Footer configuration
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Chapter 1: Foundations',
              to: '/docs/category/foundations',
            },
            {
              label: 'Chapter 5: Humanoid Action',
              to: '/docs/category/humanoid-action--vla-integration',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/rolling/',
            },
            {
              label: 'NVIDIA Isaac Sim',
              href: 'https://developer.nvidia.com/isaac-sim',
            },
            {
              label: 'Gazebo',
              href: 'https://gazebosim.org/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-org/physical-ai-ebook',
            },
            {
              label: 'Discord',
              href: 'https://discord.gg/your-server',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/your-handle',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
    },

    // Prism syntax highlighting
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'json', 'cpp'],
    },

    // Algolia search (optional - configure if you have Algolia)
    // algolia: {
    //   appId: 'YOUR_APP_ID',
    //   apiKey: 'YOUR_SEARCH_API_KEY',
    //   indexName: 'physical-ai-ebook',
    // },

    // Announcement bar (optional)
    announcementBar: {
      id: 'ai_assistant',
      content:
        '🤖 <strong>New!</strong> Try our AI assistant - select any text and click "Summarize" or ask questions in the chat widget!',
      backgroundColor: '#6366f1',
      textColor: '#ffffff',
      isCloseable: true,
    },

    // Table of contents
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
  } satisfies Preset.ThemeConfig,

  customFields: {
    betterAuthUrl: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3001",
    backendUrl: process.env.REACT_APP_BACKEND_URL || "http://localhost:8000",
  },
};

export default config;

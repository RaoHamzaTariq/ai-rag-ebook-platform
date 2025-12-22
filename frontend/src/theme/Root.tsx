import React from 'react';
import ChatWidget from '../components/ChatWidget/index';

import { AuthProvider } from '../contexts/AuthContext';
import NavbarAuth from '../components/Navbar/NavbarAuth';
import { useEffect } from 'react';
import { createRoot } from 'react-dom/client';

// Default implementation, that you can customize
function Root({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Mount NavbarAuth component into the navbar placeholder
    const navbarAuthRoot = document.getElementById('navbar-auth-root');
    if (navbarAuthRoot && !navbarAuthRoot.hasChildNodes()) {
      const root = createRoot(navbarAuthRoot);
      root.render(
        <AuthProvider>
          <NavbarAuth />
        </AuthProvider>
      );
    }
  }, []);

  return (
    <AuthProvider>
      {children}
      <ChatWidget />
    </AuthProvider>
  );
}

export default Root;
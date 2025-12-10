import React from 'react';
import ChatWidget from '../components/ChatWidget/index';

// Default implementation, that you can customize
function Root({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}

export default Root;
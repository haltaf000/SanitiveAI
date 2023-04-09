import React from 'react';
import Header from './Header';
import Footer from './Footer';

const BaseLayout = ({ children, isLoggedIn, onToggleLogin }) => {
  return (
    <>
      <Header isLoggedIn={isLoggedIn} onToggleLogin={onToggleLogin} />
      <main>{children}</main>
      <Footer />
    </>
  );
};

export default BaseLayout;
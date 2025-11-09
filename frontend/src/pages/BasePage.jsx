import React, { useState } from 'react';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import './BasePage.css';

function BasePage({ children }) {
  const [isNavVisible, setIsNavVisible] = useState(false);

  const toggleNav = () => {
    setIsNavVisible(!isNavVisible);
  };

  return (
      <div className={`content-wrapper`}>
        <NavBar />
        <main className="main-content">
          {children}
        </main>
        <Footer />
      </div>
  );
}

export default BasePage;

import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>Zenos Food</h3>
          <p>O melhor da gastronomia local</p>
        </div>
        
        <div className="footer-section">
          <h4>Links Úteis</h4>
          <Link to="/about">Sobre</Link>
          <Link to="/contact">Contato</Link>
          <Link to="/privacy">Privacidade</Link>
        </div>
        
        <div className="footer-section">
          <h4>Restaurantes</h4>
          <Link to="/partners">Seja Parceiro</Link>
          <Link to="/restaurants">Encontre Restaurantes</Link>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} Zenos Food. Todos os direitos reservados.</p>
      </div>
    </footer>
  );
}

export default Footer;

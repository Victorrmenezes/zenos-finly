import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>Zenos Financeiro</h3>
          <p>Vida financeira Zen!</p>
        </div>
        
        <div className="footer-section">
          <h4>Links Úteis</h4>
          <Link to="/contact">Contato</Link>
        </div>
        
        <div className="footer-section">
          <h4>Financeiro</h4>
          <Link to="/partners">Seja Parceiro</Link>
          <Link to="/transactions">Minhas Transações</Link>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} Zenos Financeiro. Todos os direitos reservados.</p>
      </div>
    </footer>
  );
}

export default Footer;

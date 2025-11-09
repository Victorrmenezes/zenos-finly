import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './NavBar.css';

function NavBar() {
  const { user, handleLogout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-logo-group">
        <Link to="/" className="navbar-logo">Zenos</Link>
      </div>
      {/* <div className="navbar-search">
        <input
          type="search"
          placeholder="Buscar restaurantes..."
          className="search-input"
        /></div> */}
      <div className="navbar-menu-group">
        <Link to="/" className="navbar-menu-item">Dashboard</Link>
        <Link to="/credit-card" className="navbar-menu-item">Cartão de Crédito</Link>
        {/* <Link to="/contacts" className="navbar-menu-item">CONTATOS</Link> */}
      </div>
      <div className="navbar-auth-group">
        {!user ? (
          <>
            <Link to="/login" className="navbar-menu-item btn-link">SIGN IN</Link>
              </>
        ) : (
          <>
            <Link to="/profile" className="navbar-menu-item">
              {user.first_name || 'Perfil'}
            </Link>
            <button onClick={handleLogout} className="navbar-menu-item btn-link">
              Sair
            </button>
          </>
        )}
      </div>
    </nav>
  );
}

export default NavBar;

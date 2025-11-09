import React from 'react';
import '../pages/LoginPage.css';
import LoginForm from '../components/LoginForm';

function LoginPage() {
  return (
    <div className="auth-page">
      <div className="auth-hero" aria-hidden="true">
        <div className="hero-overlay">
          <div className="hero-content">
            <h1>Zenos Financeiro</h1>
            <p>
              Controle sua vida financeira e continue Zen.
            </p>
          </div>
        </div>
      </div>

      <div className="auth-panel">
        <div className="auth-container">

          <h2 className="auth-title">Sign in</h2>

          <div className="socials">
            <button className="btn social google" type="button">Continue com Google</button>
            <button className="btn social twitter" type="button">Continue com Facebook</button>
          </div>

          <div className="divider"><span>OR</span></div>

          <LoginForm redirectUrl="/profile" />
        </div>
      </div>
    </div>
  );
}

export default LoginPage;

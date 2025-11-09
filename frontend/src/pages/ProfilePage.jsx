import React from 'react';
import BasePage from './BasePage';
import { useAuth } from '../context/AuthContext';

function ProfilePage() {
  const { user } = useAuth();
  return (
    <BasePage>
      <h1>Perfil</h1>
      {user ? (
        <div>
          <p>Usuário: {user.username}</p>
          <p>Email: {user.email}</p>
        </div>
      ) : (
        <p>Não autenticado.</p>
      )}
    </BasePage>
  );
}

export default ProfilePage;

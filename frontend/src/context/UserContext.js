// frontend/src/context/UserContext.js

import React, { createContext, useContext, useState } from "react";

/**
 * Contexto global para autenticação ou identificação do usuário.
 * Permite setar e acessar o usuário logado em qualquer parte da aplicação.
 */
const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [usuario, setUsuario] = useState(null);

  return (
    <UserContext.Provider value={{ usuario, setUsuario }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);

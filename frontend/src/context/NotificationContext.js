// frontend/src/context/NotificationContext.js

import React, { createContext, useContext, useState } from "react";

/**
 * Contexto global para notificações rápidas (success, error, info).
 * Use para exibir mensagens em banners, toasts ou snackbars.
 */
const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notificacao, setNotificacao] = useState(null);

  // Exemplo de notificação: { tipo: "success", mensagem: "Formulário enviado!" }
  const showNotification = (tipo, mensagem, timeout = 4000) => {
    setNotificacao({ tipo, mensagem });
    setTimeout(() => setNotificacao(null), timeout);
  };

  return (
    <NotificationContext.Provider value={{ notificacao, showNotification }}>
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotification = () => useContext(NotificationContext);

// frontend/src/context/NotificationContext.js
import React, { createContext, useContext, useState } from "react";

const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notificacao, setNotificacao] = useState(null);

  const showNotification = (tipo, mensagem, timeout = 4000) => {
    setNotificacao({ tipo, mensagem });
    setTimeout(() => setNotificacao(null), timeout);
  };

  return (
    <NotificationContext.Provider value={{ notificacao, showNotification }}>
      {notificacao && (
        <div className="mensagem">
          <strong>{notificacao.tipo?.toUpperCase()}:</strong> {notificacao.mensagem}
        </div>
      )}
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotification = () => useContext(NotificationContext);

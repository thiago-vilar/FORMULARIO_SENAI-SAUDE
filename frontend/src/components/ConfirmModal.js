// frontend/src/components/ConfirmModal.js

import React from "react";

const ConfirmModal = ({ isOpen, title, message, onConfirm, onCancel }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>{title || "Confirmação"}</h3>
        <p>{message}</p>
        <div className="modal-actions">
          <button type="button" onClick={onConfirm} className="modal-confirm-btn">
            Confirmar
          </button>
          <button type="button" onClick={onCancel} className="modal-cancel-btn">
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;

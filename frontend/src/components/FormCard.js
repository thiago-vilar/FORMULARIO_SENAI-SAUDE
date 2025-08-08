// frontend/src/components/FormCard.js
import React from "react";
import "../styles/FormCard.css";

const FormCard = ({ title, description, children, onSubmit }) => (
  <div className="form-card">
    <form className="form-card-content" onSubmit={onSubmit}>
      <div className="form-card-header">
        <h2 className="form-card__title">{title}</h2>
        {description && <p className="form-card__desc">{description}</p>}
      </div>
      <div className="form-card-body">{children}</div>
    </form>
  </div>
);

export default FormCard;

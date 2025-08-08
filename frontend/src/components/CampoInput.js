// frontend/src/components/CampoInput.js
import React from "react";

const CampoInput = ({
  label,
  type = "text",
  name,
  value,
  onChange,
  required = false,
  min,
  max,
  step,
  placeholder,
  ...rest
}) => (
  <div className="campo-input">
    <label>
      {label}
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        min={min}
        max={max}
        step={step}
        placeholder={placeholder}
        {...rest}
      />
    </label>
  </div>
);

export default CampoInput;

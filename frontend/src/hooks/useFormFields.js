// frontend/src/hooks/useFormFields.js

import { useState } from "react";

/**
 * Hook genérico para controlar os campos de um formulário dinâmico.
 * Ideal para uso com formulários SENAI-Saúde, permite adicionar, remover e atualizar campos.
 */
export default function useFormFields(initialFields = []) {
  const [fields, setFields] = useState(initialFields);

  const handleFieldChange = (index, key, value) => {
    setFields((prev) =>
      prev.map((field, idx) =>
        idx === index ? { ...field, [key]: value } : field
      )
    );
  };

  const addField = (newField) => setFields([...fields, newField]);

  const removeField = (index) => {
    setFields((prev) => prev.filter((_, idx) => idx !== index));
  };

  const resetFields = () => setFields(initialFields);

  return { fields, setFields, handleFieldChange, addField, removeField, resetFields };
}

import { useState, useEffect } from 'react';
import '../styles/crud.css';

export default function CrudPage({
  title,
  icon,
  service,
  columns,
  formFields,
  renderExtraInfo,
  renderActions,
  initialFormData = {},
}) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState(initialFormData);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    try {
      setLoading(true);
      const data = await service.getAll();
      setItems(data.results || data);
    } catch (err) {
      console.error('Error loading items:', err);
    } finally {
      setLoading(false);
    }
  };

  const openCreateModal = () => {
    setEditingItem(null);
    setFormData(initialFormData);
    setError('');
    setShowModal(true);
  };

  const openEditModal = (item) => {
    setEditingItem(item);
    const data = {};
    formFields.forEach((field) => {
      data[field.name] = item[field.name] ?? '';
    });
    setFormData(data);
    setError('');
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingItem(null);
    setFormData(initialFormData);
    setError('');
  };

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? e.target.checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    try {
      // Clean up empty values for optional fields
      const cleanedData = { ...formData };
      formFields.forEach((field) => {
        if (cleanedData[field.name] === '' && !field.required) {
          cleanedData[field.name] = null;
        }
        if (field.type === 'number' && cleanedData[field.name]) {
          cleanedData[field.name] = Number(cleanedData[field.name]);
        }
      });

      if (editingItem) {
        await service.update(editingItem.id, cleanedData);
      } else {
        await service.create(cleanedData);
      }
      closeModal();
      loadItems();
    } catch (err) {
      const errorData = err.response?.data;
      if (errorData) {
        const messages = Object.entries(errorData)
          .map(([key, value]) => {
            const fieldLabel = formFields.find((f) => f.name === key)?.label || key;
            return `${fieldLabel}: ${Array.isArray(value) ? value.join(', ') : value}`;
          })
          .join('\n');
        setError(messages);
      } else {
        setError('Ошибка сохранения');
      }
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (item) => {
    if (!confirm(`Удалить этот элемент?`)) return;

    try {
      await service.delete(item.id);
      loadItems();
    } catch (err) {
      alert('Ошибка удаления');
    }
  };

  const renderFieldInput = (field) => {
    const commonProps = {
      id: field.name,
      name: field.name,
      value: formData[field.name] ?? '',
      onChange: handleInputChange,
      required: field.required,
      disabled: saving,
    };

    switch (field.type) {
      case 'select':
        return (
          <select {...commonProps}>
            <option value="">-- Выберите --</option>
            {field.options?.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        );
      case 'textarea':
        return <textarea {...commonProps} rows={3} />;
      case 'checkbox':
        return (
          <input
            type="checkbox"
            id={field.name}
            name={field.name}
            checked={formData[field.name] || false}
            onChange={handleInputChange}
            disabled={saving}
          />
        );
      case 'date':
        return <input type="date" {...commonProps} />;
      case 'number':
        return <input type="number" {...commonProps} min={field.min} max={field.max} />;
      default:
        return <input type="text" {...commonProps} />;
    }
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner"></div>
        <p>Загрузка...</p>
      </div>
    );
  }

  return (
    <div className="crud-page">
      <div className="page-header">
        <h1>
          {icon} {title}
        </h1>
        <button className="btn-primary" onClick={openCreateModal}>
          + Добавить
        </button>
      </div>

      {renderExtraInfo && <div className="extra-info">{renderExtraInfo()}</div>}

      {renderActions && <div className="page-actions">{renderActions()}</div>}

      <div className="table-container">
        <table>
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key}>{col.label}</th>
              ))}
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={columns.length + 1} className="empty-message">
                  Нет данных
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id}>
                  {columns.map((col) => (
                    <td key={col.key}>
                      {col.render ? col.render(item) : item[col.key]}
                    </td>
                  ))}
                  <td className="actions-cell">
                    <button className="btn-edit" onClick={() => openEditModal(item)}>
                      ✏️
                    </button>
                    <button className="btn-delete" onClick={() => handleDelete(item)}>
                      🗑️
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingItem ? 'Редактирование' : 'Создание'}</h2>
              <button className="modal-close" onClick={closeModal}>
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className="modal-form">
              {error && <div className="form-error">{error}</div>}

              {formFields.map((field) => (
                <div
                  key={field.name}
                  className={`form-group ${field.type === 'checkbox' ? 'checkbox-group' : ''}`}
                >
                  <label htmlFor={field.name}>
                    {field.label}
                    {field.required && <span className="required">*</span>}
                  </label>
                  {renderFieldInput(field)}
                </div>
              ))}

              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={closeModal}>
                  Отмена
                </button>
                <button type="submit" className="btn-primary" disabled={saving}>
                  {saving ? 'Сохранение...' : 'Сохранить'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}


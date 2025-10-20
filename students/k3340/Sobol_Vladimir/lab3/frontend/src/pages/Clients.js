import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  Space, 
  message, 
  Popconfirm,
  Card,
  InputNumber
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { clientsAPI } from '../services/api';

const Clients = () => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingClient, setEditingClient] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    try {
      setLoading(true);
      const response = await clientsAPI.getAll();
      setClients(response.data.results || response.data);
    } catch (error) {
      message.error('Ошибка загрузки клиентов');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingClient(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (client) => {
    setEditingClient(client);
    form.setFieldsValue(client);
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await clientsAPI.delete(id);
      message.success('Клиент удален');
      loadClients();
    } catch (error) {
      message.error('Ошибка удаления клиента');
    }
  };

  const handleSubmit = async (values) => {
    try {
      if (editingClient) {
        await clientsAPI.update(editingClient.id, values);
        message.success('Клиент обновлен');
      } else {
        await clientsAPI.create(values);
        message.success('Клиент создан');
      }
      setModalVisible(false);
      loadClients();
    } catch (error) {
      message.error('Ошибка сохранения клиента');
    }
  };

  const columns = [
    {
      title: 'Паспорт',
      dataIndex: 'passport_number',
      key: 'passport_number',
    },
    {
      title: 'Фамилия',
      dataIndex: 'last_name',
      key: 'last_name',
    },
    {
      title: 'Имя',
      dataIndex: 'first_name',
      key: 'first_name',
    },
    {
      title: 'Отчество',
      dataIndex: 'patronymic',
      key: 'patronymic',
    },
    {
      title: 'Город',
      dataIndex: 'city',
      key: 'city',
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button 
            type="primary" 
            size="small" 
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Редактировать
          </Button>
          <Popconfirm
            title="Удалить клиента?"
            onConfirm={() => handleDelete(record.id)}
            okText="Да"
            cancelText="Нет"
          >
            <Button 
              danger 
              size="small" 
              icon={<DeleteOutlined />}
            >
              Удалить
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card>
        <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
          <h2>Управление клиентами</h2>
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={handleAdd}
          >
            Добавить клиента
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={clients || []}
          loading={loading}
          rowKey="id"
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `Всего: ${total} клиентов`,
          }}
        />
      </Card>

      <Modal
        title={editingClient ? 'Редактировать клиента' : 'Добавить клиента'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="passport_number"
            label="Номер паспорта"
            rules={[{ required: true, message: 'Введите номер паспорта' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="last_name"
            label="Фамилия"
            rules={[{ required: true, message: 'Введите фамилию' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="first_name"
            label="Имя"
            rules={[{ required: true, message: 'Введите имя' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="patronymic"
            label="Отчество"
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="city"
            label="Город"
            rules={[{ required: true, message: 'Введите город' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingClient ? 'Обновить' : 'Создать'}
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                Отмена
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Clients;

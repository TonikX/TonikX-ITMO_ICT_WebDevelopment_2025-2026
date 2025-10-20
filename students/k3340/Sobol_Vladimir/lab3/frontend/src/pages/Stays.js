import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Button, 
  Modal, 
  Form, 
  Select, 
  DatePicker, 
  Space, 
  message, 
  Popconfirm,
  Card,
  Tag
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { staysAPI, clientsAPI, roomsAPI } from '../services/api';

const { Option } = Select;

const Stays = () => {
  const [stays, setStays] = useState([]);
  const [clients, setClients] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingStay, setEditingStay] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [staysRes, clientsRes, roomsRes] = await Promise.all([
        staysAPI.getAll(),
        clientsAPI.getAll(),
        roomsAPI.getAll()
      ]);
      setStays(staysRes.data.results || staysRes.data);
      setClients(clientsRes.data.results || clientsRes.data);
      setRooms(roomsRes.data.results || roomsRes.data);
    } catch (error) {
      message.error('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingStay(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (stay) => {
    setEditingStay(stay);
    form.setFieldsValue({
      ...stay,
      check_in: stay.check_in ? dayjs(stay.check_in) : null,
      check_out: stay.check_out ? dayjs(stay.check_out) : null,
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await staysAPI.delete(id);
      message.success('Проживание удалено');
      loadData();
    } catch (error) {
      message.error('Ошибка удаления проживания');
    }
  };

  const handleSubmit = async (values) => {
    try {
      const data = {
        ...values,
        check_in: values.check_in.format('YYYY-MM-DD'),
        check_out: values.check_out ? values.check_out.format('YYYY-MM-DD') : null,
      };

      if (editingStay) {
        await staysAPI.update(editingStay.id, data);
        message.success('Проживание обновлено');
      } else {
        await staysAPI.create(data);
        message.success('Проживание создано');
      }
      setModalVisible(false);
      loadData();
    } catch (error) {
      message.error('Ошибка сохранения проживания');
    }
  };

  const columns = [
    {
      title: 'Клиент',
      dataIndex: 'client_name',
      key: 'client_name',
    },
    {
      title: 'Номер',
      dataIndex: 'room_number',
      key: 'room_number',
    },
    {
      title: 'Заселение',
      dataIndex: 'check_in',
      key: 'check_in',
    },
    {
      title: 'Выезд',
      dataIndex: 'check_out',
      key: 'check_out',
      render: (value) => value || <Tag color="green">Проживает</Tag>,
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
            title="Удалить проживание?"
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
          <h2>Управление проживаниями</h2>
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={handleAdd}
          >
            Добавить проживание
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={stays || []}
          loading={loading}
          rowKey="id"
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `Всего: ${total} проживаний`,
          }}
        />
      </Card>

      <Modal
        title={editingStay ? 'Редактировать проживание' : 'Добавить проживание'}
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
            name="client"
            label="Клиент"
            rules={[{ required: true, message: 'Выберите клиента' }]}
          >
            <Select>
              {clients.map(client => (
                <Option key={client.id} value={client.id}>
                  {client.last_name} {client.first_name} ({client.passport_number})
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="room"
            label="Номер"
            rules={[{ required: true, message: 'Выберите номер' }]}
          >
            <Select>
              {rooms.map(room => (
                <Option key={room.id} value={room.id}>
                  №{room.number} ({room.room_type_display})
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="check_in"
            label="Дата заселения"
            rules={[{ required: true, message: 'Выберите дату заселения' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="check_out"
            label="Дата выезда"
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingStay ? 'Обновить' : 'Создать'}
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

export default Stays;

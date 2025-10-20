import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  InputNumber, 
  Select, 
  Space, 
  message, 
  Popconfirm,
  Card,
  Tag,
  DatePicker
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { roomsAPI } from '../services/api';

const { Option } = Select;

const Rooms = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingRoom, setEditingRoom] = useState(null);
  const [form] = Form.useForm();
  const [freeRoomsModalVisible, setFreeRoomsModalVisible] = useState(false);
  const [freeRooms, setFreeRooms] = useState([]);
  const [selectedDate, setSelectedDate] = useState(dayjs());

  useEffect(() => {
    loadRooms();
  }, []);

  const loadRooms = async () => {
    try {
      setLoading(true);
      const response = await roomsAPI.getAll();
      setRooms(response.data.results || response.data);
    } catch (error) {
      message.error('Ошибка загрузки номеров');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingRoom(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (room) => {
    setEditingRoom(room);
    form.setFieldsValue({
      ...room,
      daily_rate: room.daily_rate
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await roomsAPI.delete(id);
      message.success('Номер удален');
      loadRooms();
    } catch (error) {
      message.error('Ошибка удаления номера');
    }
  };

  const handleSubmit = async (values) => {
    try {
      if (editingRoom) {
        await roomsAPI.update(editingRoom.id, values);
        message.success('Номер обновлен');
      } else {
        await roomsAPI.create(values);
        message.success('Номер создан');
      }
      setModalVisible(false);
      loadRooms();
    } catch (error) {
      message.error('Ошибка сохранения номера');
    }
  };

  const loadFreeRooms = async () => {
    try {
      const response = await roomsAPI.getFreeRooms(selectedDate.format('YYYY-MM-DD'));
      setFreeRooms(response.data.free_rooms || []);
      setFreeRoomsModalVisible(true);
    } catch (error) {
      message.error('Ошибка загрузки свободных номеров');
    }
  };

  const columns = [
    {
      title: 'Номер',
      dataIndex: 'number',
      key: 'number',
      sorter: (a, b) => a.number - b.number,
    },
    {
      title: 'Этаж',
      dataIndex: 'floor',
      key: 'floor',
      sorter: (a, b) => a.floor - b.floor,
    },
    {
      title: 'Тип',
      dataIndex: 'room_type_display',
      key: 'room_type_display',
      render: (text) => {
        const colors = {
          'Одноместный': 'blue',
          'Двухместный': 'green',
          'Трёхместный': 'orange'
        };
        return <Tag color={colors[text]}>{text}</Tag>;
      },
    },
    {
      title: 'Цена/сутки',
      dataIndex: 'daily_rate',
      key: 'daily_rate',
      render: (value) => `${value} ₽`,
      sorter: (a, b) => a.daily_rate - b.daily_rate,
    },
    {
      title: 'Телефон',
      dataIndex: 'phone',
      key: 'phone',
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
            title="Удалить номер?"
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
          <h2>Управление номерами</h2>
          <Space>
            <DatePicker
              value={selectedDate}
              onChange={setSelectedDate}
              format="DD.MM.YYYY"
            />
            <Button 
              type="default" 
              icon={<SearchOutlined />}
              onClick={loadFreeRooms}
            >
              Свободные номера
            </Button>
            <Button 
              type="primary" 
              icon={<PlusOutlined />}
              onClick={handleAdd}
            >
              Добавить номер
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={rooms || []}
          loading={loading}
          rowKey="id"
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `Всего: ${total} номеров`,
          }}
        />
      </Card>

      <Modal
        title={editingRoom ? 'Редактировать номер' : 'Добавить номер'}
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
            name="number"
            label="Номер комнаты"
            rules={[{ required: true, message: 'Введите номер комнаты' }]}
          >
            <InputNumber min={1} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="floor"
            label="Этаж"
            rules={[{ required: true, message: 'Введите этаж' }]}
          >
            <InputNumber min={1} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="room_type"
            label="Тип номера"
            rules={[{ required: true, message: 'Выберите тип номера' }]}
          >
            <Select>
              <Option value="single">Одноместный</Option>
              <Option value="double">Двухместный</Option>
              <Option value="triple">Трёхместный</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="daily_rate"
            label="Цена за сутки (₽)"
            rules={[{ required: true, message: 'Введите цену за сутки' }]}
          >
            <InputNumber min={0} step={0.01} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="phone"
            label="Телефон"
            rules={[{ required: true, message: 'Введите телефон' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingRoom ? 'Обновить' : 'Создать'}
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                Отмена
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={`Свободные номера на ${selectedDate.format('DD.MM.YYYY')}`}
        open={freeRoomsModalVisible}
        onCancel={() => setFreeRoomsModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setFreeRoomsModalVisible(false)}>
            Закрыть
          </Button>
        ]}
      >
        <Table
          dataSource={freeRooms || []}
          columns={columns.slice(0, -1)} // Убираем колонку действий
          pagination={false}
          size="small"
        />
      </Modal>
    </div>
  );
};

export default Rooms;

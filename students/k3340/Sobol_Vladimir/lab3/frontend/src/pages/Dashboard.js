import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Table, DatePicker, Button, Space, message } from 'antd';
import { 
  HomeOutlined, 
  UserOutlined, 
  CalendarOutlined, 
  TeamOutlined,
  DollarOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { roomsAPI, clientsAPI, staysAPI, employeesAPI, reportsAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalRooms: 0,
    totalClients: 0,
    activeStays: 0,
    totalEmployees: 0,
    freeRooms: 0,
    totalIncome: 0
  });
  const [freeRooms, setFreeRooms] = useState([]);
  const [recentStays, setRecentStays] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState(dayjs());

  useEffect(() => {
    loadDashboardData();
  }, [selectedDate]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Загружаем статистику
      const [roomsRes, clientsRes, staysRes, employeesRes, freeRoomsRes] = await Promise.all([
        roomsAPI.getAll(),
        clientsAPI.getAll(),
        staysAPI.getAll(),
        employeesAPI.getAll(),
        roomsAPI.getFreeRooms(selectedDate.format('YYYY-MM-DD'))
      ]);

      const staysData = staysRes.data.results || staysRes.data;
      const activeStays = staysData.filter(stay => !stay.check_out).length;
      
      setStats({
        totalRooms: (roomsRes.data.results || roomsRes.data).length,
        totalClients: (clientsRes.data.results || clientsRes.data).length,
        activeStays,
        totalEmployees: (employeesRes.data.results || employeesRes.data).length,
        freeRooms: freeRoomsRes.data.free_count,
        totalIncome: 0 // Будет загружено из отчета
      });

      setFreeRooms((freeRoomsRes.data.free_rooms || []).slice(0, 5));
      setRecentStays(staysData.slice(0, 5));

      // Загружаем доход за текущий квартал
      const currentQuarter = Math.ceil((dayjs().month() + 1) / 3);
      try {
        const reportRes = await reportsAPI.getQuarterReport(currentQuarter);
        setStats(prev => ({
          ...prev,
          totalIncome: reportRes.data.total_income
        }));
      } catch (error) {
        console.log('Не удалось загрузить отчет о доходах');
      }

    } catch (error) {
      message.error('Ошибка загрузки данных');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'Номер',
      dataIndex: 'number',
      key: 'number',
    },
    {
      title: 'Этаж',
      dataIndex: 'floor',
      key: 'floor',
    },
    {
      title: 'Тип',
      dataIndex: 'room_type_display',
      key: 'room_type_display',
    },
    {
      title: 'Цена/сутки',
      dataIndex: 'daily_rate',
      key: 'daily_rate',
      render: (value) => `${value} ₽`,
    },
  ];

  const stayColumns = [
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
      title: 'Статус',
      key: 'status',
      render: (_, record) => (
        record.check_out ? 'Выселен' : 'Проживает'
      ),
    },
  ];

  return (
    <div>
      <h1>Панель управления</h1>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Всего номеров"
              value={stats.totalRooms}
              prefix={<HomeOutlined />}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Всего клиентов"
              value={stats.totalClients}
              prefix={<UserOutlined />}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Активных проживаний"
              value={stats.activeStays}
              prefix={<CalendarOutlined />}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Сотрудников"
              value={stats.totalEmployees}
              prefix={<TeamOutlined />}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Свободных номеров"
              value={stats.freeRooms}
              prefix={<CheckCircleOutlined />}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Доход за квартал"
              value={stats.totalIncome}
              prefix={<DollarOutlined />}
              precision={2}
              suffix="₽"
              loading={loading}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card 
            title="Свободные номера" 
            extra={
              <Space>
                <DatePicker
                  value={selectedDate}
                  onChange={setSelectedDate}
                  format="DD.MM.YYYY"
                />
                <Button onClick={loadDashboardData}>Обновить</Button>
              </Space>
            }
          >
            <Table
              dataSource={freeRooms || []}
              columns={columns}
              pagination={false}
              size="small"
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Последние проживания">
            <Table
              dataSource={recentStays || []}
              columns={stayColumns}
              pagination={false}
              size="small"
              loading={loading}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;

import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Select, 
  Button, 
  Table, 
  Statistic, 
  Row, 
  Col, 
  message,
  DatePicker,
  Space
} from 'antd';
import { BarChartOutlined, ReloadOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { reportsAPI, roomsAPI, clientsAPI } from '../services/api';

const { Option } = Select;

const Reports = () => {
  const [quarterReport, setQuarterReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedQuarter, setSelectedQuarter] = useState(Math.ceil((dayjs().month() + 1) / 3));
  const [freeRoomsData, setFreeRoomsData] = useState([]);
  const [selectedDate, setSelectedDate] = useState(dayjs());

  useEffect(() => {
    loadQuarterReport();
  }, [selectedQuarter]);

  const loadQuarterReport = async () => {
    try {
      setLoading(true);
      const response = await reportsAPI.getQuarterReport(selectedQuarter);
      setQuarterReport(response.data);
    } catch (error) {
      message.error('Ошибка загрузки отчета');
    } finally {
      setLoading(false);
    }
  };

  const loadFreeRooms = async () => {
    try {
      const response = await roomsAPI.getFreeRooms(selectedDate.format('YYYY-MM-DD'));
      setFreeRoomsData(response.data.free_rooms || []);
    } catch (error) {
      message.error('Ошибка загрузки свободных номеров');
    }
  };

  const roomIncomeColumns = [
    {
      title: 'Номер',
      dataIndex: 'room',
      key: 'room',
    },
    {
      title: 'Доход (₽)',
      dataIndex: 'income',
      key: 'income',
      render: (value) => `${value}`,
    },
  ];

  const roomClientsColumns = [
    {
      title: 'Номер',
      dataIndex: 'room',
      key: 'room',
    },
    {
      title: 'Количество клиентов',
      dataIndex: 'clients',
      key: 'clients',
    },
  ];

  const floorsColumns = [
    {
      title: 'Этаж',
      dataIndex: 'floor',
      key: 'floor',
    },
    {
      title: 'Количество номеров',
      dataIndex: 'count',
      key: 'count',
    },
  ];

  const freeRoomsColumns = [
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

  return (
    <div>
      <Card>
        <h2>Отчеты и аналитика</h2>
        
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={24} md={12}>
            <Card title="Отчет по кварталу">
              <Space style={{ marginBottom: 16 }}>
                <Select
                  value={selectedQuarter}
                  onChange={setSelectedQuarter}
                  style={{ width: 120 }}
                >
                  <Option value={1}>1 квартал</Option>
                  <Option value={2}>2 квартал</Option>
                  <Option value={3}>3 квартал</Option>
                  <Option value={4}>4 квартал</Option>
                </Select>
                <Button 
                  icon={<ReloadOutlined />}
                  onClick={loadQuarterReport}
                  loading={loading}
                >
                  Обновить
                </Button>
              </Space>

              {quarterReport && (
                <div>
                  <Row gutter={16}>
                    <Col span={12}>
                      <Statistic
                        title="Общий доход"
                        value={quarterReport.total_income}
                        precision={2}
                        suffix="₽"
                      />
                    </Col>
                    <Col span={12}>
                      <Statistic
                        title="Период"
                        value={`${quarterReport.period.start} - ${quarterReport.period.end}`}
                      />
                    </Col>
                  </Row>

                  <div style={{ marginTop: 16 }}>
                    <h4>Доход по номерам</h4>
                    <Table
                      dataSource={quarterReport?.income_per_room || []}
                      columns={roomIncomeColumns}
                      pagination={false}
                      size="small"
                    />
                  </div>

                  <div style={{ marginTop: 16 }}>
                    <h4>Клиенты по номерам</h4>
                    <Table
                      dataSource={quarterReport?.clients_per_room || []}
                      columns={roomClientsColumns}
                      pagination={false}
                      size="small"
                    />
                  </div>

                  <div style={{ marginTop: 16 }}>
                    <h4>Номера по этажам</h4>
                    <Table
                      dataSource={quarterReport?.rooms_per_floor || []}
                      columns={floorsColumns}
                      pagination={false}
                      size="small"
                    />
                  </div>
                </div>
              )}
            </Card>
          </Col>

          <Col xs={24} md={12}>
            <Card title="Свободные номера">
              <Space style={{ marginBottom: 16 }}>
                <DatePicker
                  value={selectedDate}
                  onChange={setSelectedDate}
                  format="DD.MM.YYYY"
                />
                <Button 
                  icon={<BarChartOutlined />}
                  onClick={loadFreeRooms}
                >
                  Показать
                </Button>
              </Space>

              <Table
                dataSource={freeRoomsData || []}
                columns={freeRoomsColumns}
                pagination={false}
                size="small"
              />
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default Reports;

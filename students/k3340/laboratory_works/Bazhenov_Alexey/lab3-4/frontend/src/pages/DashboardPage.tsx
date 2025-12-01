import { Box, Card, CardContent, CircularProgress, Typography } from '@mui/material';
import dayjs from 'dayjs';

import { useGetEmployeesQuery, useGetFreeRoomsQuery, useGetQuarterlyReportQuery } from '../services/api';

export function DashboardPage() {
  const { data: freeRooms, isLoading: freeLoading } = useGetFreeRoomsQuery();
  const current = dayjs();
  const quarter = Math.floor(current.month() / 3) + 1;
  const year = current.year();
  const { data: report, isLoading: reportLoading } = useGetQuarterlyReportQuery({
    quarter,
    year,
  });
  const { data: employees, isLoading: employeesLoading } = useGetEmployeesQuery();

  const cards = [
    {
      title: 'Свободные номера',
      value: freeRooms?.total_free_rooms ?? '—',
      loading: freeLoading,
      description: freeRooms
        ? freeRooms.by_type.map((item) => `${item.label}: ${item.count}`).join(', ')
        : 'Нет данных',
    },
    {
      title: `Доход за Q${quarter} ${year}`,
      value: report?.total_income ? `${report.total_income.toLocaleString()} ₽` : '—',
      loading: reportLoading,
      description: report ? 'Смотрите подробный отчёт в разделе "Отчёты"' : 'Нет данных',
    },
    {
      title: 'Сотрудники уборки',
      value: employees?.length ?? '—',
      loading: employeesLoading,
      description: 'Количество активных сотрудников',
    },
  ];

  return (
    <Box
      sx={{
        display: 'grid',
        gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' },
        gap: 3,
      }}
    >
      {cards.map((card) => (
        <Card key={card.title}>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              {card.title}
            </Typography>
            {card.loading ? (
              <CircularProgress size={32} />
            ) : (
              <Typography variant="h4">{card.value}</Typography>
            )}
            <Typography variant="body2" sx={{ mt: 1.5 }}>
              {card.description}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
}


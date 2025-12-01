import {
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@mui/material';
import { skipToken } from '@reduxjs/toolkit/query';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs, { Dayjs } from 'dayjs';
import { useMemo, useState } from 'react';

import {
  useGetFreeRoomsQuery,
  useGetRoomClientsQuery,
  useGetRoomsQuery,
} from '../services/api';

const roomTypeLabels: Record<string, string> = {
  single: 'Одноместный',
  double: 'Двухместный',
  triple: 'Трёхместный',
};

export function RoomsPage() {
  const [roomType, setRoomType] = useState<string>('');
  const [floor, setFloor] = useState<string>('');
  const [historyRoomId, setHistoryRoomId] = useState<number | null>(null);
  const [startDate, setStartDate] = useState<Dayjs | null>(dayjs().subtract(7, 'day'));
  const [endDate, setEndDate] = useState<Dayjs | null>(dayjs());

  const { data: rooms } = useGetRoomsQuery({
    room_type: roomType || undefined,
    floor: floor ? Number(floor) : undefined,
  });
  const { data: freeSummary } = useGetFreeRoomsQuery();

  const roomHistoryParams = useMemo(() => {
    if (!historyRoomId || !startDate || !endDate) {
      return null;
    }
    return {
      roomId: historyRoomId,
      start: startDate.format('YYYY-MM-DD'),
      end: endDate.format('YYYY-MM-DD'),
    };
  }, [historyRoomId, startDate, endDate]);

  const { data: roomHistory } = useGetRoomClientsQuery(roomHistoryParams ?? skipToken);

  const floorsOptions = useMemo(() => {
    const unique = new Set((rooms ?? []).map((room) => room.floor));
    return Array.from(unique.values()).sort((a, b) => a - b);
  }, [rooms]);

  return (
    <Stack spacing={3}>
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Фильтры
          </Typography>
          <Stack
            direction={{ xs: 'column', md: 'row' }}
            spacing={2}
            alignItems="flex-start"
          >
            <TextField
              label="Тип номера"
              select
              fullWidth
              value={roomType}
              onChange={(event) => setRoomType(event.target.value)}
            >
              <MenuItem value="">Любой</MenuItem>
              {Object.entries(roomTypeLabels).map(([value, label]) => (
                <MenuItem key={value} value={value}>
                  {label}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label="Этаж"
              select
              fullWidth
              value={floor}
              onChange={(event) => setFloor(event.target.value)}
            >
              <MenuItem value="">Любой</MenuItem>
              {floorsOptions.map((value) => (
                <MenuItem key={value} value={value}>
                  {value}
                </MenuItem>
              ))}
            </TextField>
          </Stack>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6">Номера</Typography>
            <Typography variant="body2" color="text.secondary">
              Свободно: {freeSummary?.total_free_rooms ?? '—'}
            </Typography>
          </Stack>
          <Box sx={{ width: '100%', overflowX: 'auto' }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>№</TableCell>
                  <TableCell>Этаж</TableCell>
                  <TableCell>Тип</TableCell>
                  <TableCell>Мест</TableCell>
                  <TableCell>Занято</TableCell>
                  <TableCell>Телефон</TableCell>
                  <TableCell>Действия</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rooms?.map((room) => (
                  <TableRow key={room.id}>
                    <TableCell>{room.number}</TableCell>
                    <TableCell>{room.floor}</TableCell>
                    <TableCell>{roomTypeLabels[room.room_type]}</TableCell>
                    <TableCell>{room.capacity}</TableCell>
                    <TableCell>{room.occupied_places}</TableCell>
                    <TableCell>{room.phone_number}</TableCell>
                    <TableCell>
                      <Button size="small" onClick={() => setHistoryRoomId(room.id)}>
                        История
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Box>
        </CardContent>
      </Card>

      <Dialog open={Boolean(historyRoomId)} onClose={() => setHistoryRoomId(null)} maxWidth="md" fullWidth>
        <DialogTitle>История проживаний</DialogTitle>
        <DialogContent>
          <Stack direction="row" spacing={2} my={2}>
            <DatePicker
              label="С начала"
              value={startDate}
              onChange={(value) => setStartDate(value)}
            />
            <DatePicker label="По" value={endDate} onChange={(value) => setEndDate(value)} />
          </Stack>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Клиент</TableCell>
                <TableCell>Заезд</TableCell>
                <TableCell>Выезд</TableCell>
                <TableCell>Статус</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {roomHistory?.map((stay) => (
                <TableRow key={stay.id}>
                  <TableCell>{stay.client.full_name}</TableCell>
                  <TableCell>{stay.check_in}</TableCell>
                  <TableCell>{stay.check_out ?? '—'}</TableCell>
                  <TableCell>{stay.status === 'active' ? 'Проживает' : 'Завершено'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogContent>
      </Dialog>
    </Stack>
  );
}


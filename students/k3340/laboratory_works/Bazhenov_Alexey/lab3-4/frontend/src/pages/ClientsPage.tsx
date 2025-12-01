import {
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
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
  useCheckoutStayMutation,
  useCreateClientMutation,
  useCreateStayMutation,
  useGetClientStaysQuery,
  useGetClientsQuery,
  useGetOverlappingClientsQuery,
} from '../services/api';
import type { Client } from '../types';

export function ClientsPage() {
  const [cityFilter, setCityFilter] = useState('');
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [checkInDate, setCheckInDate] = useState<Dayjs | null>(dayjs());
  const [roomNumber, setRoomNumber] = useState('');
  const [checkoutDate, setCheckoutDate] = useState<Dayjs | null>(dayjs());
  const [overlapStart, setOverlapStart] = useState<Dayjs | null>(dayjs().subtract(7, 'day'));
  const [overlapEnd, setOverlapEnd] = useState<Dayjs | null>(dayjs());

  const { data: clients } = useGetClientsQuery(cityFilter ? { city: cityFilter } : undefined);
  const { data: stays } = useGetClientStaysQuery(selectedClient?.id ?? 0, {
    skip: !selectedClient,
  });
  const overlapParams = useMemo(() => {
    if (!selectedClient || !overlapStart || !overlapEnd) return null;
    return {
      clientId: selectedClient.id,
      start: overlapStart.format('YYYY-MM-DD'),
      end: overlapEnd.format('YYYY-MM-DD'),
    };
  }, [selectedClient, overlapStart, overlapEnd]);
  const { data: overlapping } = useGetOverlappingClientsQuery(overlapParams ?? skipToken);

  const [createClient] = useCreateClientMutation();
  const [createStay, { isLoading: isCheckInLoading }] = useCreateStayMutation();
  const [checkoutStay, { isLoading: isCheckoutLoading }] = useCheckoutStayMutation();

  const handleCreateClient = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    await createClient({
      passport_number: formData.get('passport_number') as string,
      last_name: formData.get('last_name') as string,
      first_name: formData.get('first_name') as string,
      middle_name: formData.get('middle_name') as string,
      city: formData.get('city') as string,
      phone: formData.get('phone') as string,
      email: formData.get('email') as string,
    }).unwrap();
    setCreateDialogOpen(false);
    event.currentTarget.reset();
  };

  const handleCheckIn = async () => {
    if (!selectedClient || !checkInDate || !roomNumber) return;
    await createStay({
      client: selectedClient.id,
      room: Number(roomNumber),
      check_in: checkInDate.format('YYYY-MM-DD'),
    }).unwrap();
    setRoomNumber('');
  };

  const handleCheckout = async (stayId: number) => {
    if (!checkoutDate) return;
    await checkoutStay({
      stayId,
      check_out: checkoutDate.format('YYYY-MM-DD'),
    }).unwrap();
  };

  return (
    <Stack spacing={3}>
      <Card>
        <CardContent>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center">
            <TextField
              label="Город"
              value={cityFilter}
              onChange={(event) => setCityFilter(event.target.value)}
            />
            <Button variant="contained" onClick={() => setCreateDialogOpen(true)}>
              Добавить клиента
            </Button>
          </Stack>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Клиенты
          </Typography>
          <Box sx={{ overflowX: 'auto' }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ФИО</TableCell>
                  <TableCell>Паспорт</TableCell>
                  <TableCell>Город</TableCell>
                  <TableCell>Телефон</TableCell>
                  <TableCell />
                </TableRow>
              </TableHead>
              <TableBody>
                {clients?.map((client) => (
                  <TableRow key={client.id}>
                    <TableCell>{client.full_name}</TableCell>
                    <TableCell>{client.passport_number}</TableCell>
                    <TableCell>{client.city}</TableCell>
                    <TableCell>{client.phone ?? '—'}</TableCell>
                    <TableCell align="right">
                      <Button size="small" onClick={() => setSelectedClient(client)}>
                        Управлять
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Box>
        </CardContent>
      </Card>

      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Новый клиент</DialogTitle>
        <DialogContent>
          <Box component="form" id="create-client-form" onSubmit={handleCreateClient} sx={{ mt: 2 }} display="flex" flexDirection="column" gap={2}>
            <TextField name="passport_number" label="Паспорт" required />
            <TextField name="last_name" label="Фамилия" required />
            <TextField name="first_name" label="Имя" required />
            <TextField name="middle_name" label="Отчество" />
            <TextField name="city" label="Город" required />
            <TextField name="phone" label="Телефон" />
            <TextField name="email" label="Email" />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Отмена</Button>
          <Button type="submit" form="create-client-form" variant="contained">
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={Boolean(selectedClient)} onClose={() => setSelectedClient(null)} maxWidth="md" fullWidth>
        <DialogTitle>{selectedClient?.full_name}</DialogTitle>
        <DialogContent>
          <Typography variant="subtitle1" gutterBottom>
            Управление проживанием
          </Typography>
          <Stack
            direction={{ xs: 'column', md: 'row' }}
            spacing={2}
            mb={3}
          >
            <Box sx={{ flex: 1 }}>
              <Stack spacing={2}>
                <TextField
                  label="Номер комнаты (ID)"
                  value={roomNumber}
                  onChange={(event) => setRoomNumber(event.target.value)}
                />
                <DatePicker label="Дата заселения" value={checkInDate} onChange={setCheckInDate} />
                <Button variant="contained" onClick={handleCheckIn} disabled={isCheckInLoading}>
                  Заселить
                </Button>
              </Stack>
            </Box>
            <Box sx={{ flex: 1 }}>
              <Stack spacing={2}>
                <DatePicker label="Дата выселения" value={checkoutDate} onChange={setCheckoutDate} />
                <Button
                  variant="outlined"
                  disabled={!stays?.length || isCheckoutLoading}
                  onClick={() => {
                    const activeStay = stays?.find((stay) => stay.status === 'active');
                    if (activeStay) {
                      handleCheckout(activeStay.id);
                    }
                  }}
                >
                  Выселить активного клиента
                </Button>
              </Stack>
            </Box>
          </Stack>

          <Typography variant="subtitle1" gutterBottom>
            Текущие проживание
          </Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Комната</TableCell>
                <TableCell>Дата заезда</TableCell>
                <TableCell>Дата выезда</TableCell>
                <TableCell>Статус</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {stays?.map((stay) => (
                <TableRow key={stay.id}>
                  <TableCell>{stay.room}</TableCell>
                  <TableCell>{stay.check_in}</TableCell>
                  <TableCell>{stay.check_out ?? '—'}</TableCell>
                  <TableCell>{stay.status === 'active' ? 'Проживает' : 'Завершено'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          <Typography variant="subtitle1" mt={3}>
            Совпадающие проживающие
          </Typography>
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} my={2}>
            <DatePicker label="С" value={overlapStart} onChange={setOverlapStart} />
            <DatePicker label="По" value={overlapEnd} onChange={setOverlapEnd} />
          </Stack>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Клиент</TableCell>
                <TableCell>Город</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {overlapping?.map((client) => (
                <TableRow key={client.id}>
                  <TableCell>{client.full_name}</TableCell>
                  <TableCell>{client.city}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelectedClient(null)}>Закрыть</Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
}


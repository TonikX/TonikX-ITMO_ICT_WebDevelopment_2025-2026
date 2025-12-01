import {
  Card,
  CardContent,
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
import { useState } from 'react';

import { useGetStaysQuery } from '../services/api';

export function StaysPage() {
  const [status, setStatus] = useState('');
  const { data: stays } = useGetStaysQuery(status ? { status } : undefined);

  return (
    <Stack spacing={3}>
      <Card>
        <CardContent>
          <TextField
            select
            label="Статус"
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            sx={{ width: 240 }}
          >
            <MenuItem value="">Все</MenuItem>
            <MenuItem value="active">Проживают</MenuItem>
            <MenuItem value="completed">Выселены</MenuItem>
          </TextField>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Проживания
          </Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Клиент ID</TableCell>
                <TableCell>Комната</TableCell>
                <TableCell>Заезд</TableCell>
                <TableCell>Выезд</TableCell>
                <TableCell>Статус</TableCell>
                <TableCell>Стоимость</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {stays?.map((stay) => (
                <TableRow key={stay.id}>
                  <TableCell>{stay.client}</TableCell>
                  <TableCell>{stay.room}</TableCell>
                  <TableCell>{stay.check_in}</TableCell>
                  <TableCell>{stay.check_out ?? '—'}</TableCell>
                  <TableCell>{stay.status === 'active' ? 'Проживает' : 'Выселен'}</TableCell>
                  <TableCell>{stay.total_cost}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </Stack>
  );
}


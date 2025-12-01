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
import dayjs from 'dayjs';
import { useState } from 'react';

import { useGetQuarterlyReportQuery } from '../services/api';

export function ReportsPage() {
  const now = dayjs();
  const [quarter, setQuarter] = useState(Math.floor(now.month() / 3) + 1);
  const [year, setYear] = useState(now.year());

  const { data: report } = useGetQuarterlyReportQuery({ quarter, year });

  return (
    <Stack spacing={3}>
      <Stack direction={{ xs: 'column', md: 'row' }} spacing={3}>
        <Card sx={{ flex: 1, minWidth: 280 }}>
          <CardContent>
            <TextField
              select
              label="Квартал"
              value={quarter}
              onChange={(event) => setQuarter(Number(event.target.value))}
              fullWidth
              sx={{ mb: 2 }}
            >
              {[1, 2, 3, 4].map((q) => (
                <MenuItem key={q} value={q}>
                  Q{q}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label="Год"
              type="number"
              value={year}
              onChange={(event) => setYear(Number(event.target.value))}
              fullWidth
            />
            <Typography variant="h6" mt={3}>
              Всего доход: {report?.total_income?.toLocaleString() ?? '—'} ₽
            </Typography>
          </CardContent>
        </Card>
        <Card sx={{ flex: 2 }}>
          <CardContent>
            <Typography variant="subtitle1">Клиенты по номерам</Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Номер</TableCell>
                  <TableCell>Клиентов</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {report?.clients_per_room.map((row) => (
                  <TableRow key={row.room__id}>
                    <TableCell>{row.room__number}</TableCell>
                    <TableCell>{row.client_count}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Stack>

      <Stack direction={{ xs: 'column', md: 'row' }} spacing={3}>
        <Card sx={{ flex: 1 }}>
          <CardContent>
            <Typography variant="subtitle1">Номера по этажам</Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Этаж</TableCell>
                  <TableCell>Кол-во</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {report?.rooms_per_floor.map((row) => (
                  <TableRow key={row.floor}>
                    <TableCell>{row.floor}</TableCell>
                    <TableCell>{row.room_count}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
        <Card sx={{ flex: 1 }}>
          <CardContent>
            <Typography variant="subtitle1">Доход по номерам</Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Номер</TableCell>
                  <TableCell>Доход</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {report?.income_per_room.map((row) => (
                  <TableRow key={row.room__id}>
                    <TableCell>{row.room__number}</TableCell>
                    <TableCell>{Number(row.total_income).toLocaleString()} ₽</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Stack>
    </Stack>
  );
}


import React, { useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Grid,
  Card,
  CardContent,
} from '@mui/material'
import { staffAPI } from '../api/staff.api'
import { MonthlyReport } from '../types'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'

export const MonthlyReportPage: React.FC = () => {
  const [year, setYear] = useState(new Date().getFullYear())
  const [month, setMonth] = useState(new Date().getMonth() + 1)
  const [report, setReport] = useState<MonthlyReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const handleGenerate = async () => {
    try {
      setLoading(true)
      const data = await staffAPI.getMonthlyReport(year, month)
      setReport(data)
      setNotification({
        open: true,
        message: 'Отчёт успешно сгенерирован',
        severity: 'success',
      })
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Ежемесячный отчёт
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
          <TextField
            label="Год"
            type="number"
            value={year}
            onChange={(e) => setYear(parseInt(e.target.value))}
            sx={{ width: 120 }}
          />
          <TextField
            label="Месяц"
            type="number"
            value={month}
            onChange={(e) => setMonth(parseInt(e.target.value))}
            inputProps={{ min: 1, max: 12 }}
            sx={{ width: 120 }}
          />
          <Button
            variant="contained"
            onClick={handleGenerate}
            disabled={loading}
          >
            Сгенерировать отчёт
          </Button>
        </Box>
      </Paper>

      {report && (
        <>
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Новые читатели за месяц
                  </Typography>
                  <Typography variant="h3" color="primary">
                    {report.new_readers.total}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Период отчёта
                  </Typography>
                  <Typography>
                    {report.period.start_date} - {report.period.end_date}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Новые читатели по залам
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Зал</TableCell>
                    <TableCell align="right">Новых читателей</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {report.new_readers.by_hall.map((item) => (
                    <TableRow key={item.hall_id}>
                      <TableCell>{item.hall_name}</TableCell>
                      <TableCell align="right">{item.new_readers_count}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Ежедневная статистика
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Дата</TableCell>
                    <TableCell align="right">Книг всего</TableCell>
                    <TableCell align="right">Читателей всего</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {report.daily_statistics.map((day) => (
                    <TableRow key={day.date}>
                      <TableCell>{day.date}</TableCell>
                      <TableCell align="right">{day.total.books_count}</TableCell>
                      <TableCell align="right">{day.total.readers_count}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </>
      )}

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={() => setNotification({ ...notification, open: false })}
      />
    </Container>
  )
}



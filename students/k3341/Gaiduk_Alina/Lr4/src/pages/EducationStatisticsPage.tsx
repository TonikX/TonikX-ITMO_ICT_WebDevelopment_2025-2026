import React, { useEffect, useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material'
import { readersAPI } from '../api/readers.api'
import { EducationStatistics } from '../types'
import { Notification } from '../components/Notification'
import { Loading } from '../components/Loading'
import { getErrorMessage } from '../utils/notifications'

export const EducationStatisticsPage: React.FC = () => {
  const [statistics, setStatistics] = useState<EducationStatistics | null>(null)
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  useEffect(() => {
    loadStatistics()
  }, [])

  const loadStatistics = async () => {
    try {
      setLoading(true)
      const data = await readersAPI.getEducationStatistics()
      setStatistics(data)
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

  if (loading) return <Loading />

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        Статистика по образованию читателей
      </Typography>
      {statistics && (
        <Box sx={{ mt: 3 }}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6">
              Всего активных читателей: {statistics.total}
            </Typography>
          </Paper>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Категория</TableCell>
                  <TableCell align="right">Процент (%)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>Начальное образование</TableCell>
                  <TableCell align="right">{statistics.percentages.начальное}%</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Среднее образование</TableCell>
                  <TableCell align="right">{statistics.percentages.среднее}%</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Высшее образование</TableCell>
                  <TableCell align="right">{statistics.percentages.высшее}%</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Не указано</TableCell>
                  <TableCell align="right">{statistics.percentages.не_указано}%</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>С учёной степенью</TableCell>
                  <TableCell align="right">{statistics.percentages.учёная_степень}%</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
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



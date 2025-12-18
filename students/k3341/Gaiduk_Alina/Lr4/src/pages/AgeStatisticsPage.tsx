import React, { useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Card,
  CardContent,
} from '@mui/material'
import { readersAPI } from '../api/readers.api'
import { AgeStatistics } from '../types'
import { Notification } from '../components/Notification'
import { getErrorMessage } from '../utils/notifications'

export const AgeStatisticsPage: React.FC = () => {
  const [age, setAge] = useState(20)
  const [statistics, setStatistics] = useState<AgeStatistics | null>(null)
  const [notification, setNotification] = useState<{
    open: boolean
    message: string
    severity: 'success' | 'error' | 'info'
  }>({ open: false, message: '', severity: 'info' })

  const handleLoad = async () => {
    try {
      const data = await readersAPI.getAgeStatistics(age)
      setStatistics(data)
    } catch (error) {
      setNotification({
        open: true,
        message: getErrorMessage(error),
        severity: 'error',
      })
    }
  }

  return (
    <Container maxWidth="sm">
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Статистика по возрасту читателей
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
          <TextField
            label="Максимальный возраст"
            type="number"
            value={age}
            onChange={(e) => setAge(parseInt(e.target.value))}
            fullWidth
          />
          <Button variant="contained" onClick={handleLoad}>
            Загрузить
          </Button>
        </Box>
      </Paper>

      {statistics && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Результат
            </Typography>
            <Typography variant="body1">
              Количество активных читателей младше {statistics.max_age} лет:
            </Typography>
            <Typography variant="h3" color="primary" sx={{ mt: 2 }}>
              {statistics.readers_count}
            </Typography>
          </CardContent>
        </Card>
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



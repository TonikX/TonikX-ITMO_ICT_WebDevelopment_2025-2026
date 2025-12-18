import React from 'react'
import { Box, CircularProgress } from '@mui/material'

// компонент для отображения индикатора загрузки
export const Loading: React.FC = () => {
  return (

    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="400px"
    >
      <CircularProgress />
    </Box>
  )
}



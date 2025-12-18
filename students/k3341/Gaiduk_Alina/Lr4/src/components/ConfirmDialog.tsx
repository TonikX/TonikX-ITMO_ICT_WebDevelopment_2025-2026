import React from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from '@mui/material'

// интерфейс для пропсов компонента ConfirmDialog
interface ConfirmDialogProps {
  open: boolean // флаг видимости диалога
  title: string
  message: string
  onConfirm: () => void
  onCancel: () => void
}

// компонент диалога подтверждения действия (например, удаления)
export const ConfirmDialog: React.FC<ConfirmDialogProps> = ({
  open,
  title,
  message,
  onConfirm,
  onCancel,
}) => {
  return (
    // модальное окно из MUI
    <Dialog open={open} onClose={onCancel}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{message}</DialogContentText>
      </DialogContent>
      {/* область с кнопками действий */}
      <DialogActions>
        <Button onClick={onCancel} color="primary">
          Отмена
        </Button>
        <Button onClick={onConfirm} color="error" variant="contained">
          Подтвердить
        </Button>
      </DialogActions>
    </Dialog>
  )
}



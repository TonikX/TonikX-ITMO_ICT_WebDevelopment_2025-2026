/**
 * Custom hook для управления диалогом подтверждения удаления
 * Упрощает работу с delete confirmation state
 */

import { useState, useCallback } from 'react'
import { DeleteConfirmState, DEFAULT_DELETE_CONFIRM } from '../types/common'

// интерфейс возвращаемого значения хука useDeleteConfirm
interface UseDeleteConfirmReturn {
  deleteConfirm: DeleteConfirmState // состояние диалога подтверждения удаления
  openDeleteConfirm: (id: number) => void
  closeDeleteConfirm: () => void
}

// хук для управления диалогом подтверждения удаления
export const useDeleteConfirm = (): UseDeleteConfirmReturn => {
  // начальное состояние диалога подтверждения
  const [deleteConfirm, setDeleteConfirm] = useState<DeleteConfirmState>(DEFAULT_DELETE_CONFIRM)

  // функция для открытия диалога подтверждения удаления
  const openDeleteConfirm = useCallback((id: number) => {
    setDeleteConfirm({ open: true, id })
  }, []) // пустой массив зависимостей - функция создается один раз

  // функция для закрытия диалога подтверждения удаления
  const closeDeleteConfirm = useCallback(() => {
    setDeleteConfirm(DEFAULT_DELETE_CONFIRM)
  }, [])

  // возвращаем объект с состоянием и функциями управления диалогом
  return {
    deleteConfirm,
    openDeleteConfirm,
    closeDeleteConfirm,
  }
}


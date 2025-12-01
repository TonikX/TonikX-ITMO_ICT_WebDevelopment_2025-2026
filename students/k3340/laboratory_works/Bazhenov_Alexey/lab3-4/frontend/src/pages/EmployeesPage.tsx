import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
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
import DeleteIcon from '@mui/icons-material/Delete';
import { useState } from 'react';

import {
  useCreateEmployeeMutation,
  useFireEmployeeMutation,
  useGetEmployeesQuery,
  useUpdateScheduleMutation,
  useWhoCleansQuery,
} from '../services/api';
import type { CleaningAssignment, Employee } from '../types';

const weekdayOptions = [
  { value: 'mon', label: 'Пн' },
  { value: 'tue', label: 'Вт' },
  { value: 'wed', label: 'Ср' },
  { value: 'thu', label: 'Чт' },
  { value: 'fri', label: 'Пт' },
  { value: 'sat', label: 'Сб' },
  { value: 'sun', label: 'Вс' },
];

export function EmployeesPage() {
  const { data: employees } = useGetEmployeesQuery();
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [scheduleDialog, setScheduleDialog] = useState<Employee | null>(null);
  const [assignments, setAssignments] = useState<CleaningAssignment[]>([]);
  const [clientId, setClientId] = useState('');
  const [weekday, setWeekday] = useState('');
  const {
    data: cleaner,
    refetch: refetchCleaner,
    isFetching: isCleanerLoading,
  } = useWhoCleansQuery(
    { clientId: Number(clientId), weekday },
    { skip: !clientId || !weekday },
  );

  const [createEmployee] = useCreateEmployeeMutation();
  const [fireEmployee] = useFireEmployeeMutation();
  const [updateSchedule] = useUpdateScheduleMutation();

  const handleCreateEmployee = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    await createEmployee({
      last_name: formData.get('last_name') as string,
      first_name: formData.get('first_name') as string,
      middle_name: formData.get('middle_name') as string,
    }).unwrap();
    event.currentTarget.reset();
    setCreateDialogOpen(false);
  };

  const openScheduleDialog = (employee: Employee) => {
    setScheduleDialog(employee);
    setAssignments(employee.assignments ?? []);
  };

  const addAssignment = () => {
    setAssignments((prev) => [...prev, { floor: 1, weekday: 'mon' }]);
  };

  const updateAssignment = (index: number, patch: Partial<CleaningAssignment>) => {
    setAssignments((prev) => prev.map((item, idx) => (idx === index ? { ...item, ...patch } : item)));
  };

  const removeAssignment = (index: number) => {
    setAssignments((prev) => prev.filter((_, idx) => idx !== index));
  };

  const handleScheduleSave = async () => {
    if (!scheduleDialog) return;
    await updateSchedule({
      employeeId: scheduleDialog.id,
      assignments: assignments.map((assignment) => ({
        floor: assignment.floor,
        weekday: assignment.weekday,
      })),
    }).unwrap();
    setScheduleDialog(null);
  };

  return (
    <Stack spacing={3}>
      <Card>
        <CardContent>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
            <Button variant="contained" onClick={() => setCreateDialogOpen(true)}>
              Принять сотрудника
            </Button>
            <TextField
              label="ID клиента"
              value={clientId}
              onChange={(event) => setClientId(event.target.value)}
            />
            <TextField
              select
              label="День недели"
              value={weekday}
              onChange={(event) => setWeekday(event.target.value)}
            >
              <MenuItem value="">—</MenuItem>
              {weekdayOptions.map((day) => (
                <MenuItem key={day.value} value={day.value}>
                  {day.label}
                </MenuItem>
              ))}
            </TextField>
            <Button
              variant="outlined"
              disabled={!clientId || !weekday}
              onClick={() => refetchCleaner()}
            >
              Кто убирает?
            </Button>
            {isCleanerLoading ? (
              <Typography>Поиск...</Typography>
            ) : cleaner ? (
              <Chip label={`${cleaner.last_name} ${cleaner.first_name}`} color="success" />
            ) : null}
          </Stack>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6">Сотрудники</Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>ФИО</TableCell>
                <TableCell>Статус</TableCell>
                <TableCell>График</TableCell>
                <TableCell />
              </TableRow>
            </TableHead>
            <TableBody>
              {employees?.map((employee) => (
                <TableRow key={employee.id}>
                  <TableCell>{`${employee.last_name} ${employee.first_name}`}</TableCell>
                  <TableCell>{employee.status === 'active' ? 'Работает' : 'Уволен'}</TableCell>
                  <TableCell>
                    <Stack direction="row" spacing={1} flexWrap="wrap">
                      {employee.assignments?.map((assignment) => (
                        <Chip
                          key={`${assignment.floor}-${assignment.weekday}`}
                          label={`Этаж ${assignment.floor} — ${
                            weekdayOptions.find((w) => w.value === assignment.weekday)?.label
                          }`}
                        />
                      ))}
                    </Stack>
                  </TableCell>
                  <TableCell align="right">
                    <Button size="small" onClick={() => openScheduleDialog(employee)}>
                      График
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      onClick={() => fireEmployee(employee.id)}
                      disabled={employee.status === 'fired'}
                    >
                      Уволить
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Новый сотрудник</DialogTitle>
        <Box component="form" id="create-employee-form" onSubmit={handleCreateEmployee}>
          <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField name="last_name" label="Фамилия" required />
            <TextField name="first_name" label="Имя" required />
            <TextField name="middle_name" label="Отчество" />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setCreateDialogOpen(false)}>Отмена</Button>
            <Button type="submit" variant="contained">
              Сохранить
            </Button>
          </DialogActions>
        </Box>
      </Dialog>

      <Dialog open={Boolean(scheduleDialog)} onClose={() => setScheduleDialog(null)} maxWidth="sm" fullWidth>
        <DialogTitle>График уборки</DialogTitle>
        <DialogContent>
          <Stack spacing={2}>
            {assignments.map((assignment, index) => (
              <Stack key={`${index}-${assignment.weekday}`} direction="row" spacing={2} alignItems="center">
                <TextField
                  label="Этаж"
                  type="number"
                  value={assignment.floor}
                  onChange={(event) =>
                    updateAssignment(index, { floor: Number(event.target.value) })
                  }
                />
                <TextField
                  select
                  label="День"
                  value={assignment.weekday}
                  onChange={(event) =>
                    updateAssignment(index, { weekday: event.target.value })
                  }
                >
                  {weekdayOptions.map((day) => (
                    <MenuItem key={day.value} value={day.value}>
                      {day.label}
                    </MenuItem>
                  ))}
                </TextField>
                <IconButton onClick={() => removeAssignment(index)}>
                  <DeleteIcon />
                </IconButton>
              </Stack>
            ))}
            <Button onClick={addAssignment}>Добавить</Button>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setScheduleDialog(null)}>Отмена</Button>
          <Button variant="contained" onClick={handleScheduleSave}>
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
}


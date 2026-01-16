# Лабораторная 4

### 1. Настройка CORS

В проекте Django устанавливаем
```pip install django-cors-headers```

Далее в файле `settings.py` добавляем в списки:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```

И разрешение для фронтенда: 
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

### 2. Реализовать интерфейсы авторизации, регистрации и изменения учётных данных и настроить взаимодействие с серверной частью.

#### 2.1 Взаимодействие с сервером

Все запросы авторизованные — токен передаётся в заголовках Authorization: Token <token>.

`api.js`

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default api
```

Перед каждым переходом по маршруту осуществляется проверка, авторизован ли пользователь: 
```javascript
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})
```

#### 2.2 Авторизация, регистрация и изменение учетных данных 

![](1.png)
![](2.png)
![](3.png)

### 3. Реализовать клиентские интерфейсы

Routes:

```javascript
const routes = [
  {
    path: '/login',
    component: LoginView,
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: HomeView,
    meta: { requiresAuth: true },
  },
  { path: '/register', component: RegisterView },
  { path: '/profile', component: ProfileView },
  { path: '/residents', component: ResidentsListView },
  { path: '/residents/:id', component: ResidentDetailView },
  { path: '/residents/:id/edit', component: ResidentEditView },
  { path: '/residents/new', component: NewResidentView },
  { path: '/reservations', component: ReservationsListView },
  { path: '/reservations/new', component: NewReservationView },
  { path: '/reservations/:id', component: ReservationDetailView },
  { path: '/reservations/:id/edit', component: ReservationEditView },
  { path: '/rooms', component: RoomsListView },
  { path: '/rooms/new', component: NewRoomView },
  { path: '/rooms/:id', component: RoomsDetailView },
  { path: '/rooms/:id/edit', component: RoomsEditView },
  { path: '/clients-by-room', component: ClientsByRoomView },
  { path: '/clients-from-city', component: ClientsFromCityView},
  { path: '/clients-with-city', component: ClientBookingsView},
  { path: '/report', component: ReportView},
  { path: '/cleaning-info-per-day', component: CleaningPerDayView},
  { path: '/available-rooms', component: AvailableRoomsView},
  { path: '/workers', component: WorkersListView},
  { path: '/workers/:id/edit', component: WorkerEditView},
  { path: '/workers/new', component: NewWorkerView},
  { path: '/cleaning', component: CleaningListView},
  { path: '/cleaning/:id/edit', component: CleaningEditView},
  { path: '/cleaning/new', component: NewCleaningView},

]
```



Реализованны следующие интерфейсы:

1. Клиенты: 

      - Добавление нового клиента
      - Удаление клиента
      - Изменение данных клиента
      - Просмотр списка всех клиентов
      ![](clients_1.png)
      ![](clients_2.png)

2. Бронирования: 

      - Добавление нового бронирования 
      - Удаление бронирования 
      - Изменение данных бронирования 
      - Просмотр списка всех бронирований
      ![](res_1.png)
      ![](res_2.png)
      ![](res_3.png)

3. Номера: 
   
      - Просмотр списка всех номеров 
      - Изменение данных номера
      - Удаление номера
      - Добавление нового номера
      ![](rooms_1.png)
      ![](rooms_2.png)
      ![](rooms_3.png)
   
4. Сотрудники:
   
      - Добавление нового сотрудника
      - Редактирование данных сотрудника
      - Редактирование графика уборок сотрудника 
      - Удаление сотрудника
      ![](w_1.png)
      ![](w_2.png)
      ![](w_3.png)

5. Фактические уборки:

      - Добавление записи об уборке 
      - Редактирование/удаление записи об уборке 
      ![](cl_1.png)
      ![](cl_2.png)

Для удобства реализована верхняя панель навигации: 

![](4.png)
![](5.png)

Интерфейсы для запросов

   - О клиентах, проживавших в заданном номере, в заданный период времени
   - О количестве клиентов, прибывших из заданного города
   - О том, кто из служащих убирал номер указанного клиента в заданный день недели
   - Сколько в гостинице свободных номеров
   - Список клиентов с указанием места жительства, которые проживали в те же дни, что и заданный клиент, в определенный период времени
   - Выдача отчета

![](q_1.png)
![](q_2.png)
![](q_3.png)
![](q_4.png)
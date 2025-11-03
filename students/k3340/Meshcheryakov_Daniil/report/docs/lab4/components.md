# Компоненты приложения

Описание всех Vue компонентов системы управления читальным залом.

## Структура компонентов

```
src/
├── components/          # Переиспользуемые компоненты
│   └── NavigationBar.vue
└── views/              # Страничные компоненты
    ├── Login.vue
    ├── Dashboard.vue
    ├── ReadingRooms.vue
    ├── Readers.vue
    ├── Reservations.vue
    ├── Librarians.vue
    └── Reports.vue
```

---

## NavigationBar.vue

Верхняя панель навигации и боковое меню.

### Функциональность

- Отображение названия приложения
- Боковое меню с навигацией
- Информация о текущем пользователе
- Кнопка выхода

### Код (excerpt)

```vue
<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar color="primary" prominent>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-book-open-variant</v-icon>
        Читальный Зал
      </v-toolbar-title>
      <v-spacer />
      <v-btn @click="logout">
        <v-icon start>mdi-logout</v-icon>
        Выход
      </v-btn>
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item to="/dashboard" prepend-icon="mdi-view-dashboard">
          <v-list-item-title>Панель управления</v-list-item-title>
        </v-list-item>
        
        <v-list-item to="/reading-rooms" prepend-icon="mdi-door">
          <v-list-item-title>Читальные залы</v-list-item-title>
        </v-list-item>

        <!-- Остальные пункты меню... -->
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const drawer = ref(true)
const router = useRouter()
const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
  router.push('/')
}
</script>
```

---

## Login.vue

Страница входа и регистрации.

### Функциональность

- Форма входа (username, password)
- Модальное окно регистрации
- Валидация полей
- Success/Error сообщения
- Автоматический редирект после входа

### Ключевые элементы

**Форма входа:**
```vue
<v-form @submit.prevent="handleLogin">
  <v-text-field
    v-model="username"
    label="Имя пользователя"
    prepend-inner-icon="mdi-account"
    variant="outlined"
    density="comfortable"
    required
  />
  
  <v-text-field
    v-model="password"
    label="Пароль"
    type="password"
    prepend-inner-icon="mdi-lock"
    variant="outlined"
    density="comfortable"
    required
  />
  
  <v-btn type="submit" color="primary" block :loading="loading">
    <v-icon start>mdi-login</v-icon>
    Войти
  </v-btn>
</v-form>
```

**Регистрация:**
```vue
<v-dialog v-model="showRegister" max-width="600">
  <v-card>
    <v-card-title>Регистрация нового пользователя</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="handleRegister">
        <v-text-field v-model="registerForm.username" label="Имя пользователя" />
        <v-text-field v-model="registerForm.email" label="Email" type="email" />
        <v-text-field v-model="registerForm.password" label="Пароль" type="password" />
        <v-text-field v-model="registerForm.re_password" label="Подтвердите пароль" type="password" />
        
        <v-btn type="submit" :loading="registerLoading">
          Зарегистрироваться
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</v-dialog>
```

---

## Dashboard.vue

Главная панель управления.

### Функциональность

- **Статистика:** Карточки с общими показателями
- **Свободные залы:** Поиск по дате/времени
- **Последние бронирования:** Таблица недавних записей

### Ключевые секции

**Статистика:**
```vue
<v-row>
  <v-col cols="12" md="3">
    <v-card>
      <v-card-text>
        <div class="text-h4">{{ stats.rooms_count }}</div>
        <div class="text-subtitle-1">Читальных залов</div>
      </v-card-text>
    </v-card>
  </v-col>
  <!-- Остальные карточки... -->
</v-row>
```

**Свободные залы с date picker:**
```vue
<v-menu v-model="dateMenu">
  <template v-slot:activator="{ props }">
    <v-text-field
      :model-value="formattedDate"
      label="Дата и время"
      readonly
      v-bind="props"
    />
  </template>
  <v-card>
    <v-date-picker
      v-model="datePickerValue"
      locale="ru"
    />
    <v-text-field
      v-model="timeValue"
      label="Время"
      type="time"
    />
  </v-card>
</v-menu>
<v-btn @click="loadFreeReadingRooms">Обновить</v-btn>
```

**Таблица:**
```vue
<v-data-table
  :headers="headers"
  :items="freeReadingRooms"
  :loading="loading"
  no-data-text="Нет данных"
  loading-text="Загрузка..."
/>
```

---

## ReadingRooms.vue

Управление читальными залами.

### Функциональность

- Таблица всех залов
- CRUD операции
- Диалог создания/редактирования
- Удаление с подтверждением

### Форма зала

```vue
<v-form ref="formRef">
  <v-text-field
    v-model.number="form.number"
    label="Номер зала"
    type="number"
    variant="outlined"
    density="comfortable"
  />
  
  <v-text-field
    v-model.number="form.floor"
    label="Этаж"
    type="number"
    variant="outlined"
  />
  
  <v-select
    v-model="form.room_type"
    label="Тип зала"
    :items="['small', 'medium', 'large']"
    variant="outlined"
  />
  
  <v-text-field
    v-model.number="form.capacity"
    label="Вместимость (мест)"
    type="number"
    variant="outlined"
  />
  
  <v-text-field
    v-model.number="form.hourly_rate"
    label="Цена за час (₽)"
    type="number"
    step="0.01"
    variant="outlined"
  />
  
  <v-textarea
    v-model="form.description"
    label="Описание"
    variant="outlined"
  />
</v-form>
```

### Таблица действий

```vue
<template v-slot:item.actions="{ item }">
  <v-btn icon size="small" @click="editRoom(item)">
    <v-icon>mdi-pencil</v-icon>
  </v-btn>
  <v-btn icon size="small" @click="deleteRoom(item)">
    <v-icon>mdi-delete</v-icon>
  </v-btn>
</template>
```

---

## Readers.vue

Управление читателями.

### Форма читателя

```vue
<v-form ref="formRef">
  <v-text-field
    v-model="form.library_card"
    label="Номер читательского билета"
    variant="outlined"
    required
  />
  
  <v-text-field v-model="form.last_name" label="Фамилия" variant="outlined" />
  <v-text-field v-model="form.first_name" label="Имя" variant="outlined" />
  <v-text-field v-model="form.patronymic" label="Отчество" variant="outlined" />
  <v-text-field v-model="form.phone" label="Телефон" variant="outlined" />
  <v-text-field v-model="form.email" label="Email" type="email" variant="outlined" />
</v-form>
```

---

## Reservations.vue

Управление бронированиями.

### User-friendly Date/Time Picker

**Начало бронирования:**
```vue
<v-menu v-model="dateMenuFrom">
  <template v-slot:activator="{ props }">
    <v-text-field
      :model-value="formattedDateFrom"
      label="Начало бронирования"
      readonly
      v-bind="props"
    />
  </template>
  <v-card>
    <v-date-picker
      v-model="datePickerFrom"
      @update:model-value="updateDateFrom"
      locale="ru"
    />
    <v-text-field
      v-model="timeFrom"
      label="Время"
      type="time"
    />
  </v-card>
</v-menu>
```

### Выбор читателя и зала

```vue
<v-select
  v-model="form.reader"
  :items="readers"
  item-title="text"
  item-value="id"
  label="Читатель"
  variant="outlined"
/>

<v-select
  v-model="form.reading_room"
  :items="readingRooms"
  item-title="text"
  item-value="id"
  label="Читальный зал"
  variant="outlined"
/>

<v-checkbox
  v-model="form.is_active"
  label="Активно"
  color="primary"
/>
```

---

## Librarians.vue

Управление библиотекарями.

### Специальные действия

```vue
<template v-slot:item.actions="{ item }">
  <v-btn icon @click="editLibrarian(item)">
    <v-icon>mdi-pencil</v-icon>
  </v-btn>
  
  <!-- Fire/Hire -->
  <v-btn
    v-if="item.is_active"
    icon
    color="error"
    @click="fireLibrarian(item)"
  >
    <v-icon>mdi-account-remove</v-icon>
  </v-btn>
  <v-btn
    v-else
    icon
    color="success"
    @click="hireLibrarian(item)"
  >
    <v-icon>mdi-account-plus</v-icon>
  </v-btn>
  
  <v-btn icon color="error" @click="deleteLibrarian(item)">
    <v-icon>mdi-delete</v-icon>
  </v-btn>
</template>
```

---

## Reports.vue

Просмотр отчетов.

### Выбор квартала и экспорт

```vue
<v-select
  v-model="selectedQuarter"
  :items="[1, 2, 3, 4]"
  label="Квартал"
  @update:model-value="loadReport"
/>

<v-btn @click="exportReport">
  <v-icon start>mdi-download</v-icon>
  Экспорт
</v-btn>
```

### Отображение данных

```vue
<v-card class="mb-4">
  <v-card-title>Квартал {{ selectedQuarter }}</v-card-title>
  <v-card-text>
    <div class="text-h4">{{ report.total_income }} ₽</div>
    <div class="text-subtitle-1">Общий доход</div>
  </v-card-text>
</v-card>

<v-data-table
  :headers="headers"
  :items="report.rooms_stats"
  no-data-text="Нет данных"
/>
```

---

## Общие паттерны

### Composition API Setup

Все компоненты используют `<script setup>`:

```vue
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const items = ref([])
const loading = ref(false)
const dialog = ref(false)
const form = ref({})

const loadItems = async () => {
  loading.value = true
  try {
    const response = await api.get('/items/')
    items.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadItems()
})
</script>
```

### Error Handling

```javascript
try {
  await api.post('/items/', formData)
  // Success
  dialog.value = false
  loadItems()
} catch (error) {
  errorMessage.value = error.response?.data?.detail || 'Ошибка'
}
```

### Form Reset

```javascript
const resetForm = () => {
  form.value = {
    field1: '',
    field2: '',
    // ...
  }
}
```

---

## Best Practices

### 1. Reactivity

```javascript
// ✅ Правильно
const items = ref([])
const count = computed(() => items.value.length)

// ❌ Неправильно
let items = []
```

### 2. Async/Await

```javascript
// ✅ Правильно
const loadData = async () => {
  try {
    const response = await api.get('/data/')
    data.value = response.data
  } catch (error) {
    handleError(error)
  }
}

// ❌ Неправильно
api.get('/data/').then(r => data.value = r.data)
```

### 3. Component Organization

```vue
<script setup>
// 1. Imports
import { ref } from 'vue'

// 2. Props/Emits
const props = defineProps({...})
const emit = defineEmits([...])

// 3. Reactive state
const items = ref([])

// 4. Computed
const filteredItems = computed(...)

// 5. Methods
const loadItems = async () => {...}

// 6. Lifecycle
onMounted(() => {...})
</script>
```

---

## Следующие шаги

- [Маршрутизация](routing.md)
- [State Management](state.md)
- [API Integration](api-integration.md)


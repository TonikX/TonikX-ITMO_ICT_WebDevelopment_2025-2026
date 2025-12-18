// Конфигурация API
const API_BASE_URL = 'http://127.0.0.1:8000';
let currentToken = localStorage.getItem('token');
let currentUser = null;

async function testAPI() {
    try {
        const test = await apiRequest('/api/rooms/');
        console.log('API работает:', test);
        return true;
    } catch (error) {
        console.error('API не работает:', error);

        // Пробуем получить публичные данные
        try {
            const publicResponse = await fetch(`${API_BASE_URL}/api/rooms/`);
            console.log('Публичный запрос:', publicResponse);
        } catch (e) {
            console.error('Публичный запрос тоже не работает:', e);
        }
        return false;
    }
}

// Добавьте вызов при загрузке
document.addEventListener('DOMContentLoaded', async function() {
    console.log('Загрузка приложения...');

    // Проверяем авторизацию
    if (currentToken) {
        console.log('Токен найден:', currentToken.substring(0, 10) + '...');
        await loadCurrentUser();
        showSection('dashboard');
    } else {
        console.log('Токен не найден, показываем авторизацию');
        showSection('auth');
    }

    // Тестируем API
    await testAPI();
});

// Утилиты
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Для совместимости со старым кодом (если нужно)
window.API_BASE_URL = API_BASE_URL;
window.getCookie = getCookie;

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    console.log('Hotel Management System with Vuetify loaded');

    // Проверяем совместимость с Vue
    if (typeof Vue === 'undefined') {
        console.error('Vue.js не загружен. Проверьте подключение CDN.');
        alert('Ошибка загрузки Vue.js. Пожалуйста, проверьте подключение к интернету.');
    }

    if (typeof Vuetify === 'undefined') {
        console.error('Vuetify не загружен. Проверьте подключение CDN.');
        alert('Ошибка загрузки Vuetify. Пожалуйста, проверьте подключение к интернету.');
    }
});


function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    // Для сессионной аутентификации
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // Добавляем токен только если он есть
    if (currentToken) {
        headers['Authorization'] = `Token ${currentToken}`;
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers: headers,
            credentials: 'include'  // Важно для сессионной аутентификации
        });

        // Проверяем, что ответ JSON, а не HTML
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Сервер вернул не JSON ответ');
        }

        if (response.status === 401) {
            logout();
            throw new Error('Требуется авторизация');
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || error.message || `Ошибка ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error, 'URL:', url);
        showNotification(error.message, 'error');
        throw error;
    }
}

// Авторизация
async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showNotification('Заполните все поля', 'error');
        return;
    }

    try {
        const data = await apiRequest('/auth/token/login/', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        currentToken = data.auth_token;
        localStorage.setItem('token', currentToken);

        // Получаем информацию о пользователе
        await loadCurrentUser();
        showNotification('Успешный вход!', 'success');
        showSection('dashboard');
    } catch (error) {
        console.error('Login error:', error);
    }
}

async function register() {
    const email = document.getElementById('regEmail').value;
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const passwordConfirm = document.getElementById('regPasswordConfirm').value;
    const isStaff = document.getElementById('regIsStaff').checked;

    if (!email || !username || !password) {
        showNotification('Заполните все обязательные поля', 'error');
        return;
    }

    if (password !== passwordConfirm) {
        showNotification('Пароли не совпадают', 'error');
        return;
    }

    try {
        await apiRequest('/auth/users/', {
            method: 'POST',
            body: JSON.stringify({
                email,
                username,
                password,
                is_hotel_staff: isStaff
            })
        });

        showNotification('Регистрация успешна! Теперь войдите в систему.', 'success');
        showAuthTab('login');

        // Очищаем форму
        document.getElementById('regEmail').value = '';
        document.getElementById('regUsername').value = '';
        document.getElementById('regPassword').value = '';
        document.getElementById('regPasswordConfirm').value = '';
    } catch (error) {
        console.error('Registration error:', error);
    }
}

async function loadCurrentUser() {
    try {
        const userData = await apiRequest('/auth/users/me/');
        currentUser = userData;

        document.getElementById('currentUserEmail').textContent = userData.email;
        document.getElementById('userInfo').style.display = 'flex';

        // Показываем меню для авторизованных пользователей
        document.getElementById('authLink').style.display = 'none';
        document.getElementById('dashboardLink').style.display = 'flex';
        document.getElementById('roomsLink').style.display = 'flex';
        document.getElementById('clientsLink').style.display = 'flex';
        document.getElementById('staffLink').style.display = 'flex';
        document.getElementById('reportsLink').style.display = 'flex';
        document.getElementById('logoutLink').style.display = 'flex';

        // Заполняем форму профиля
        document.getElementById('profileUsername').value = userData.username || '';

        const profileInfo = document.getElementById('profileInfo');
        profileInfo.innerHTML = `
            <p><strong>Email:</strong> ${userData.email}</p>
            <p><strong>Статус:</strong> ${userData.is_staff ? 'Администратор' : 'Пользователь'}</p>
        `;

        // Загружаем дашборд
        await loadDashboard();
    } catch (error) {
        console.error('Error loading user:', error);
    }
}

async function updateProfile() {
    const username = document.getElementById('profileUsername').value;
    const password = document.getElementById('profilePassword').value;

    const updateData = { username };
    if (password) {
        updateData.password = password;
    }

    try {
        await apiRequest('/auth/users/me/', {
            method: 'PUT',
            body: JSON.stringify(updateData)
        });

        showNotification('Профиль обновлён', 'success');
        await loadCurrentUser();
    } catch (error) {
        console.error('Profile update error:', error);
    }
}

function logout() {
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('token');

    // Скрываем меню
    document.getElementById('authLink').style.display = 'flex';
    document.getElementById('dashboardLink').style.display = 'none';
    document.getElementById('roomsLink').style.display = 'none';
    document.getElementById('clientsLink').style.display = 'none';
    document.getElementById('staffLink').style.display = 'none';
    document.getElementById('reportsLink').style.display = 'none';
    document.getElementById('logoutLink').style.display = 'none';
    document.getElementById('userInfo').style.display = 'none';

    showSection('auth');
    showNotification('Вы вышли из системы', 'info');
}

// Навигация
function showSection(sectionId) {
    // Скрываем все секции
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });

    // Показываем выбранную секцию
    const section = document.getElementById(sectionId + 'Section');
    if (section) {
        section.style.display = 'block';

        // Загружаем данные для секции
        switch(sectionId) {
            case 'dashboard':
                loadDashboard();
                break;
            case 'rooms':
                loadRooms();
                loadRoomTypes();
                break;
            case 'clients':
                loadClients();
                break;
            case 'staff':
                loadStaff();
                loadUsersForStaff();
                break;
            case 'reports':
                break;
        }
    }
}

function showAuthTab(tabName) {
    // Скрываем все формы
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('profileForm').style.display = 'none';

    // Убираем активный класс со всех кнопок
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Показываем выбранную форму
    document.getElementById(tabName + 'Form').style.display = 'block';

    // Делаем кнопку активной
    event.target.classList.add('active');

    // Для вкладки профиля нужна авторизация
    if (tabName === 'profile' && !currentToken) {
        showNotification('Требуется авторизация', 'error');
        showAuthTab('login');
    }
}

// Дашборд
async function loadDashboard() {
    if (!currentToken) return;

    try {
        // Загружаем статистику
        const rooms = await apiRequest('/api/rooms/');
        const clients = await apiRequest('/api/clients/');
        const staff = await apiRequest('/api/staff/');

        document.getElementById('roomsCount').textContent = rooms.length;
        document.getElementById('clientsCount').textContent = clients.length;
        document.getElementById('staffCount').textContent = staff.length;
    } catch (error) {
        console.error('Dashboard load error:', error);
    }
}

// Управление номерами
let currentRoomId = null;

async function loadRooms() {
    try {
        const rooms = await apiRequest('/api/rooms/');
        const tableBody = document.getElementById('roomsTableBody');
        tableBody.innerHTML = '';

        rooms.forEach(room => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${room.room_number}</td>
                <td>${room.floor}</td>
                <td>${room.room_type_name || room.room_type}</td>
                <td>${room.has_phone ? '✓' : '✗'}</td>
                <td>
                    <span class="status ${room.is_available ? 'available' : 'occupied'}">
                        ${room.is_available ? 'Свободен' : 'Занят'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="editRoom(${room.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteRoom(${room.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}

async function loadRoomTypes() {
    try {
        const roomTypes = await apiRequest('/api/room-types/');
        const select = document.getElementById('roomType');
        select.innerHTML = '<option value="">Выберите тип номера</option>';

        roomTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            option.textContent = `${type.name} (${type.price_per_night} руб./сут.)`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading room types:', error);
    }
}

function showRoomForm(roomId = null) {
    currentRoomId = roomId;
    const form = document.getElementById('roomForm');
    const title = document.getElementById('roomFormTitle');

    if (roomId) {
        title.textContent = 'Редактирование номера';
        // Загружаем данные комнаты
        loadRoomData(roomId);
    } else {
        title.textContent = 'Добавление номера';
        // Очищаем форму
        document.getElementById('roomNumber').value = '';
        document.getElementById('roomFloor').value = '';
        document.getElementById('roomType').value = '';
        document.getElementById('roomHasPhone').checked = true;
        document.getElementById('roomIsAvailable').checked = true;
    }

    form.style.display = 'block';
}

async function loadRoomData(roomId) {
    try {
        const room = await apiRequest(`/api/rooms/${roomId}/`);
        document.getElementById('roomNumber').value = room.room_number;
        document.getElementById('roomFloor').value = room.floor;
        document.getElementById('roomType').value = room.room_type;
        document.getElementById('roomHasPhone').checked = room.has_phone;
        document.getElementById('roomIsAvailable').checked = room.is_available;
    } catch (error) {
        console.error('Error loading room data:', error);
    }
}

async function saveRoom() {
    const roomData = {
        room_number: document.getElementById('roomNumber').value,
        floor: parseInt(document.getElementById('roomFloor').value),
        room_type: parseInt(document.getElementById('roomType').value),
        has_phone: document.getElementById('roomHasPhone').checked,
        is_available: document.getElementById('roomIsAvailable').checked
    };

    try {
        if (currentRoomId) {
            await apiRequest(`/api/rooms/${currentRoomId}/`, {
                method: 'PUT',
                body: JSON.stringify(roomData)
            });
            showNotification('Номер обновлён', 'success');
        } else {
            await apiRequest('/api/rooms/', {
                method: 'POST',
                body: JSON.stringify(roomData)
            });
            showNotification('Номер добавлен', 'success');
        }

        cancelRoomForm();
        loadRooms();
        loadDashboard();
    } catch (error) {
        console.error('Error saving room:', error);
    }
}

function cancelRoomForm() {
    document.getElementById('roomForm').style.display = 'none';
    currentRoomId = null;
}

async function deleteRoom(roomId) {
    if (!confirm('Вы уверены, что хотите удалить этот номер?')) return;

    try {
        await apiRequest(`/api/rooms/${roomId}/`, {
            method: 'DELETE'
        });

        showNotification('Номер удалён', 'success');
        loadRooms();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting room:', error);
    }
}

async function getAvailableRooms() {
    try {
        const data = await apiRequest('/api/rooms/available_rooms/');
        document.getElementById('availableRoomsCount').textContent = data.available_rooms;
    } catch (error) {
        console.error('Error getting available rooms:', error);
    }
}

async function getRoomsByFloor() {
    try {
        const data = await apiRequest('/api/rooms/rooms_by_floor/');
        const container = document.getElementById('roomsByFloor');
        container.innerHTML = '';

        data.forEach(item => {
            const div = document.createElement('div');
            div.textContent = `Этаж ${item.floor}: ${item.count} номеров`;
            container.appendChild(div);
        });
    } catch (error) {
        console.error('Error getting rooms by floor:', error);
    }
}

// Управление клиентами
let currentClientId = null;

async function loadClients() {
    try {
        const clients = await apiRequest('/api/clients/');
        const tableBody = document.getElementById('clientsTableBody');
        tableBody.innerHTML = '';

        clients.forEach(client => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${client.last_name} ${client.first_name} ${client.middle_name}</td>
                <td>${client.passport_number}</td>
                <td>${client.city}</td>
                <td>${new Date(client.check_in_date).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="editClient(${client.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteClient(${client.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading clients:', error);
    }
}

function showClientForm(clientId = null) {
    currentClientId = clientId;
    const form = document.getElementById('clientForm');
    const title = document.getElementById('clientFormTitle');

    if (clientId) {
        title.textContent = 'Редактирование клиента';
        loadClientData(clientId);
    } else {
        title.textContent = 'Добавление клиента';
        document.getElementById('clientLastName').value = '';
        document.getElementById('clientFirstName').value = '';
        document.getElementById('clientMiddleName').value = '';
        document.getElementById('clientPassport').value = '';
        document.getElementById('clientCity').value = '';
    }

    form.style.display = 'block';
}

async function loadClientData(clientId) {
    try {
        const client = await apiRequest(`/api/clients/${clientId}/`);
        document.getElementById('clientLastName').value = client.last_name;
        document.getElementById('clientFirstName').value = client.first_name;
        document.getElementById('clientMiddleName').value = client.middle_name;
        document.getElementById('clientPassport').value = client.passport_number;
        document.getElementById('clientCity').value = client.city;
    } catch (error) {
        console.error('Error loading client data:', error);
    }
}

async function saveClient() {
    const clientData = {
        last_name: document.getElementById('clientLastName').value,
        first_name: document.getElementById('clientFirstName').value,
        middle_name: document.getElementById('clientMiddleName').value,
        passport_number: document.getElementById('clientPassport').value,
        city: document.getElementById('clientCity').value
    };

    try {
        if (currentClientId) {
            await apiRequest(`/api/clients/${currentClientId}/`, {
                method: 'PUT',
                body: JSON.stringify(clientData)
            });
            showNotification('Клиент обновлён', 'success');
        } else {
            await apiRequest('/api/clients/', {
                method: 'POST',
                body: JSON.stringify(clientData)
            });
            showNotification('Клиент добавлен', 'success');
        }

        cancelClientForm();
        loadClients();
        loadDashboard();
    } catch (error) {
        console.error('Error saving client:', error);
    }
}

function cancelClientForm() {
    document.getElementById('clientForm').style.display = 'none';
    currentClientId = null;
}

async function deleteClient(clientId) {
    if (!confirm('Вы уверены, что хотите удалить этого клиента?')) return;

    try {
        await apiRequest(`/api/clients/${clientId}/`, {
            method: 'DELETE'
        });

        showNotification('Клиент удалён', 'success');
        loadClients();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting client:', error);
    }
}

async function searchClientsByCity() {
    const city = document.getElementById('clientSearch').value;
    if (!city) {
        loadClients();
        return;
    }

    try {
        const data = await apiRequest(`/api/clients/from_city/?city=${encodeURIComponent(city)}`);
        showNotification(`Клиентов из ${city}: ${data.count}`, 'info');
    } catch (error) {
        console.error('Error searching clients:', error);
    }
}

// Управление сотрудниками
let currentStaffId = null;

async function loadStaff() {
    try {
        const staff = await apiRequest('/api/staff/');
        const tableBody = document.getElementById('staffTableBody');
        tableBody.innerHTML = '';

        staff.forEach(employee => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${employee.last_name} ${employee.first_name} ${employee.middle_name}</td>
                <td>${employee.user_email || employee.user}</td>
                <td>
                    <span class="status ${employee.is_active ? 'active' : 'inactive'}">
                        ${employee.is_active ? 'Работает' : 'Уволен'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="editStaff(${employee.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm ${employee.is_active ? 'btn-warning' : 'btn-success'}"
                            onclick="${employee.is_active ? 'fireStaff' : 'hireStaff'}(${employee.id})">
                        <i class="fas ${employee.is_active ? 'fa-user-times' : 'fa-user-check'}"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading staff:', error);
    }
}

async function loadUsersForStaff() {
    try {
        const users = await apiRequest('/auth/users/');
        const select = document.getElementById('staffUser');
        select.innerHTML = '<option value="">Выберите пользователя</option>';

        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user.id;
            option.textContent = `${user.email} (${user.username})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

function showStaffForm(staffId = null) {
    currentStaffId = staffId;
    const form = document.getElementById('staffForm');
    const title = document.getElementById('staffFormTitle');

    if (staffId) {
        title.textContent = 'Редактирование сотрудника';
        loadStaffData(staffId);
    } else {
        title.textContent = 'Добавление сотрудника';
        document.getElementById('staffLastName').value = '';
        document.getElementById('staffFirstName').value = '';
        document.getElementById('staffMiddleName').value = '';
        document.getElementById('staffUser').value = '';
        document.getElementById('staffIsActive').checked = true;
    }

    form.style.display = 'block';
}

async function loadStaffData(staffId) {
    try {
        const staff = await apiRequest(`/api/staff/${staffId}/`);
        document.getElementById('staffLastName').value = staff.last_name;
        document.getElementById('staffFirstName').value = staff.first_name;
        document.getElementById('staffMiddleName').value = staff.middle_name;
        document.getElementById('staffUser').value = staff.user;
        document.getElementById('staffIsActive').checked = staff.is_active;
    } catch (error) {
        console.error('Error loading staff data:', error);
    }
}

async function saveStaff() {
    const staffData = {
        last_name: document.getElementById('staffLastName').value,
        first_name: document.getElementById('staffFirstName').value,
        middle_name: document.getElementById('staffMiddleName').value,
        user: parseInt(document.getElementById('staffUser').value),
        is_active: document.getElementById('staffIsActive').checked
    };

    try {
        if (currentStaffId) {
            await apiRequest(`/api/staff/${currentStaffId}/`, {
                method: 'PUT',
                body: JSON.stringify(staffData)
            });
            showNotification('Сотрудник обновлён', 'success');
        } else {
            await apiRequest('/api/staff/', {
                method: 'POST',
                body: JSON.stringify(staffData)
            });
            showNotification('Сотрудник добавлен', 'success');
        }

        cancelStaffForm();
        loadStaff();
        loadDashboard();
    } catch (error) {
        console.error('Error saving staff:', error);
    }
}

function cancelStaffForm() {
    document.getElementById('staffForm').style.display = 'none';
    currentStaffId = null;
}

async function hireStaff(staffId) {
    try {
        await apiRequest(`/api/staff/${staffId}/hire/`, {
            method: 'POST'
        });
        showNotification('Сотрудник принят на работу', 'success');
        loadStaff();
    } catch (error) {
        console.error('Error hiring staff:', error);
    }
}

async function fireStaff(staffId) {
    if (!confirm('Вы уверены, что хотите уволить этого сотрудника?')) return;

    try {
        await apiRequest(`/api/staff/${staffId}/fire/`, {
            method: 'POST'
        });
        showNotification('Сотрудник уволен', 'warning');
        loadStaff();
    } catch (error) {
        console.error('Error firing staff:', error);
    }
}

async function loadStaffWithServices() {
    try {
        const staff = await apiRequest('/api/staff/');
        const modalContent = document.getElementById('staffServicesContent');
        modalContent.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i><p>Загрузка...</p></div>';

        document.getElementById('staffServicesModal').style.display = 'block';

        let html = '<div class="staff-services-list">';
        for (const employee of staff) {
            try {
                const services = await apiRequest(`/api/staff/${employee.id}/with_services/`);
                html += `
                    <div class="staff-service-item">
                        <h4>${employee.last_name} ${employee.first_name}</h4>
                        <div class="services-list">
                            ${services.staff_services && services.staff_services.length > 0
                                ? services.staff_services.map(s =>
                                    `<div class="service-item">${s.service_name}</div>`
                                  ).join('')
                                : '<p>Нет назначенных услуг</p>'
                            }
                        </div>
                    </div>
                `;
            } catch (error) {
                html += `<div class="staff-service-item">
                    <h4>${employee.last_name} ${employee.first_name}</h4>
                    <p class="error">Ошибка загрузки услуг</p>
                </div>`;
            }
        }
        html += '</div>';

        modalContent.innerHTML = html;
    } catch (error) {
        console.error('Error loading staff with services:', error);
        document.getElementById('staffServicesContent').innerHTML =
            '<p class="error">Ошибка загрузки данных</p>';
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Отчёты
async function generateQuarterlyReport() {
    const year = document.getElementById('reportYear').value;
    const quarter = document.getElementById('reportQuarter').value;

    try {
        const report = await apiRequest(`/api/stays/quarterly_report/?year=${year}&quarter=${quarter}`);
        const resultDiv = document.getElementById('quarterlyReportResult');

        let html = `
            <div class="report-result">
                <h4>Отчёт за ${year} год, ${quarter} квартал</h4>
                <p><strong>Общий доход:</strong> ${report.total_income || 0} руб.</p>
                <p><strong>Всего клиентов:</strong> ${report.total_clients || 0}</p>

                <h5>Статистика по номерам:</h5>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Номер</th>
                                <th>Тип</th>
                                <th>Клиентов</th>
                                <th>Доход</th>
                            </tr>
                        </thead>
                        <tbody>
        `;

        if (report.room_statistics && report.room_statistics.length > 0) {
            report.room_statistics.forEach(stat => {
                html += `
                    <tr>
                        <td>${stat['room__room_number'] || 'N/A'}</td>
                        <td>${stat['room__room_type__name'] || 'N/A'}</td>
                        <td>${stat.client_count || 0}</td>
                        <td>${stat.total_income || 0} руб.</td>
                    </tr>
                `;
            });
        } else {
            html += '<tr><td colspan="4">Нет данных</td></tr>';
        }

        html += `
                        </tbody>
                    </table>
                </div>

                <h5>Номера по этажам:</h5>
                <div class="rooms-by-floor">
        `;

        if (report.rooms_by_floor && report.rooms_by_floor.length > 0) {
            report.rooms_by_floor.forEach(item => {
                html += `<p>Этаж ${item.floor}: ${item.room_count || 0} номеров</p>`;
            });
        } else {
            html += '<p>Нет данных</p>';
        }

        html += `</div></div>`;

        resultDiv.innerHTML = html;
        showNotification('Отчёт сформирован', 'success');
    } catch (error) {
        console.error('Error generating report:', error);
    }
}

async function getClientsByCity() {
    const city = document.getElementById('citySearch').value;
    if (!city) {
        showNotification('Введите город', 'error');
        return;
    }

    try {
        const data = await apiRequest(`/api/clients/from_city/?city=${encodeURIComponent(city)}`);
        const resultDiv = document.getElementById('cityClientsResult');
        resultDiv.innerHTML = `
            <div class="city-result">
                <p><strong>Город:</strong> ${data.city}</p>
                <p><strong>Количество клиентов:</strong> ${data.count}</p>
            </div>
        `;
    } catch (error) {
        console.error('Error getting clients by city:', error);
    }
}

async function getCleanerForClient() {
    const clientId = document.getElementById('clientForCleaner').value;
    const day = document.getElementById('cleanerDay').value;

    try {
        const data = await apiRequest(`/api/cleaning-schedule/cleaner_for_client_room/?client_id=${clientId}&day_of_week=${day}`);
        const resultDiv = document.getElementById('cleanerResult');

        if (data.error) {
            resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <div class="cleaner-result">
                    <p><strong>Уборщик:</strong> ${data.staff_name || 'N/A'}</p>
                    <p><strong>Этаж:</strong> ${data.floor || 'N/A'}</p>
                    <p><strong>День недели:</strong> ${data.day_of_week_display || data.day_of_week}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error getting cleaner:', error);
        document.getElementById('cleanerResult').innerHTML =
            '<p class="error">Ошибка при поиске уборщика</p>';
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем авторизацию
    if (currentToken) {
        loadCurrentUser();
        showSection('dashboard');
    } else {
        showSection('auth');
    }

    // Загружаем данные для аналитики
    if (currentToken) {
        getAvailableRooms();
        getRoomsByFloor();
    }
});

// Вспомогательные функции для редактирования
function editRoom(id) {
    showRoomForm(id);
    window.scrollTo(0, document.getElementById('roomForm').offsetTop);
}

function editClient(id) {
    showClientForm(id);
    window.scrollTo(0, document.getElementById('clientForm').offsetTop);
}

function editStaff(id) {
    showStaffForm(id);
    window.scrollTo(0, document.getElementById('staffForm').offsetTop);
}
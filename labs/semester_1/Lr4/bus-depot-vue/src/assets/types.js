export const titles = {
    'bus-types': 'Типы автобусов',
    'buses': 'Автобусы',
    'routes': 'Маршруты',
    'drivers': 'Водители',
    'driver-assignments': 'Назначения водителей',
    'bus-statuses': 'Статусы автобусов'
}

export const foreignKeys = {
    'bus-types': [],
    'buses': [['bus_type', 'bus_types']],
    'routes': [],
    'drivers': [['main_bus', 'buses'], ['main_route', 'routes']],
    'driver-assignments': [['driver', 'drivers'], ['bus', 'buses'], ['route', 'routes']],
    'bus-statuses': [['bus', 'buses']], 
}

export const foreignKeys2 = {
    'bus-types': {},
    'buses': {
        'bus_type': 'bus_types',
    },
    'routes': {},
    'drivers': {
        'main_bus': 'buses',
        'main_route': 'routes',
    },
    'driver-assignments': {
        'driver': 'drivers',
        'bus': 'buses',
        'route': 'routes',
    },
    'bus-statuses': {
        'bus': 'buses',
    },
}

export const fields = {
    'bus-types': ['name', 'capacity'],
    'buses': ['license_plate', 'bus_type', 'is_active', 'purchase_date'],
    'routes': ['number', 'start_point', 'end_point', 'start_time', 'end_time', 'interval', 'duration'],
    'drivers': ['full_name', 'passport', 'birth_date', 'driver_class', 'experience', 'salary', 'main_bus', 'main_route'],
    'driver-assignments': ['driver', 'bus', 'route', 'date', 'start_time', 'end_time'],
    'bus-statuses': ['bus', 'date', 'status', 'reason'],
}

export const choices = {
    'driver_class': ['1', '2', '3'],
    'status': ['active', 'not_active', 'broken', 'no_driver']
}

export const namingFunctions = {
    'bus-types': async (data) => {
        return `${data.name} (число мест: ${data.capacity})`
    },
    'buses': async (data) => {
        return `${data.license_plate} ` +
                `(${await getForeignField('bus-types', data.bus_type, 'name')})`
    },
    'routes': async (data) => {
        return `${data.number} (${data.start_point} - ${data.end_point})`
    },
    'drivers': async (data) => {
        return `${data.full_name} ` +
               `(автобус: ${await getForeignField('buses', data.main_bus, 'license_plate')}, ` +
               `маршрут: ${await getForeignField('routes', data.main_route, 'number')})`
    },
    'driver-assignments': async (data) => {
        return `${await getForeignField('drivers', data.driver, 'full_name')} на ` +
                `${await getBusName(data.bus)} | ${data.date}`
    },
    'bus-statuses': async (data) => {
        return `${await getBusName(data.bus)} - ${data.status} | ${data.date}`
    }
}

async function getObject(type, id) {
    try {
        const token = localStorage.getItem('auth_token');
        if (!token) return null

        const response = await fetch(`http://127.0.0.1:8000/bus-depot/${type}/${id}`, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        return data;
    } catch {
        return null;
    }
}

async function getForeignField(type, id, field) {
    const data = await getObject(type, id);
    if (!data) return id;
    return data[field];
}

async function getBusName(id) {
    const data = await getObject('buses', id)
    if (!data) return id;
    return `${data.license_plate} (${await getForeignField('bus-types', data.bus_type, 'name')})`
}

export async function getObjectName(type, id) {
    const data = await getObject(type, id)
    const name = await namingFunctions[type](data)
    return name
}

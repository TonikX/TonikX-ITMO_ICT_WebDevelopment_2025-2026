## Работа с серверной частью. Сервисный слой (Services)

Для организации взаимодействия клиентского приложения с серверной частью был реализован сервисный слой, представленный
набором JavaScript-файлов в директории services.

Каждый сервис инкапсулирует HTTP-запросы к соответствующему API серверной части и отвечает за работу с конкретной
сущностью предметной области.

### Назначение сервисного слоя

Сервисный слой выполняет следующие функции:

* изолирует логику HTTP-запросов от Vue-компонентов;
* обеспечивает единообразный способ взаимодействия с REST API;
* повышает читаемость и поддерживаемость кода;
* упрощает повторное использование запросов в разных частях приложения.

Все запросы реализованы с использованием библиотеки Axios.

### Структура сервисов

В проекте реализованы следующие сервисы:

| Сервис | Назначение | Основные методы |
|--------|------------|-----------------|
| **authService.js** | Управление аутентификацией и пользователями | `login()`, `register()`, `getCurrentUser()`, `logout()`, `updateProfile()` |
| **objectsService.js** | Управление объектами (парками) | `getObjects()`, `getObjectById()`, `createObject()`, `updateObject()`, `deleteObject()` |
| **objectZoneService.js** | Работа с зонами объектов | `getObjectZones()`, `createZone()`, `updateZone()`, `deleteZone()`, `getZoneById()` |
| **plantService.js** | Управление растениями | `getPlantsByObject()`, `getPlantById()`, `createPlant()`, `updatePlant()`, `deletePlant()`, `createPlantPlacement()` |
| **speciesService.js** | Работа с видами растений | `getSpecies()`, `getSpeciesById()`, `createSpecies()`, `updateSpecies()`, `deleteSpecies()` |
| **wateringService.js** | Управление графиками полива | `getPlantWateringSchedules()`, `createWateringSchedule()`, `updateWateringSchedule()`, `deleteWateringSchedule()` |
| **workerService.js** | Управление информацией о сотрудниках | `getAllWorkers()`, `getWorkerById()`, `createWorker()`, `updateWorker()`, `deleteWorker()` |
| **plantWorkerService.js** | Связь растений и работников | `getPlantWorkerAssignments()`, `createPlantWorkerAssignment()`, `updatePlantWorkerAssignment()`, `deletePlantWorkerAssignment()`, `getObjectWorkers()` |
| **contractsService.js** | Управление сервисными контрактами | `getContractsByObject()`, `createContract()`, `updateContract()`, `deleteContract()`, `getContractById()` |
| **enterprisesService.js** | Работа с предприятиями | `getEnterprises()`, `getEnterpriseById()`, `createEnterprise()`, `updateEnterprise()`, `deleteEnterprise()` |

### Принципы реализации сервисов

Каждый сервис:

* экспортирует набор асинхронных функций;
* использует axios для выполнения HTTP-запросов;
* передаёт токен авторизации через HTTP-заголовок Authorization;
* возвращает данные ответа сервера без дополнительной обработки.

Пример типового запроса:

```js
axios.get(url, {
  headers: {
    Authorization: `Token ${token}`,
  },
});
```

### Использование сервисов в компонентах

Сервисы используются во Vue-компонентах и Pinia-хранилищах:

* для загрузки данных при инициализации компонентов;
* при выполнении действий пользователя (создание, редактирование, удаление);
* при обновлении интерфейса после изменений данных.
* Такой подход позволяет отделить бизнес-логику от логики представления, что соответствует лучшим практикам разработки клиентских приложений.
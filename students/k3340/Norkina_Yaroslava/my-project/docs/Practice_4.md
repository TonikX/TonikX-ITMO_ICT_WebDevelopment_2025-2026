Практическая работа №4

Часть 2.

Создадим папку для лабораторной работы №4 и активируем виртуальное окружение

.\\.venv\\Scripts\\activate

<img width="974" height="113" alt="image" src="https://github.com/user-attachments/assets/0cb8fcdc-3edb-496e-8ba8-a78585e225b3" />


Для начала необходимо установить node.js и npm.

<img width="974" height="477" alt="image" src="https://github.com/user-attachments/assets/71dd290b-3078-4821-b771-56bcde1601df" />

<img width="636" height="300" alt="image" src="https://github.com/user-attachments/assets/9d488542-0f2e-474f-af40-4e471ac020eb" />

<img width="636" height="276" alt="image" src="https://github.com/user-attachments/assets/5aaa59ea-64f0-4165-836f-6752cba0e629" />


Для установки vue требуется выполнить следующую команду в терминале:

<table><tbody><tr><td><p>$ npm install -g @vue/cli</p></td></tr></tbody></table>

Теперь, когда vue ٧и vue-cli глобально установлены, можно приступать к инициализации проекта:

npm init vue@latest

<img width="974" height="128" alt="image" src="https://github.com/user-attachments/assets/dead0c1a-cd58-46bf-8f1b-199dd8e0b88f" />


Следуем инструкциям по установке пакетов от утилиты CLI:

<img width="974" height="481" alt="image" src="https://github.com/user-attachments/assets/32f55979-d586-42df-9419-4f729a8b971f" />


Первоначальный проект создан

Выполним команды:

cd practice\_4

npm install \\\\Установить зависимости

npm run dev \\\\Запустить проект

В случае удачного запуска в консоли отобразится адрес, на котором запустился проект:

<img width="562" height="140" alt="image" src="https://github.com/user-attachments/assets/a843382d-26dd-42a1-b232-8cd17a45a698" />


<img width="974" height="555" alt="image" src="https://github.com/user-attachments/assets/528fdadc-4964-42bf-8e3e-62da32d3adf4" />


Далее установим vue.js devtools. Это расширение позволяет просматривать состав компонентов и данные в них.

<img width="644" height="321" alt="image" src="https://github.com/user-attachments/assets/989cd59a-3c5d-49ea-86f6-d3de53052e26" />


Компоненты, роутинг

**Клиентский роутинг** – используется в SPA (одностраничных приложениях). Сервер отдаёт один HTML-файл, а JavaScript на стороне клиента управляет URL и подгружает нужные «страницы» (на самом деле, компоненты) динамически, без полной перезагрузки.

Необходимо создать отдельный компонент src/components/Hello.vue, чтобы разобраться с тем, как работает компонентный подход.

<img width="536" height="452" alt="image" src="https://github.com/user-attachments/assets/4e4f34c7-2ea3-494f-a7cd-a6ebf8702867" />


Создание роутера

В файле конфигурации роутера (src/router/index.js) есть массив со всеми путями, которые используются в приложении. Добавим созданный компонент

import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'

import Hello from "@/components/Hello.vue";

const routes = \[  // массив с роутами

   // отдельный роут:  

   {

       path: '/hi', // конкретный url-адрес

       component: Hello // Ссылка на компонент

   },

\]

const router = createRouter({

   history: createWebHistory(), routes

})

export default router

Файл src/main.js:

import { createApp } from 'vue'  
import App from './App.vue'  
import './assets/main.css'  
import router from "./router";

createApp(App).use(router).mount('#app')

Роутер необходимо встроить в файл App.vue (файл src/App.vue)

<img width="620" height="403" alt="image" src="https://github.com/user-attachments/assets/1093d508-af1d-4141-8d1b-0e0cc89ff144" />


Запуск первого компонента

Переходим по ссылке http://localhost:5173/hi после запуска проекта:

<img width="974" height="482" alt="image" src="https://github.com/user-attachments/assets/2392c963-0648-4b4a-9f02-64b7b767b875" />


Разделение компонентов на view и components

**_Представление в Vue.js_** — это компонент, который ссылается на фактическую страницу, с которой работает пользователь.

**Что такое компонент в Vue.js?** Компонент — это и представление Vue, и компонент по техническому использованию. Компонент определяет что-то, что можно использовать повторно быть и может сохранено в src/components. Например, компонент может быть заголовком, нижним колонтитулом, рекламой, таблицей, текстовыми полями или кнопками. Затем можно получить доступ к одному или нескольким компонентам внутри представления, например, к верхнему и нижнему колонтитулу.

Компонент представления Vue является **страницей**, а компонент относится к чему-то, что можно использовать повторно и можно использовать в представлении.

Компоненты разбиты по разным папкам для представлений и компонентов, чтобы упростить работу с кодовой базой.

*   Компонент представлений Vue относится к страницам, на которые может переходить пользователь. Представления Vue также могут использовать компоненты из папки компонентов, такие как AppHeader.vue и AppFooter.vue.
*   Папка компонентов относится к компонентам, которые можно повторно использовать в проекте, а также можно использовать для создания компонентов представлений Vue.

Теперь, когда известно, что компонент представления может содержать другие компоненты, можно приступить к еще большему разделению проекта.

Создание компонентов и представления для получения и отображения данных

Весь код компоненты или представления во Vue логически можно разделить на три части: template, script, style. Template отвечает за вёрстку, html-код. Script — за все скрипты, которые используются для добавления какой-либо логики (запросы к API, вывод информации и так далее). Style — за все стили компоненты.

Код представления с комментариями (файл src/views/Warriors.vue).

<img width="974" height="607" alt="image" src="https://github.com/user-attachments/assets/4656a968-6c1f-4801-89a1-7858da21255c" />


Создание компонента получения данных

<img width="974" height="489" alt="image" src="https://github.com/user-attachments/assets/015ccf03-4cf1-4004-8fd7-3717f84b5c50" />


Добавление новой страницы (маршрута) в роутер:

<img width="974" height="426" alt="image" src="https://github.com/user-attachments/assets/aefe8e89-6b28-4600-85e0-428a2e41a54d" />


Результат:

<img width="444" height="418" alt="image" src="https://github.com/user-attachments/assets/7dd20007-4056-4a1d-9c66-5e34b7f3683b" />


Часть 3.

Настройка CORS (Cross-origin resource sharing)

— механизм, использующий дополнительные HTTP-заголовки, чтобы дать возможность [агенту пользователя](https://developer.mozilla.org/ru/docs/%D0%A1%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C/User_agent) получать разрешения на доступ к выбранным ресурсам с сервера на источнике (домене), отличном от того, который использует сайт использует в данный момент. Говорят, что агент пользователя делает запрос с другого источника (cross-origin HTTP request), если источник текущего документа отличается от запрашиваемого ресурса доменом, протоколом или портом.

Механизм CORS поддерживает кросс-доменные запросы и передачу данных между браузером и web-серверами по защищенному соединению. Современные браузеры используют CORS в API-контейнерах, таких как XMLHttpRequest или Fetch, чтобы снизить риски, присущие запросам с других источников.

Стандарт CORS различает “простые” и “сложные” запросы. Простым считается запрос работающий со следующими методами:

*   HEAD
*   GET
*   POST

и заголовками:

*   Accept
*   Accept-Language
*   Content-Language
*   Last-Event-ID
*   Content-Type, но только со значениями:
    *   application/x-www-form-urlencoded
    *   multipart/form-data
    *   text/plain

Сервер, получив на обработку подобный запрос, должен прочесть Origin и решить, как его обрабатывать. Заголовок ответа Access-Control-Allow-Origin регулирует, с какого домена разрешено запрашивать данные. Это может быть как веб-адрес, так и знак астерикса (звездочки), если разрешено всем. 

Необходимо обратить внимание, что рассматривается ситуация в которой ведется взаимодействие с чужими API. С вероятностью почти 100% они работают по протоколу JSON, то есть принимают и отдают заголовок Content-Type: application/json. Такой запрос автоматически перестает быть простым и переходит в разряд “сложных”, где схема взаимодействия иная.

Сложные запросы проходят в два этапа. Сначала браузер делает запрос по тому же URL, но методом OPTIONS. Сервер должен ответить: какими другими методами и дополнительными заголовками (помимо стандартных) можно обращаться к этому урлу. И только получив разрешение, браузер сделает запрос на основной URL.

При этом браузер все запомнит: если разрешили только методы GET и POST, то PUT и DELETE не сработают. Аналогично с заголовками: если помимо стандартных разрешено использовать только Authorization, то нужно передать его и ничего другого.

Первая стадия, когда делается запрос OPTION, официально называется preflight request. Необходимо отметить, что такое взаимодействие весьма прозрачно отражается в браузере. Например, в консоли разработчика в Хроме видны оба запроса со всеми заголовками.

Настройка CORS в Django REST framework.

pip install django-cors-headers

<img width="974" height="318" alt="image" src="https://github.com/user-attachments/assets/42fb24f9-9de2-4f28-832b-e6ddae667189" />


Добавим приложение в settings.py:

<img width="404" height="460" alt="image" src="https://github.com/user-attachments/assets/432a267e-1e47-4ca8-9787-fe63eb40c313" />


Затем необходимо добавить corsheaders.middleware.CorsMiddleware в “MIDDLEWARE\_CLASSES” в settings.py (**необходимо** **добавтиь перед всеми остальными объектами**):

<img width="974" height="399" alt="image" src="https://github.com/user-attachments/assets/4c0577b4-66c1-4156-add0-21b3ca9ac0a6" />


Затем необходимо включить CORS для всех доменов, добавив следующий параметр: CORS\_ORIGIN\_ALLOW\_ALL = True

Разрешим для всех доменов.

Дополнительные параметры конфигурации:

CORS\_ALLOW\_HEADERS = \[

    'authorization',

    'content-type',

    'x-csrftoken',

    'accept',

    'origin',

    'user-agent',

    'x-requested-with',

    'XMLHttpRequest',

\]

CORS\_ALLOW\_METHODS = \[

    'DELETE',

    'GET',

    'OPTIONS',

    'PATCH',

    'POST',

    'PUT',

\]

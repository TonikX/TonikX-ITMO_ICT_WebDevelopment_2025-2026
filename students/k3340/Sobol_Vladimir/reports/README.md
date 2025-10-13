# Отчёты по WEB-программированию

## 👨‍💻 Студент
**ФИО:** Соболь Владимир Вячеславович
**Группа:** K3340  
**ИСУ:** 409594

---

## 📚 Содержание

| № | Название | Ссылка |
|---|-----------|--------|
| 1 | [Лабораторная работа №1 — Сокеты, TCP/UDP, HTTP](lab1/docs/index.md) |
| 2 | [Практическая работа №2 — Django, CRUD, Bootstrap](lab2/docs/index.md) |

---

## ⚙️ Используемые технологии

- Python 3.12  
- Django  
- MkDocs + Material  
- HTML / CSS / Bootstrap  
- Socket, threading, json  

---

## 🌐 Ссылка на GitHub Pages

👉 [https://твое_имя.github.io/TonikX-ITMO_ICT_WebDevelopment_2025-2026/students/k3340/Meshcheryakov_Daniil/report/](#)

---

## 🚀 Как запустить документацию локально

### 🏠 Главная страница (с меню):

```bash
cd reports
mkdocs serve
```

Откройте в браузере: **http://127.0.0.1:8000**

С главной страницы можно перейти на ЛР1 или ЛР2!

---

### 📝 Запуск отдельной лабораторной:

**Лабораторная №1:**
```bash
cd reports/docs/lab1
mkdocs serve
```

**Лабораторная №2:**
```bash
cd reports/docs/lab2
mkdocs serve
```

Откройте в браузере: **http://127.0.0.1:8000**

---

### 🛑 Остановить сервер:

```bash
# Найти процесс
lsof -i :8000

# Остановить (замените PID на номер процесса)
kill PID
```
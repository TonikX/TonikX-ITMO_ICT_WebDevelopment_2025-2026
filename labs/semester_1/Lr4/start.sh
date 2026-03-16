#!/bin/bash

PROJECT_ROOT="/home/vlad/github/TonikX-ITMO_ICT_WebDevelopment_2025-2026"

cleanup() {
    echo "Остановка процессов..."
    kill $DJANGO_PID $VUE_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Активация виртуального окружения..."
source "$PROJECT_ROOT/.venv/bin/activate"

echo "Запуск Django..."
cd "$PROJECT_ROOT/students/k3341/Klimenkov_Vladislav/Lr4/bus_depot_project"
python3 manage.py runserver &
DJANGO_PID=$!

sleep 2

echo "Запуск Vue..."
cd "$PROJECT_ROOT/students/k3341/Klimenkov_Vladislav/Lr4/bus-depot-vue"
npm run dev &
VUE_PID=$!

echo "Сервер и клиент запущены."

wait $DJANGO_PID $VUE_PID

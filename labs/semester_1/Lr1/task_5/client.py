import requests


class GradeClient:
    """
    Клиента для отправки POST-запросов с оценками по дисциплинам.
    """
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
    
    def add_grade(self, discipline, grade):
        """
        Формирует и отправляет POST-запрос серверу с оценкой по дисциплиной
        и выводит ответ от сервера в консоль.
        """
        data = {
            'discipline': discipline,
            'grade': grade
        }
        try:
            response = requests.post(f"{self.base_url}", data=data)
            response.encoding = 'utf-8'
            print(f"Ответ сервера: {response.text}")
        except Exception as e:
            print(f"Ошибка: {e}")

def main():
    """
    Main-функция с реализацией консольного клиента для отправки оценок по дисциплинам.
    """
    client = GradeClient()
    print("Консольный клиент для добавления оценок по дисциплинам")
    print("Команды:")
    print("  add - добавить оценку")
    print("  exit - выход")
    print()

    # Цикл работы консольного клиента
    while True:
        try:
            # Запрашиваем команду
            command = input("> ").strip()
            if not command:
                continue

            # Запрашиваем дисциплину и оценку и отправляем их на сервер
            if command == 'add':
                print("\nДобавление новой оценки:")
                discipline = input("Введите название дисциплины: ").strip()
                grade = input("Введите оценку: ").strip()
                if discipline and grade:
                    client.add_grade(discipline, grade)
                else:
                    print("Ошибка: Все поля должны быть заполнены")
                print()

            elif command == 'exit':
                break
            else:
                print("Неизвестная команда.")
        
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()

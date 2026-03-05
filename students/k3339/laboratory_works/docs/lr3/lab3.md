# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов
### Manufactory
#### Breeds
1 **Получить список пород**
```
GET /manufactory/breeds/
```
![img.png](images/img.png)

2 **Добавить породу**

```
POST /manufactory/breeds/
```
![img_1.png](images/img_1.png)
3 **Получить разницу между средним значением производительности породы и средним числом по цеху**
```
GET /manufactory/breeds/difference/
```
![img_2.png](images/img_2.png)
4 **Получить детальную информацию о породе**
```
GET /manufactory/breeds/{id}
```
![img_3.png](images/img_3.png)
5 **Изменить породу**
```
UPDATE /manufactory/breeds/{id}
```
![img_4.png](images/img_4.png)
6 **Изменить породу**
```
PATCH /manufactory/breeds/{id}
```
![img_5.png](images/img_5.png)
7 **Удалить породу**
```
DELETE /manufactory/breeds/{id}
```
![img_6.png](images/img_6.png)
#### Cells
8 **Получить список клеток**
```
GET /manufactory/cells/
```
![img_7.png](images/img_7.png)
9 **Добавить клетку**
```
POST /manufactory/cells/
```
![img_8.png](images/img_8.png)

#### Chicken
10 **Получить список куриц**
```
GET /manufactory/chicken/
```
![img_9.png](images/img_9.png)
11 **Добавить курицу**
```
POST /manufactory/chicken/
```
![img_10.png](images/img_10.png)
12 **Удалить курицу**
```
DELETE /manufactory/chicken/{id}
```
![img_11.png](images/img_11.png)

13 **Получить информацию о курице**
```
GET /manufactory/chicken/{id}
```
![img_12.png](images/img_12.png)
14 **Изменить информацию о курице**
```
PUT /manufactory/chicken/{id}
```
![img_13.png](images/img_13.png)
15 **Изменить информацию о курице**
```
PATCH /manufactory/chicken/{id}
```
![img_14.png](images/img_14.png)
#### Diets
16 **Получить список диет**
```
GET /manufactory/diets/
```
![img_15.png](images/img_15.png)


### Auth
32 **Получить токен юзера по паролю и никнейму**
```
POST /auth/token/login
```
33 **Вывести информацию о пользователе**
```
GET /auth/users/me
```
34 **Зарегистрировать пользователя**
```
POST /auth/users
```


# views.py (отрывок)

        class EmployeeAPIView(GenericAPIView):
            permission_classes = [IsAuthenticated]
            serializer_class = EmployeeSerializer
        
            def get(self, request):
                employees = Employee.objects.all()
                serializer = EmployeeSerializer(employees, many=True)
                return Response(serializer.data)
        
            def post(self, request):
                serializer = EmployeeSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        class EmployeeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
            permission_classes = [IsAuthenticated]
            serializer_class = EmployeeSerializer
            queryset = Employee.objects.all()
        
        
        class ResponsibleEmployeeAPIView(APIView):
            permission_classes = [IsAuthenticated]
            serializer_class = ResponsibleEmployeeWriteSerializer
        
            def get(self, request):
                employees = ResponsibleEmployee.objects.all()
                serializer = ResponsibleEmployeeSerializer(employees, many=True)
                return Response(serializer.data)
        
            def post(self, request):
                serializer = ResponsibleEmployeeWriteSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        class ResponsibleEmployeeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
            permission_classes = [IsAuthenticated]
            serializer_class = ResponsibleEmployeeWriteSerializer
            queryset = ResponsibleEmployee.objects.all()
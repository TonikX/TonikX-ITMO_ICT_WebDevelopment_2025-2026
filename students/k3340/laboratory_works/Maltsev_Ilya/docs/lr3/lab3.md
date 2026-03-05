# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов

### Individual Clients
1. **Получить список клиентов**
```
GET /clients/
```
![img_1.png](images/img_1.png)

2. **Получить информацию о клиенте**
```
GET /clients/{id}/
```
![img_2.png](images/img_2.png)

3. **Создать клиента**
```
POST /clients/
```
![img_3.png](images/img_3.png)

4. **Обновить клиента**
```
PUT /clients/{id}/
```
![img_4.png](images/img_4.png)

5. **Частично обновить клиента**
```
PATCH /clients/{id}/
```
![img_5.png](images/img_5.png)

6. **Удалить клиента**
```
DELETE /clients/{id}/
```
![img_6.png](images/img_6.png)

### Agents
1. **Получить список агентов**
```
GET /agents/
```
![img_7.png](images/img_7.png)

2. **Получить информацию об агенте**
```
GET /agents/{id}/
```
![img_8.png](images/img_8.png)

3. **Создать агента**
```
POST /agents/
```
![img_9.png](images/img_9.png)

4. **Обновить агента**
```
PUT /agents/{id}/
```
![img_10.png](images/img_10.png)

5. **Частично обновить агента**
```
PATCH /agents/{id}/
```
![img_11.png](images/img_11.png)

6. **Удалить агента**
```
DELETE /agents/{id}/
```
![img_12.png](images/img_12.png)

### Individual Contracts
1. **Получить список индивидуальных контрактов**
```
GET /clients/contracts
```
![img_13.png](images/img_13.png)

2. **Получить информацию об индивидуальном контракте**
```
GET /clients/contracts/{id}/
```
![img_15.png](images/img_15.png)
3. **Создать индивидуальный контракт**
```
POST /clients/contracts
```
![img_14.png](images/img_14.png)
4. **Обновить индивидуальный контракт**
```
PUT /clients/contracts/{id}/
```
![img_16.png](images/img_16.png)

5. **Частично обновить индивидуальный контракт**
```
PATCH /clients/contracts/{id}/
```
![img_17.png](images/img_17.png)
6. **Удалить индивидуальный контракт**
```
DELETE /clients/contracts/{id}/
```
![img_18.png](images/img_18.png)

### Labor Contracts
1. **Получить список трудовых контрактов**
```
GET /agents/contracts/
```
![img_19.png](images/img_19.png)

2. **Получить информацию о трудовом контракте**
```
GET /agents/contracts/{id}/
```
![img_21.png](images/img_21.png)

3. **Создать трудовой контракт**
```
POST /agents/contracts/
```
![img_20.png](images/img_20.png)
4. **Обновить трудовой контракт**
```
PUT /agents/contracts/{id}/
```
![img_22.png](images/img_22.png)
5. **Частично обновить трудовой контракт**
```
PATCH /agents/contracts/{id}/
```
![img_23.png](images/img_23.png)

6. **Удалить трудовой контракт**
```
DELETE /agents/contracts/{id}/
```
![img_24.png](images/img_24.png)

### Organizations
1. **Получить список организаций**
```
GET /organizations/
```
![img_25.png](images/img_25.png)
2. **Получить информацию об организации**
```
GET /organizations/{id}/
```
![img_26.png](images/img_26.png)

3. **Создать организацию**
```
POST /organizations/
```
![img_27.png](images/img_27.png)

4. **Обновить организацию**
```
PUT /organizations/{id}/
```

5. **Частично обновить организацию**
```
PATCH /organizations/{id}/
```
![img_28.png](images/img_28.png)


## views.py (отрывок)

    class IndividualClientAPIView(GenericAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = IndividualClientSerializer
    
        def get(self, request):
            clients = IndividualClient.objects.all()
            serializer = IndividualClientSerializer(clients, many=True)
            return Response(serializer.data)
    
        def post(self, request):
            serializer = IndividualClientSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    class IndividualClientDetailView(generics.RetrieveUpdateDestroyAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = IndividualClientSerializer
        queryset = IndividualClient.objects.all()
    
    
    class AgentAPIView(GenericAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = AgentSerializer
    
        def get(self, request):
            agents = Agent.objects.all()
            serializer = AgentSerializer(agents, many=True)
            return Response(serializer.data)
    
        def post(self, request):
            serializer = AgentSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

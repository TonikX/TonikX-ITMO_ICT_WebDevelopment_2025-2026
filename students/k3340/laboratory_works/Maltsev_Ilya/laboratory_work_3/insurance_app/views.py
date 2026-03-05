from django.db.models import Count, F, Sum, Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from insurance_app.models import InsuredEmployee, CollectiveContract, Organization, Agent, IndividualContract, \
    IndividualClient, LaborContract, RiskCategory, InsuredEventIndividual, IndividualPayment, InsuredEventEmployee, \
    EmployeePayment
from insurance_app.serializers import InsuredEmployeeSerializer, OrganizationSerializer, AgentSerializer, \
    InsuredEmployeeWriteSerializer, IndividualClientSerializer, IndividualContractSerializer, \
    IndividualContractWriteSerializer, LaborContractSerializer, LaborContractWriteSerializer, \
    CollectiveContractSerializer, CollectiveContractWriteSerializer, RiskCategorySerializer, \
    InsuredEventIndividualSerializer, InsuredEventIndividualWriteSerializer, IndividualPaymentWriteSerializer, \
    IndividualPaymentSerializer, InsuredEventEmployeeWriteSerializer, InsuredEventEmployeeSerializer, \
    EmployeePaymentWriteSerializer, EmployeePaymentSerializer


class IndividualClientAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndividualClientSerializer

    def get(self, request):
        clients = IndividualClient.objects.all()
        serializer = IndividualClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IndividualClientSerializer(data=request.data)
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
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()


class IndividualContractAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndividualContractWriteSerializer

    def get(self, request):
        contracts = IndividualContract.objects.all()
        serializer = IndividualContractSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IndividualContractWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class IndividualContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndividualContractWriteSerializer
    queryset = IndividualContract.objects.all()


class LaborContractAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LaborContractWriteSerializer

    def get(self, request):
        contracts = LaborContract.objects.all()
        serializer = LaborContractSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LaborContractWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LaborContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LaborContractWriteSerializer
    queryset = LaborContract.objects.all()


class OrganizationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()


class CollectiveContractAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectiveContractWriteSerializer

    def get(self, request):
        contracts = CollectiveContract.objects.all()
        serializer = CollectiveContractSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectiveContractWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectiveContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectiveContractWriteSerializer
    queryset = CollectiveContract.objects.all()


class RiskCategoryAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RiskCategorySerializer

    def get(self, request):
        categories = RiskCategory.objects.all()
        serializer = RiskCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RiskCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuredEmployeeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InsuredEmployeeWriteSerializer

    def get(self, request):
        insured_employees = InsuredEmployee.objects.all()
        serializer = InsuredEmployeeSerializer(insured_employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InsuredEmployeeWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuredEmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InsuredEmployeeWriteSerializer
    queryset = InsuredEmployee.objects.all()


class InsuredEventIndividualAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InsuredEventIndividualWriteSerializer

    def get(self, request):
        insured_event_individuals = InsuredEventIndividual.objects.all()
        serializer = InsuredEventIndividualSerializer(insured_event_individuals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InsuredEventIndividualWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndividualPaymentAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndividualPaymentWriteSerializer

    def get(self, request):
        individual_payments = IndividualPayment.objects.all()
        serializer = IndividualPaymentSerializer(individual_payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IndividualPaymentWriteSerializer(data=request.dat)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuredEmployeeEventAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InsuredEventEmployeeWriteSerializer

    def get(self, request):
        insured_event_employees = InsuredEventEmployee.objects.all()
        serializer = InsuredEventEmployeeSerializer(insured_event_employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InsuredEventEmployeeWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeePaymentAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeePaymentWriteSerializer

    def get(self, request):
        employee_payments = EmployeePayment.objects.all()
        serializer = EmployeePaymentSerializer(employee_payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeePaymentWriteSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RelatedOrganizationsView(GenericAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Список других организаций, застрахованных теми же агентами, что и заданная, для действующих договоров",
        manual_parameters=[
            openapi.Parameter(
                'organization_id',
                openapi.IN_QUERY,
                description="Target organization id",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval", schema=OrganizationSerializer),
        }
    )
    def get(self, request):
        organization_id = request.query_params.get('organization_id')
        agent_ids = CollectiveContract.objects.filter(
            organization_id=organization_id, status='a'
        ).values_list('agent_id', flat=True)
        queryset = Organization.objects.filter(
            collectivecontract__agent_id__in=agent_ids
        ).exclude(id=organization_id).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AgentContractStatsView(GenericAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Для каждого агента вывести количество заключенных им договоров каждого типа за определенный период времени",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Начало периода",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Конец периода",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        agents = Agent.objects.annotate(
            individual_contracts=Count('individualcontract', filter=(
                    Q(individualcontract__sign_date__gte=start_date) &
                    Q(individualcontract__sign_date__lte=end_date)
            )),
            collective_contracts=Count('collectivecontract', filter=(
                    Q(collectivecontract__sign_date__gte=start_date) &
                    Q(collectivecontract__sign_date__lte=end_date)
            ))
        ).values('first_name', 'second_name', 'patronymic', 'individual_contracts', 'collective_contracts')
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "statistics": [
                {
                    'agent': f"{agent['first_name']} {agent['second_name']} {agent['patronymic']}",
                    'individual_contracts_count': agent['individual_contracts'],
                    'collective_contracts_count': agent['collective_contracts']
                }
                for agent in agents
            ]
        }
        return Response(data, status=status.HTTP_200_OK)


class InsuredEmployeesView(GenericAPIView):
    serializer_class = InsuredEmployeeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Для заданной персоны вывести список застрахованных сотрудников в одном коллективном договоре для действующих коллективных договоров.",
        manual_parameters=[
            openapi.Parameter(
                'employee_id',
                openapi.IN_QUERY,
                description="Идентификатор застрахованного сотрудника",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        employee_id = request.query_params['employee_id']
        contract_ids = CollectiveContract.objects.filter(
            insured_employees__id=employee_id, status='a'
        ).values_list('id', flat=True)
        queryset = InsuredEmployee.objects.filter(
            collective_contract_id__in=contract_ids
        ).exclude(id=employee_id)
        serializer = InsuredEmployeeSerializer(queryset, many=True)
        return Response(serializer.data)


class PaymentsByContractTypeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Вывести общую сумму выплат по каждому типу договоров при возникших страховых случаях за заданный период времени.",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Начало периода",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Конец периода",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        individual_payments = IndividualContract.objects.filter(
            insuredeventindividual__date__gte=start_date,
            insuredeventindividual__date__lte=end_date
        ).aggregate(total_payments=Sum('insuredeventindividual__individualpayment__amount'))

        collective_payments = CollectiveContract.objects.filter(
            insured_employees__insuredeventemployee__date__gte=start_date,
            insured_employees__insuredeventemployee__date__lte=end_date
        ).aggregate(total_payments=Sum('insured_employees__insuredeventemployee__employeepayment__amount'))
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "payments_by_contract_type": {
                "individual_contracts": individual_payments["total_payments"] or 0,
                "collective_contracts": collective_payments["total_payments"] or 0,
            }
        }

        return Response(data, status=status.HTTP_200_OK)


class OrganizationPaymentsView(GenericAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Для каждого юридического лица вывести реквизиты договора и общую сумму выплат по всем категориям сотрудников.",
        responses={
            200: openapi.Response(description="Successful retrieval", schema=OrganizationSerializer(many=True)),
        }
    )
    def get(self, request):
        organizations_payments = Organization.objects.annotate(
            total_payments=Sum(
                'collectivecontract__insured_employees__insuredeventemployee__employeepayment__amount'
            )
        ).values('full_name', 'bank_code', 'total_payments')
        result = [
            {
                "full_name": organization_payments["full_name"],
                "bank_code": organization_payments["bank_code"],
                "total_payments": organization_payments["total_payments"] or 0
            }
            for organization_payments in organizations_payments
        ]

        return Response(result, status=status.HTTP_200_OK)


class ContractsSummaryView(GenericAPIView):
    serializer_class = IndividualContractSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Отчёт",
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        queryset = Agent.objects.annotate(
            active_individual_contracts=Count(
                'individualcontract', filter=Q(individualcontract__status='a')
            ),
            active_collective_contracts=Count(
                'collectivecontract', filter=Q(collectivecontract__status='a')
            ),
            total_individual_sum=Sum(
                'individualcontract__insuredeventindividual__individualpayment__amount'
            ),
            total_collective_sum=Sum(
                'collectivecontract__insured_employees__insuredeventemployee__employeepayment__amount'
            )
        ).annotate(
            company_total_sum=F('total_individual_sum') + F('total_collective_sum')
        ).values('id', 'first_name', 'second_name', 'active_individual_contracts', 'active_collective_contracts',
                 'total_individual_sum', 'total_collective_sum', 'company_total_sum')

        result = [
            {
                "id": agent["id"],
                "first_name": agent["first_name"],
                "second_name": agent["second_name"],
                "active_individual_contracts": agent["active_individual_contracts"] or 0,
                "active_collective_contracts": agent["active_collective_contracts"] or 0,
                "total_individual_sum": agent["total_individual_sum"] or 0,
                "total_collective_sum": agent["total_collective_sum"] or 0,
                "company_total_sum": agent["company_total_sum"] or 0
            }
            for agent in queryset
        ]

        return Response(result, status=status.HTTP_200_OK)

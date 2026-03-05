from django.urls import path

from insurance_app.views import InsuredEmployeeDetailView, RelatedOrganizationsView, IndividualClientAPIView, \
    IndividualClientDetailView, AgentAPIView, AgentDetailView, IndividualContractAPIView, IndividualContractDetailView, \
    LaborContractAPIView, LaborContractDetailView, OrganizationAPIView, OrganizationDetailView, \
    CollectiveContractAPIView, CollectiveContractDetailView, RiskCategoryAPIView, InsuredEmployeeAPIView, \
    InsuredEmployeeEventAPIView, InsuredEventIndividualAPIView, IndividualPaymentAPIView, EmployeePaymentAPIView, \
    AgentContractStatsView, InsuredEmployeesView, PaymentsByContractTypeView, OrganizationPaymentsView, \
    ContractsSummaryView

urlpatterns = [
    path('clients/', IndividualClientAPIView.as_view()),
    path('clients/<int:pk>/', IndividualClientDetailView.as_view()),
    path('agents/', AgentAPIView.as_view()),
    path('agents/<int:pk>/', AgentDetailView.as_view()),
    path('clients/contracts', IndividualContractAPIView.as_view()),
    path('clients/contracts/<int:pk>/', IndividualContractDetailView.as_view()),
    path('agents/contracts/', LaborContractAPIView.as_view()),
    path('agents/contracts/<int:pk>/', LaborContractDetailView.as_view()),
    path('organizations/', OrganizationAPIView.as_view()),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view()),
    path('organizations/contracts/', CollectiveContractAPIView.as_view()),
    path('organizations/contracts/<int:pk>/', CollectiveContractDetailView.as_view()),
    path('categories/', RiskCategoryAPIView.as_view()),
    path('employees/', InsuredEmployeeAPIView.as_view()),
    path('employees/<int:pk>/', InsuredEmployeeDetailView.as_view()),
    path('employees/events/', InsuredEmployeeEventAPIView.as_view()),
    path('employees/payments/', EmployeePaymentAPIView.as_view()),
    path('clients/events/', InsuredEventIndividualAPIView.as_view()),
    path('clients/payments/', IndividualPaymentAPIView.as_view()),
    path('employee/{id}/', InsuredEmployeeDetailView.as_view()),
    path('organizations/related/', RelatedOrganizationsView.as_view()),
    path('agents/contracts/stats/', AgentContractStatsView.as_view()),
    path('employees/colleagues', InsuredEmployeesView.as_view()),
    path('payments/total', PaymentsByContractTypeView.as_view()),
    path('organization/payments/', OrganizationPaymentsView.as_view()),
    path('report/', ContractsSummaryView.as_view()),
]
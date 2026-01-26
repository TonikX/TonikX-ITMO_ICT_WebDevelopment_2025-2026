from rest_framework.exceptions import APIException
from rest_framework import status


class AlreadyHaveCompanyError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "У вас уже есть компания"
    default_code = 'already_have_company'


class NoCompanyError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "У вас нет компании"
    default_code = 'no_company'


class PermissionDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "У вас недостаточно прав для выполнения этого действия"
    default_code = 'permission_denied'


class CompanyPermissionDeniedError(PermissionDeniedError):
    default_detail = "Вы не можете выполнять действия с чужой компанией"
    default_code = 'company_permission_denied'


class ServicePermissionDeniedError(PermissionDeniedError):
    default_detail = "Вы не можете выполнять действия с чужими услугами"
    default_code = 'service_permission_denied'


class DiscountPermissionDeniedError(PermissionDeniedError):
    default_detail = "Вы не можете создавать скидки для чужих услуг"
    default_code = 'discount_permission_denied'


class DiscountDateError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Дата окончания должна быть позже даты начала"
    default_code = 'invalid_discount_dates'


class RequestPermissionDeniedError(PermissionDeniedError):
    default_detail = "Вы не можете менять статус этой заявки"
    default_code = 'request_permission_denied'


class InvalidStatusError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Неверный статус"
    default_code = 'invalid_status'


class SelfRequestStatusError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Вы не можете менять статус своей заявки"
    default_code = 'self_request_status'


class AnalyticsPermissionDeniedError(PermissionDeniedError):
    default_detail = "У вас нет доступа к аналитике этой компании"
    default_code = 'analytics_permission_denied'


class CompanyNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Компания не найдена"
    default_code = 'company_not_found'


class UserActionForbiddenError(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = "Используйте специальные эндпоинты для действий с пользователями"
    default_code = 'user_action_forbidden'


class CompanyActionForbiddenError(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = "Используйте эндпоинт /my/ для обновления своей компании"
    default_code = 'company_action_forbidden'
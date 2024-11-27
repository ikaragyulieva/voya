from voya.clients.models import ClientProfile
from voya.employees.models import EmployeeProfile


def get_user_obj(request):
    if request.user.is_authenticated and request.user.is_active:

        try:
            profile = ClientProfile.objects.get(user=request.user, is_active=True)

            return profile
        except ClientProfile.DoesNotExist:
            pass

        try:
            profile = EmployeeProfile.objects.get(user=request.user, is_active=True)

            return profile

        except EmployeeProfile.DoesNotExist:
            pass

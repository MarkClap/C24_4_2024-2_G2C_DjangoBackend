from django.urls import path
from .views import AssignRoleView, RemoveRoleView
from django.urls import path


urlpatterns = [
    path('api/assign-role/', AssignRoleView.as_view(), name='assign_role'),
    path('api/remove-role/', RemoveRoleView.as_view(), name='remove_role'),
]
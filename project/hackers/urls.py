from django.urls import path
from .views import DashboardView, NavbarView, ReportsLevel, ReportsOwasp, ReportsWeakness, ReportsActivity, ProgramsListView, UpdateProfileView


app_name = "hackers"
urlpatterns = [
    path('dashboard/user-info', DashboardView.as_view(), name='user-info'),
    path('dashboard/reports-levels', ReportsLevel.as_view(), name='reports-levels'),
    #path('dashboard/reports-10OWASP', reports_10OWASP, name='reports-10OWASP'),
    path('dashboard/reports-10OWASP', ReportsOwasp.as_view(), name='reports-10OWASP'),
    #path('dashboard/reports-weaknesses', reports_weakness, name='reports-weaknesses'),
    path('dashboard/reports-weaknesses', ReportsWeakness.as_view(), name='reports-weaknesses'),
    path('dashboard/user-activity', ReportsActivity.as_view(), name='user-activity'),
    path('dashboard/discovery',ProgramsListView.as_view(), name='discovery'),
    path('dashboard/profile/', UpdateProfileView.as_view(), name='profile'),
    path('navbar/', NavbarView.as_view(), name='navbar'),

]
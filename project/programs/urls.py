from django.urls import path
from .views import ProgramInfoView,ReportsAsset,ReportsClosedState, ReportsLevel, ReportsOwasp, ReportsWeakness, ReportsActivity


app_name = "hackers"
urlpatterns = [
    path('dashboard/user-info', ProgramInfoView.as_view(), name='user-info'),
    path('dashboard/reports-levels', ReportsLevel.as_view(), name='reports-levels'),

    path('dashboard/reports-10OWASP', ReportsOwasp.as_view(), name='reports-10OWASP'),

    path('dashboard/reports-weaknesses', ReportsWeakness.as_view(), name='reports-weaknesses'),
    path('dashboard/reports-asset', ReportsAsset.as_view(), name='reports_assety'),
    path('dashboard/reports-closed-state', ReportsClosedState.as_view(), name='reports-closed_state'),
    path('dashboard/user-activity', ReportsActivity.as_view(), name='user-activity'),

]
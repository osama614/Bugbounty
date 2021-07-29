from django.urls import path
from .views import ProgramInfoView,ReportsAsset,ReportsClosedState, ReportsLevel, ReportsOwasp, ReportsWeakness, ReportsActivity, ProgramView, AnnouncementListView, AnnouncementDetailView


app_name = "programs"
urlpatterns = [
    path('dashboard/user-info', ProgramInfoView.as_view(), name='user-info'),
    path('dashboard/reports-levels', ReportsLevel.as_view(), name='reports-levels'),
    path('dashboard/reports-10OWASP', ReportsOwasp.as_view(), name='reports-10OWASP'),
    path('dashboard/reports-weaknesses', ReportsWeakness.as_view(), name='reports-weaknesses'),
    path('dashboard/reports-asset', ReportsAsset.as_view(), name='reports_assety'),
    path('dashboard/reports-closed-state', ReportsClosedState.as_view(), name='reports-closed_state'),
    path('dashboard/user-activity', ReportsActivity.as_view(), name='user-activity'),
    path('dashboard/user-activity', ReportsActivity.as_view(), name='user-activity'),
    path('<int:id>/', ProgramView.as_view(), name='program-view'),
    path('dashboard/settings/announcements', AnnouncementListView.as_view(), name='settings-announcement'),
    path('dashboard/settings/announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='action-settings-announcement'),
]
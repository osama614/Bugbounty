from django.urls import path
from .views import (ChangeAvaterView, DashboardView, NavbarView, ReportsLevel, ReportsOwasp, ReportsWeakness, ReportsListView,HackerProfile,
                    ReportsActivity, ProgramsListView, SkillsView, UpdateProfileView, ActivityView, LeaderBoardView, ReportDetail, set_event)


app_name = "hackers"
urlpatterns = [
    path('<str:username>', HackerProfile.as_view(), name='profile'),
    path('dashboard/user-info', DashboardView.as_view(), name='user-info'),
    path('dashboard/reports-levels', ReportsLevel.as_view(), name='reports-levels'),
    #path('dashboard/reports-10OWASP', reports_10OWASP, name='reports-10OWASP'),
    path('dashboard/reports-10OWASP', ReportsOwasp.as_view(), name='reports-10OWASP'),
    #path('dashboard/reports-weaknesses', reports_weakness, name='reports-weaknesses'),
    path('dashboard/reports-weaknesses', ReportsWeakness.as_view(), name='reports-weaknesses'),
    path('dashboard/user-activity', ReportsActivity.as_view(), name='user-activity'),
    path('dashboard/discovery',ProgramsListView.as_view(), name='discovery'),
    path('dashboard/settings/profile/', UpdateProfileView.as_view(), name='profile'),
    path('dashboard/settings/set-avater/', ChangeAvaterView.as_view(), name='avater'),
    path('dashboard/settings/skills/', SkillsView.as_view(), name='skills'),
    path('navbar/', NavbarView.as_view(), name='navbar'),
    path('activity/', ActivityView.as_view(), name='activity'),
    path('leaderboard/', LeaderBoardView.as_view(), name='leader-board'),
    path('submissions/', ReportsListView.as_view(), name='submissions'),
    path('submissions/<int:pk>', ReportDetail.as_view(), name='report-page'),
    path('submissions/<int:pk>/events', set_event, name='report-page'),

]
from django.urls import path
from .views import (AssetDetailView, AssetListView, ChangeLogoView, CompanyInfoView, CompanyPolicy, NavbarView, ProgramInfoView, ReportDetail,ReportsAsset,ReportsClosedState, ReportsLevel, PReportsListView,
                   ReportsOwasp, ReportsWeakness, ReportsActivity, ProgramView, AnnouncementListView, 
                    AnnouncementDetailView, RewardsView, upload_policy_image)


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
    path('submissions/', PReportsListView.as_view(), name='submissions-program'),
    path('submissions/<int:pk>', ReportDetail.as_view(), name='report-page'),
    path('dashboard/settings/announcements', AnnouncementListView.as_view(), name='settings-announcement'),
    path('dashboard/settings/announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='action-settings-announcement'),
    path('dashboard/settings/assets', AssetListView.as_view(), name='settings-asset'),
    path('dashboard/settings/assets/<int:pk>/', AssetDetailView.as_view(), name='action-settings-asset'),
    path('dashboard/settings/set-logo', ChangeLogoView.as_view(), name='settings-logo'),
    path('dashboard/settings/company-info', CompanyInfoView.as_view(), name='settings-company-info'),
    path('dashboard/settings/company-policy', CompanyPolicy.as_view(), name='settings-company-policy'),
    path('dashboard/settings/rewards', RewardsView.as_view(), name='settings-rewards'),
    path('navbar/', NavbarView.as_view(), name='navbar'),
    path('policy-image/', upload_policy_image , name='policy-image'),
    path('<str:username>/', ProgramView.as_view(), name='program-view'),
]
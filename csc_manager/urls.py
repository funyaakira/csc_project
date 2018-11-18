from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import reverse

from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # トップページ
	path('', views.home, name='home'),

    # シフト単日表示
    path('shift/<int:year>/<int:month>/<int:day>/', views.ShiftDayView.as_view(), name='shift_day'),

    # シフト個人カレンダー表示
    path('shift/indiv/<int:pk>/<int:year>/<int:month>/', views.ShiftIndivView.as_view(), name='shift_indiv'),

    # シフトGogleSpreadSheetからの受信インターフェース
	path('shift/receive_from_gas/', views.receive_from_gas, name='receive_from_gas'),

    # 利用者 - 一覧
	path('riyosya_list/', views.RiyosyaListView.as_view(), name='riyosya_list'),

    # 利用者 - 新規入所
	path('riyosya_new/', views.RiyosyaNewView.as_view(), name='riyosya_new'),

    # イベント - 一覧(当月)
	path('event_list/', views.EventListView.as_view(), name='event_list'),

    # イベント - 一覧(年月指定)
	path('event_list/<int:year>/<int:month>/', views.EventListView.as_view(), name='event_list'),


    path('test_create/', views.TestCreateView.as_view(), name='test_create'),


    path('test/', views.TestView.as_view(), name='test'),


	path('shift/sw.js', (TemplateView.as_view(template_name="ayumi_manager/sw.js",
		content_type='application/javascript',)), name='sw.js'),

	path('shift/manifest.json', (TemplateView.as_view(template_name="ayumi_manager/manifest.json",
		content_type='application/javascript',)), name='manifest.json'),
]

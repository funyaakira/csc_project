from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import reverse

from . import views
from ._views.Event import EventListView, EventCreateView
from ._views.Shift import ShiftDayView, ShiftIndivView
from ._views.Riyosya import RiyosyaListView, RiyosyaNewView, RiyosyaTaisyoView, TaisyoListView, TaisyoRenewView

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # トップページ
	path('', views.home, name='home'),

    # シフト - 単日表示
    path('shift/<int:year>/<int:month>/<int:day>/', ShiftDayView.as_view(), name='shift_day'),

    # シフト - 個人カレンダー表示
    path('shift/indiv/<int:pk>/<int:year>/<int:month>/', ShiftIndivView.as_view(), name='shift_indiv'),

    # シフト - データアップロード
    path('shift_upload/', views.shift_upload, name='shift_upload'),

    # 利用者 - 利用者 - 一覧
	path('riyosya_list/', RiyosyaListView.as_view(), name='riyosya_list'),

    # 利用者 - 利用者 - 新規入所
	path('riyosya_new/', RiyosyaNewView.as_view(), name='riyosya_new'),

    # 利用者 - 利用者 - 退所
	path('riyosya_taisyo/riyosyariyoukikan/<int:pk>/', RiyosyaTaisyoView.as_view(), name='riyosya_taisyo'),

    # 利用者 - 退所者 - 退所者一覧
    path('taisyo_list/', TaisyoListView.as_view(), name='taisyo_list'),

    # 利用者 - 退所者 - 再入所
    path('taisyo_renew/riyosya/<int:pk>/', TaisyoRenewView.as_view(), name='taisyo_renew'),

    # イベント - 一覧(当月)
	path('event_list/', EventListView.as_view(), name='event_list'),

    # イベント - 一覧(年月指定)
	path('event_list/<int:year>/<int:month>/', EventListView.as_view(), name='event_list'),

    # イベント - 新規
    path('event_create/', EventCreateView.as_view(), name='event_create'),


    # # シフトGogleSpreadSheetからの受信インターフェース
    # path('shift/receive_from_gas/', views.receive_from_gas, name='receive_from_gas'),
    # path('test_create/', views.TestCreateView.as_view(), name='test_create'),
    #
    #
    # path('test/', views.TestView.as_view(), name='test'),
    #
    #
	# path('shift/sw.js', (TemplateView.as_view(template_name="ayumi_manager/sw.js",
	# 	content_type='application/javascript',)), name='sw.js'),
    #
	# path('shift/manifest.json', (TemplateView.as_view(template_name="ayumi_manager/manifest.json",
	# 	content_type='application/javascript',)), name='manifest.json'),
]

from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import reverse

from . import views
from ._views.Event import *
from ._views.Shift import *
from ._views.Riyosya import *
from ._views.Renraku import *
from ._views.Kiroku import *
from ._views.Print import *

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # トップページ
	path('', views.home, name='home'),

    # トップページ
	path('index.html', views.home, name='home'),

    # シフト - 単日表示
    path('shift/<int:year>/<int:month>/<int:day>/', ShiftDayView.as_view(), name='shift_day'),

    # シフト - 個人カレンダー表示
    path('shift/indiv/<int:pk>/<int:year>/<int:month>/', ShiftIndivView.as_view(), name='shift_indiv'),

    # シフト - データアップロード
    path('shift/upload/', views.shift_upload, name='shift_upload'),

    # 利用者 - 利用者 - 一覧
	path('riyosya_list/', RiyosyaListView.as_view(), name='riyosya_list'),

    # 利用者 - 利用者 - 一覧 - 年月日指定(テスト用)
	path('riyosya_list/<int:year>/<int:month>/<int:day>/', RiyosyaListView.as_view(), name='riyosya_list'),

    # 利用者 - 利用者 - 実開始日時登録
	path('riyosya/start/input/<int:pk>', RiyosyaStartInputView.as_view(), name='riyosya_start_input'),

    # 利用者 - 利用者 - 実終了日時登録
	path('riyosya/last/input/<int:pk>', RiyosyaLastInputView.as_view(), name='riyosya_last_input'),

    # 利用者 - 利用者 - 詳細
	path('riyosya_detail/<int:pk>/', RiyosyaDetailView.as_view(), name='riyosya_detail'),

    # 利用者 - 利用者 - 新規入所
	path('riyosya_new/', RiyosyaNewView.as_view(), name='riyosya_new'),

    # 利用者 - 利用者 - 利用予定者一覧
	path('riyosya/yotei/list', RiyosyaYoteiListView.as_view(), name='riyosya_yotei_list'),

    # 利用者 - 利用者 - 退所
	path('riyosya_taisyo/riyosyariyoukikan/<int:pk>/', RiyosyaTaisyoView.as_view(), name='riyosya_taisyo'),

    # 利用者 - 退所者 - 退所者一覧
    path('taisyo_list/', TaisyoListView.as_view(), name='taisyo_list'),

    # 利用者 - 退所者 - 詳細
	path('taisyosya_detail/<int:pk>/', TaisyoDetailView.as_view(), name='taisyosya_detail'),

    # 利用者 - 退所者 - 再入所
    path('taisyo_renew/riyosya/<int:pk>/', TaisyoRenewView.as_view(), name='taisyo_renew'),

    # イベント - 一覧(当月)
	path('event_list/', EventListView.as_view(), name='event_list'),

    # イベント - 一覧(年月指定)
	path('event_list/<int:year>/<int:month>/', EventListView.as_view(), name='event_list'),

    # イベント - 一覧(年月指定) - スクロール位置指定
	path('event_list/<int:year>/<int:month>/<str:scroll_position>', EventListView.as_view(), name='event_list_with_scroll_postion'),

    # イベント - 新規 - スクロール位置指定
    path('event_create/<int:year>/<int:month>/<int:day>/<int:event_knd_id>/<str:scroll_position>', EventCreateView.as_view(), name='event_create'),

    # イベント - 削除 - スクロール位置指定
    path('event/delete/<int:year>/<int:month>/<int:day>/<int:event_id>/<str:scroll_position>', eventDelete, name='event_delete'),

    # 全体連絡 - 一覧
	path('renraku_list/', RenrakuZentaiListView.as_view(), name='renraku_list'),

    # 全体連絡 - 詳細
	path('renraku_detail/<int:pk>/', RenrakuZentaiDetailView.as_view(), name='renraku_detail'),

    # 全体連絡 - 新規
	path('renraku_create/', RenrakuZentaiCreateView.as_view(), name='renraku_create'),

    # 個人連絡 - 一覧
	path('renraku_kojin_list/', RenrakuKojinListView.as_view(), name='renraku_kojin_list'),

    # 個人連絡 - 一覧(利用者指定)
	path('renraku_kojin_list/riyosya/<int:riyosya_pk>/', RenrakuKojinListRiyosyaView.as_view(), name='renraku_kojin_list_riyosya'),

    # 個人連絡 - 詳細
	path('renraku_kojin_detail/<int:pk>/', RenrakuKojinDetailView.as_view(), name='renraku_kojin_detail'),

    # 個人連絡 - 新規
	path('renraku_kojin_create/', RenrakuKojinCreateView.as_view(), name='renraku_kojin_create'),

    # 記録 - 一覧
    path('kiroku_day_list/', kiroku_home, name='kiroku_home'),

    # 記録 - 一覧 - 日指定
    path('kiroku_day_list/<int:year>/<int:month>/<int:day>/<int:day_night>/', KirokuDayListView.as_view(), name='kiroku_day_list'),

    # 記録 - 個人一覧 - 年月指定
    path('kiroku/kojin/<int:year>/<int:month>/<int:riyosya_id>/', KirokuKojinListView.as_view(), name='kiroku_kojin'),

    # 記録 - 新規
    path('kiroku/create/<int:year>/<int:month>/<int:day>/<int:day_night>/<str:riyosya_ids>/<int:riyosya_id_current_index>', KirokuCreateView.as_view(), name='kiroku_create'),

    # # 記録 - 削除
    # path('kiroku_delete/<int:year>/<int:month>/<int:day>/<int:day_night>/<int:pk>/', KirokuDeleteView.as_view(), name='kiroku_delete'),

    # 記録 - 削除
    path('kiroku/delete/<int:year>/<int:month>/<int:day>/<int:day_night>/<str:riyosya_ids>/<int:riyosya_id_current_index>/<int:pk>/', kiroku_delete, name='kiroku_delete'),

    # 記録 - アップロード
    path('kiroku/upload/', kiroku_upload, name='kiroku_upload'),

]

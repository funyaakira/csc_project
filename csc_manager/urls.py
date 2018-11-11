from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


	path('', views.home, name='home'),

	path('shift/', views.index, name='index'),

	path('shift/index.html', views.index, name='index'),

	re_path(r'shift/(?P<shift_day>\d{4}-\d{2}-\d{2})/$', views.shift_day, name='shift_day'),

	path('shift/receive_from_gas/', views.receive_from_gas, name='receive_from_gas'),

	path('shift/sw.js', (TemplateView.as_view(template_name="ayumi_manager/sw.js",
		content_type='application/javascript',)), name='sw.js'),

	path('shift/manifest.json', (TemplateView.as_view(template_name="ayumi_manager/manifest.json",
		content_type='application/javascript',)), name='manifest.json'),
]

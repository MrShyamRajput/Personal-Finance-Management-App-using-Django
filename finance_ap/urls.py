from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login,name="login"),
    path('register', views.register,name="register"),
    path('home',views.home,name="home"),
    path('add_transaction',views.add_transaction,name="add_transaction"),
    path('view_transaction',views.view_transaction,name="view_transaction"),
    path('set_budget',views.set_budget,name="set_budget"),
    path('check_budget',views.check_budget,name="check_budget"),
    path('financial_reports',views.financial_reports,name="monthly_reports"),
   
]

from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account_details, name='account_details'),
    path('transaction/', views.make_transaction, name='make_transaction'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('balance/', views.check_balance, name='check_balance'), 
]

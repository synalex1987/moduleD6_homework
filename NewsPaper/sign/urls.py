from django.urls import path
from .views import BaseRegisterView, LoginViewPage, PersonalPage, make_author, subscriptions_update

urlpatterns = [
    path('login/', LoginViewPage.as_view(), name='login'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
    path('upgrade/', make_author, name='upgrade'),
    path('personal/', PersonalPage.as_view(), name='personal'),
    path('subscriptions_update/', subscriptions_update, name='subscriptions_update'),
]

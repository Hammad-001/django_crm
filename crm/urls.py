from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    # path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('add_record/', views.add_record, name="add_record"),
    path('view_record/<int:customer>', views.view_record, name="view_record"),
    path('delete_record/<int:customer>', views.delete_record, name="delete_record"),
    path('update_record/<int:customer>', views.update_record, name="update_record"),
]

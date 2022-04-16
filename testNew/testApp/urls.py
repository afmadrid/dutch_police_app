from django.urls import path
from . import views
from .views import Home
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', Home.as_view(), name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', auth_views.PasswordChangeView.
         as_view(template_name='change_password.html', success_url=reverse_lazy('change_password_done')),
         name='change_password'),
    path('change_password_done/', auth_views.PasswordChangeDoneView.
         as_view(template_name='change_password_done.html'),
         name='change_password_done'),
    path('reset_password/', auth_views.PasswordResetView.
         as_view(template_name='reset_password.html', success_url=reverse_lazy('reset_password_done')),
         name='reset_password'),
    path('reset_password_done', auth_views.PasswordResetDoneView.
         as_view(template_name='reset_password_done.html'),
         name='reset_password_done'),

    path('create/', views.create, name='create'),
    path('show/', views.show, name='show'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.destroy, name='delete'),
    path('details/<int:id>', views.details, name='details'), path('', Home.as_view(), name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', auth_views.PasswordChangeView.
         as_view(template_name='change_password.html', success_url=reverse_lazy('change_password_done')),
         name='change_password'),
    path('change_password_done/', auth_views.PasswordChangeDoneView.
         as_view(template_name='change_password_done.html'),
         name='change_password_done'),
    path('reset_password/', auth_views.PasswordResetView.
         as_view(template_name='reset_password.html', success_url=reverse_lazy('reset_password_done')),
         name='reset_password'),
    path('reset_password_done', auth_views.PasswordResetDoneView.
         as_view(template_name='reset_password_done.html'),
         name='reset_password_done'),

    path('create/', views.create, name='create'),
    path('show/', views.show, name='show'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.destroy, name='delete'),
    path('details/<int:id>', views.details, name='details'),
]

urlpatterns += [
  # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


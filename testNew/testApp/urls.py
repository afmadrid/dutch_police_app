from django.urls import path
from . import views
from .views import Home

urlpatterns = [
    #path('signup/', views.sign_up, name='signup'),
    #path('', views.home, name='home'),
    path('', Home.as_view(), name='home'),
    path('signup/',views.sign_up, name='signup'),
    path('login/',views.user_login, name='login'),
    path('profile/',views.user_profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    #path('<id>', views.detail_case, name='detail_case'),
    #path('create/', views.create_case, name='create'),
    #path('list/', views.list_case, name='list'),
    #path('<id>/delete', views.delete_case, name='delete_case'),
    #path('<id>/update', views.update_case, name='update_case'),
    path('create/', views.create, name='create'),
    path('show/',views.show, name='show'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.destroy, name='delete'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


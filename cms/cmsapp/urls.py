from django.urls import path
from.import views
app_name = 'cmsapp'

urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('contact',views.contact, name='contact'),
    path('artical/<str:slug>', views.detail, name='detail'),
    path('create-post',views.createPost, name='create'),
    path('update-post/<str:slug>',views.updatePost, name='update'),
    path('delete-post/<str:slug>',views.deletePost, name='delete'),
    path('signup/', views.usersignup,name='signup'),
    path('login/', views.userlogin,name='login'),
    path('logout', views.signout, name='logout'),
    path('search', views.search, name='search'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
   
]

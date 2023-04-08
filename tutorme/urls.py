"""tutorme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/delete/', views.delete_profile_view, name='delete'),
    path('createAccount/', views.create_account_view, name='createAccount'),
    path('account_type_choice/', views.account_type_choice, name='account_type_choice'),
    path('view_tutors/', views.tutor_list, name='view_tutors'),
    path('view_tutors/<int:tutor_id>/', views.view_tutor, name='view_tutor'),
    path('view_tutors/<int:tutor_id>/<int:session_id>/', views.request_session, name='request_session'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('requests_page/', views.requests_page, name='requests_page'),
    path('requests_page/view_student/<int:student_id>/', views.view_student, name='view_student'),
    path('requests_page_update/<int:request_id>/', views.requests_page_update, name='requests_page_update'),
    path('student_sessions/', views.student_sessions, name='student_sessions'),
    path('student_sessions_update/<int:request_id>/', views.student_sessions_update, name='student_sessions_update'),

]

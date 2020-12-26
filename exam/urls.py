from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_api, name='register'),
    path('login/', views.login_api, name='login'),
    path('exam/start/', views.start_exam_api, name='start_exam'),
    path('exam/submit/', views.store_result_api, name='submit_exam'),

    # admin api
    path('question/upload/', views.upload_question_api, name='upload_question'),
    path('question/list/', views.questions_api, name='list_question'),
    path('question/update/<int:que_id>/', views.questions_api, name='update_question'),
    path('question/delete/<int:que_id>/', views.questions_api, name='delete_question'),
    path('result/list/', views.result_api, name='list_result'),
]
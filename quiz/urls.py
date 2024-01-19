from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.all_quiz_view, name='all_quiz'),
    path('category/<slug:category_slug>/', views.all_quiz_view, name='cat_quiz'),
    path('question/<int:q_id>/', views.question_view, name='question'),
    path('submit-answer/<int:q_id>/<int:ques_id>/', views.submit_answer_view, name='submit_answer'),
    path('result/', views.result, name='result'),
    
  

]
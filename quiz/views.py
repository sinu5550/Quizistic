from django.shortcuts import render

from . import models
from category.models import Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


def all_quiz_view(request,category_slug=None):

    quizzes = models.Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()
    
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        quizzes = models.Quiz.objects.filter(category = category)
    categories = Category.objects.all()
    context ={"quizzes":quizzes, "categories":categories}


    return render(request,'all_quiz.html',context)

@login_required
def question_view(request,q_id):
    quiz = models.Quiz.objects.get(id=q_id)
    question = models.Question.objects.filter(quiz=quiz).order_by('id').first()

    return render(request,'questions.html',{'ques':question,'quiz': quiz})

@login_required
def submit_answer_view(request,q_id,ques_id):
    if request.method =='POST':
        quiz = models.Quiz.objects.get(id=q_id)
        question = models.Question.objects.filter(quiz=quiz,id__gt=ques_id).exclude(id= ques_id).order_by('id').first()
        if 'skip' in request.POST:
            if question:
                ques = models.Question.objects.get(id=ques_id)
                user = request.user
                answer = 'Not Submitted'
                models.UserAnswerSubmit.objects.create(
                    user=user,question=ques,right_ans=answer
                )
                return render(request,'questions.html',{'ques':question,'quiz': quiz})
        
        else:
            ques = models.Question.objects.get(id=ques_id)
            user = request.user
            answer = request.POST.get('answer', None)
            if answer is not None:
                models.UserAnswerSubmit.objects.create(
                user=user, question=ques, right_ans=answer
                )
            else:
                answer = 'Not Submitted'
                models.UserAnswerSubmit.objects.create(
                 user=user, question=ques, right_ans=answer
                )
        if question:
            return render(request,'questions.html',{'ques':question,'quiz': quiz})
        else:
            result = models.UserAnswerSubmit.objects.filter(user=request.user)
            skipped = models.UserAnswerSubmit.objects.filter(user=request.user,right_ans='Not Submitted').count()
            attemped = models.UserAnswerSubmit.objects.filter(user=request.user).exclude(right_ans='Not Submitted').count()
            rightAns= 0
            for r in result:
                if r.question.right_opt == r.right_ans:
                    rightAns+=1
            return render(request,'quiz_result.html',{'result':result,'skipped':skipped,'attemped':attemped,'rightAns':rightAns})
        
    else:
        return HttpResponse('Method is not allowed')
    


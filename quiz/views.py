from django.shortcuts import render,redirect

from . import models
from category.models import Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from datetime import timedelta

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
    lastAttemp = None
    futureTime = None
    hoursLimit = 24
    countAttemp = models.userQuizAttempts.objects.filter(user=request.user, quiz = quiz).count()
    if countAttemp == 0:
        models.userQuizAttempts.objects.create(user = request.user, quiz=quiz)
    else:
        lastAttemp= models.userQuizAttempts.objects.filter(user = request.user, quiz=quiz).order_by('-id').first()
        futureTime = lastAttemp.attemp_time+ timedelta (hours = hoursLimit)
        if lastAttemp and lastAttemp.attemp_time < futureTime :
            messages.warning(request,'You already attempted this quiz. Please come back after 24 hours.')
            return all_quiz_view(request,None)
        else:
            models.userQuizAttempts.objects.create(user = request.user, quiz=quiz)

    return render(request,'questions.html',{'ques':question,'quiz': quiz, 'lastAttemp':futureTime,})


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
                messages.warning(request, 'Please select an option before submitting.')
                return render(request, 'questions.html', {'ques': ques, 'quiz': quiz})
        if question:
            return render(request,'questions.html',{'ques':question,'quiz': quiz})
        else:
            result = models.UserAnswerSubmit.objects.filter(user=request.user,question__quiz=quiz)
            skipped = models.UserAnswerSubmit.objects.filter(user=request.user,right_ans='Not Submitted',question__quiz=quiz).count()
            attemped = models.UserAnswerSubmit.objects.filter(user=request.user,question__quiz=quiz).exclude(right_ans='Not Submitted').count()
            rightAns= 0
            for r in result:
                if r.question.right_opt == r.right_ans:
                    rightAns+=1
            return render(request,'quiz_result.html',{'result':result,'skipped':skipped,'attemped':attemped,'rightAns':rightAns,'quiz_id': q_id,'quiz':quiz})
        
        
        
        
    else:
        return redirect('all_quiz')

@login_required   
def result(request):
    result = models.UserAnswerSubmit.objects.filter(user=request.user)
    skipped = models.UserAnswerSubmit.objects.filter(user=request.user,right_ans='Not Submitted').count()
    attemped = models.UserAnswerSubmit.objects.filter(user=request.user).exclude(right_ans='Not Submitted').count()
    rightAns= 0
    for r in result:
        if r.question.right_opt == r.right_ans:
            rightAns+=1
    return render(request,'quiz_result.html',{'result':result,'skipped':skipped,'attemped':attemped,'rightAns':rightAns})
    


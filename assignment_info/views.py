from django.shortcuts import render
from .forms import SubmissionForm,CourseForm,CreateCourseForm,RegisterForm
from django.contrib.auth import get_user_model
from .models import Course,Submissions,Cname,RegUsers
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import get_object_or_404
import datetime
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from datetime import date
from django.core.mail import send_mail
from django.conf import settings

    
@login_required
def SubmissionFormView(request,pk=None):
    course = get_object_or_404(Course, pk=pk)
    instance = Submissions.objects.filter(course=course, user=request.user).first()

    submitted = (instance is not None)
    current_time=datetime.datetime.now()

    if request.method=="POST":
        sub_form = SubmissionForm(request.POST or None, request.FILES or None, instance=instance)
        if sub_form.is_valid():
            form=sub_form.save(commit=False)
            form.user=request.user
            form.course=course
            form.submitted_at=datetime.datetime.now()
            # if 'answer' in request.FILES:
            if 'answer' in request.FILES:
                form.answer=request.FILES['answer']
            form.save()
            submitted=True
    else:
        sub_form=SubmissionForm()

    return render(request,template_name='submit.html',context={
        'form':sub_form,
        'submitted':submitted,
        'course':course,
        'current_time':current_time,
        'superuser':request.user.is_superuser
    })

@login_required
def RegisterFormView(request,pk=None):
    course = get_object_or_404(Cname, pk=pk)
    instance = RegUsers.objects.filter(course=course, user=request.user).first()
    wrong_key = 0

    submitted = (instance is not None)

    if request.method=="POST":
        sub_form = RegisterForm(request.POST or None, request.FILES or None, instance=instance)
        if sub_form.is_valid():
            key_received = sub_form.cleaned_data["secret_code"]
            if key_received == course.secret_code:
                form=sub_form.save(commit=False)
                form.user=request.user
                form.course=course
                # if 'answer' in request.FILES:
                form.save()
                submitted=True
            else:
                # sub_form=RegisterForm()
                wrong_key = 1
    else:
        sub_form=RegisterForm()

    return render(request,template_name='register_course.html',context={
        'form':sub_form,
        'submitted':submitted,
        'course':course,
        'superuser':request.user.is_superuser,
        'wrong_key':wrong_key
    })


def CourseView(request):
    created=False
    if request.method=='POST':
        course_form=CourseForm(request.POST,request.FILES)
        if course_form.is_valid():
            form=course_form.save(commit=False)
            if 'question_file' in request.FILES:
                form.question_file=request.FILES['question_file']
            form.save()
            created=True
            send_mail('Subject here', 'Assignment has been created', 'submissionPortalProject@gmail.com',['arpankhanna70@gmail.com'], fail_silently=False)
            # form.deadline_date=form.d_date
        else:
            print(course_form.errors)
    else:
        course_form=CourseForm()
    return render(request,'course_form.html',context={
        'form':course_form,
        'created':created
    })

def CreateCourseView(request):
    created=False
    if request.method=='POST':
        course_form=CreateCourseForm(request.POST,request.FILES)
        if course_form.is_valid():
            form=course_form.save(commit=False)
            form.save()
            created=True
            # form.deadline_date=form.d_date
        else:
            print(course_form.errors)
    else:
        course_form=CreateCourseForm()
    return render(request,'create_course.html',context={
        'form':course_form,
        'created':created
    })

def AssigmentList(request):
    course_list=Course.objects.all()
    temp = RegUsers.objects.filter(user=request.user)
    # course_list = []
    # for i in temp:
    #     course_list.append(Course.objects.filter(code=i.course.code))
    
    # print(course_list[0].pk)

    final_list = []

    for i in course_list:
        for j in temp:
            if i.code.code == j.course.code:
                final_list.append(i)
                break
       
    return render(request,'course_list.html',context={'course_list':final_list})

def Assignments_list(request,pk):
    if(request.user.is_superuser):
        if(request.method == 'POST'):
            # print("helo")
            sub = get_object_or_404(Submissions,pk=pk)
            course=get_object_or_404(Course,pk=sub.course.pk)
            sub.grade=request.POST.get('gde')
            sub.save()
            send_mail('Subject here', 'Here is the message grade = ' + sub.grade, 'submissionPortalProject@gmail.com',['arpankhanna70@gmail.com'], fail_silently=False)
            # print(request.POST.get('gde'))
            return render(request,'assigments_list.html',context={'course':course})
        else:
            course=get_object_or_404(Course,pk=pk)
            return render(request,'assigments_list.html',context={'course':course})
    else:
        # permission_denied(request)
        # return render(request,'permission_denied.html')
        raise PermissionDenied()

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

class SubmissionListView(SuperUserRequiredMixin,ListView):
    model=Course
    template_name='submissions_list.html'
    fields='__all__'

def GradingPage(request,pk):
    sub = get_object_or_404(Submissions,pk=pk)
    return render(request,'grading_page.html',context={'submission':sub,'pk':pk})

def AfterGrading(request,pk):
    sub = get_object_or_404(Submissions,pk=pk)
    course=get_object_or_404(Course,pk=sub.course.pk)
    if request.method=='POST':
        sub.grade=request.POST.get('grade')
        sub.save()
        return render(request,'assigments_list.html',context={'course':course})
    else:
        return render(request,'grading_page.html',context={'submission':sub,'pk':pk})

def deletingAssign(request,pk):
    course=get_object_or_404(Course,pk=pk)
    course.delete()
    return render(request,'deleteassign.html')

def AvailableListView(request):
    course_list = Cname.objects.all()

    temp = RegUsers.objects.filter(user=request.user)
    c_registerd = []
    for i in temp:
        c_registerd.append(Cname.objects.get(code=i.course))

    print(c_registerd)
    return render(request,'available_course.html',context={'course_list':course_list,'c_registerd':c_registerd})

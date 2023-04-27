from django import forms
from .models import Submissions,Course,Cname,RegUsers

class CreateCourseForm(forms.ModelForm):
    code=forms.CharField(max_length=10)
    course_name=forms.CharField(max_length = 30)
    secret_code = forms.CharField(max_length=30)
    
    class Meta():
        model=Cname
        fields=('code','course_name','secret_code')


class CourseForm(forms.ModelForm):
    name=forms.CharField(max_length=100)
    # code=forms.CharField(max_length=100)
    code = forms.ModelChoiceField(queryset=Cname.objects.all())
    question=forms.CharField(widget=forms.Textarea)
    question_file=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    deadline_date=forms.DateField(widget=forms.SelectDateWidget)
    deadline_time=forms.TimeField()
    
    class Meta():
        model=Course
        fields=('name','code','question','deadline_date','deadline_time','question_file')

class SubmissionForm(forms.ModelForm):
    class Meta():
        fields=('answer',)
        model=Submissions

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['answer']='Upload your file'

class RegisterForm(forms.ModelForm):
    secret_code = forms.CharField(max_length=30)

    class Meta():
        fields=()
        model=RegUsers

import datetime
from django import forms
from planner.models import Student, Major, Minor, Advisor, Subject

year_choices = [(r,r) for r in range(2025, datetime.date.today().year+4)]
current_year = datetime.date.today().year



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'eagle_id',
            'first_name',
            'last_name',
            'email',
            'class_year',
            'end_semester',
            'college',
            'advisor',
            'major_one',
            'major_two',
            'minor_one',
            'minor_two',
        ]
        widgets = {
            'eagle_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'class_year': forms.Select(choices=year_choices, attrs={'class': 'form-control'}),
            'end_semester': forms.Select(attrs={'class': 'form-control'}),
            'college': forms.Select(attrs={'class': 'form-control'}),
            'advisor': forms.Select(attrs={'class': 'form-control'}),
            'major_one': forms.Select(attrs={'class': 'form-control'}),
            'major_two': forms.Select(attrs={'class': 'form-control'}),
            'minor_one': forms.Select(attrs={'class': 'form-control'}),
            'minor_two': forms.Select(attrs={'class': 'form-control'}),
        }
    major_one = forms.ModelChoiceField(queryset=Subject.objects.all(), 
                                       empty_label="Select a Major", 
                                       required=True)
    major_two = forms.ModelChoiceField(queryset=Subject.objects.all(), 
                                       empty_label="Select a Major", 
                                       required=False)
    minor_one = forms.ModelChoiceField(queryset=Subject.objects.all(),
                                        empty_label="Select a Minor",
                                        required=False)
    minor_two = forms.ModelChoiceField(queryset=Subject.objects.all(),
                                        empty_label="Select a Minor",
                                        required=False)

class StudentAccountForm(StudentForm):
    class Meta(StudentForm.Meta):
        fields = [field for field in StudentForm.Meta.fields if field != 'advisor']
        widgets = {**StudentForm.Meta.widgets, 
                #    'advisor': forms.Select(attrs={'class': 'form-control'}),
                   'eagle_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})}
        # advisor = forms.ModelChoiceField(queryset=Advisor.objects.all(),
        #                                 empty_label="Select an Advisor",
        #                                 required=False)
                                        

class StudentRegisterForm(StudentForm):
    class Meta(StudentForm.Meta):
        fields = [field for field in StudentForm.Meta.fields if field != 'advisor']
        widgets = {**StudentForm.Meta.widgets}
    

class AdvisorAccountForm(forms.ModelForm):
    class Meta:
        model = Advisor
        fields = [
            'eagle_id',
            'first_name',
            'last_name',
            'email',
        ]
        widgets = {
            'eagle_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())
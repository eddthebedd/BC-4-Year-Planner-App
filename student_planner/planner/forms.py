import datetime
from django import forms
from planner.models import Planner, Course

class SemesterForm(forms.Form):
    class_one = forms.ModelChoiceField(
                    queryset=Course.objects.all(),
                    empty_label="Select Course",
                    required=True)
    class_two = forms.ModelChoiceField(
                    queryset=Course.objects.all(),
                    empty_label="Select Course",
                    required=True)
    class_three = forms.ModelChoiceField(
                    queryset=Course.objects.all(),
                    empty_label="Select Course",
                    required=True)
    class_four = forms.ModelChoiceField(
                    queryset=Course.objects.all(),
                    empty_label="Select Course",
                    required=True)
    class_five = forms.ModelChoiceField(
                    queryset=Course.objects.all(),
                    empty_label="Select Course",
                    required=False)
    class_six = forms.ModelChoiceField(
                    queryset=Course.objects.all(),
                    empty_label="Select Course",
                    required=False)
    
class PlannerForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

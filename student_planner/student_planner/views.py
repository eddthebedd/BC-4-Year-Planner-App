from django.views.generic import TemplateView
from .forms import StudentAccountForm, StudentRegisterForm, AdvisorAccountForm
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import redirect
from django.contrib import messages
from planner.models import Student, Advisor
from django.shortcuts import render
from django.contrib.auth.models import User
from .decorators import admin_required
from django.views.generic import DetailView
from .forms import StudentForm


@admin_required
def admin_page(request):
    users = User.objects.all()
    return render(request, 'admin_page.html', {'users': users})

class AccountView(UpdateView):
    template_name = 'account.html'
    success_url = '/'

    def get_form_class(self):
        if self.request.user.role == 'STUDENT':
            return StudentAccountForm
        else:
            return AdvisorAccountForm
        

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            return None

    def form_valid(self, form):
        self.request.user.save()
        if hasattr(self.request.user, 'student'):
            student = Student(
                user=self.request.user,
                **form.cleaned_data
            )
            student.save()
        else:
            if hasattr(self.request.user, 'advisor'):
                advisor = self.request.user.advisor
                for field, value in form.cleaned_data.items():
                    if field != 'students':
                        setattr(advisor, field, value)
                advisor.save()
                for student in form.cleaned_data['students']:
                    student.advisor = advisor
                    student.save()
            else:
                advisor = Advisor(
                    user=self.request.user,
                    **{k: v for k, v in form.cleaned_data.items() if k != 'students'}
                )
                advisor.save()
                for student in form.cleaned_data['students']:
                    student.advisor = advisor
                    student.save()


        return super().form_valid(form)

    def get_initial(self):
        if not self.request.user.is_authenticated:
            return {}
        
        if self.request.user.role == 'ADVISOR':
            return {
                'eagle_id': self.request.user.advisor.eagle_id,
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email,
                'students': self.request.user.advisor.student_set.all()
            }
        else:
        
            student = self.request.user.student
            initial = super().get_initial()
            user_fields = ['first_name', 'last_name', 'email']
            student_fields = ['eagle_id', 'class_year', 'end_semester', 'college', 'advisor', 'major_one', 'major_two', 'minor_one', 'minor_two']

            for field in user_fields:
                initial[field] = getattr(self.request.user, field)

            for field in student_fields:
                initial[field] = getattr(student, field)

        return initial


class StudentDetailView(DetailView):
    model = Student
    template_name = 'planner/student_detail.html'
    pk_url_kwarg = 'eagle_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentForm(instance=self.object)
        return context

class LoginView(TemplateView):
    template_name = 'index.html'

    
class RegisterView(FormView):
    form_class = StudentRegisterForm
    template_name = 'register.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to register.')
            return redirect('/login/')
        
        if request.user.registered:
            messages.warning(request, 'You have already registered.')
            return redirect('/')
        
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            return None

    def form_valid(self, form):
        self.request.user.registered = True
        self.request.user.save()

        student = Student(user=self.request.user, **form.cleaned_data)
        student.save()

        return super().form_valid(form)

    def get_initial(self):
        if not self.request.user.is_authenticated:
            return {}
        
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email

        return initial
    
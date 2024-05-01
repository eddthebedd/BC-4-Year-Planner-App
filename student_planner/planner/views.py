from typing import Any
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.db import models
from planner.models import Student, Planner, Semester, Advisor
from django.contrib import messages
from .api import PlanningCoursesAPI
from .forms import SemesterForm, PlannerForm
from django.shortcuts import render
from django.contrib.auth.models import User
from .decorators import admin_required
from django.views.generic import DetailView
from .models import Student
from django.shortcuts import render, get_object_or_404

from .validutil import validateMajor


class IndexView(TemplateView):
    template_name = 'planner/index.html'


# Landing Page for Students after Login
class StudentLandingPageView(TemplateView):
    template_name = 'planner/landing_student.html'
    redirect_field_name = 'next'

    def __init__(self, **kwargs: Any) -> None:
        self.api = PlanningCoursesAPI('http://localhost:8080')
        super().__init__(**kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # messages.error(request, 'You must be logged in to view this page.')
            return redirect('/login/')
        elif not request.user.registered:
            if request.user.role == 'STUDENT':
                # messages.error(request, 'You must be registered to view this page.')
                return redirect('/register/')
            else:
                return redirect('/admin-dashboard/')
        else:
            return super().dispatch(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(email=self.request.user.email)

        num_creds = 0
        planners = Planner.objects.filter(student=student)
        planner = planners[0] if planners else None
        if planner:
            planner.semesters = [
                ('fall_one', planner.fall_one),
                ('spring_one', planner.spring_one),
                ('fall_two', planner.fall_two),
                ('spring_two', planner.spring_two),
                ('fall_three', planner.fall_three),
                ('spring_three', planner.spring_three),
                ('fall_four', planner.fall_four),
                ('spring_four', planner.spring_four),
            ]

            for sem in planner.semesters:
                num_creds += sem[1].credit_hours

        context['progress_width'] = num_creds / 120 * 100
        context['num_creds'] = num_creds
        if planners:
            sem_1 = planners[0].fall_one
            context['planners'] = planners
        
        return context

# Course Plans View
class CoursePlansView(TemplateView) :
    template_name = 'planner/course_plans.html'


# Course Plans View
class CreatePlanView(FormView) :
    form_class = PlannerForm
    template_name = 'planner/create_plan.html'
    success_url = '/create-plan/'

    def __init__(self, **kwargs):
        self.api = PlanningCoursesAPI('http://localhost:8080')
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(email=self.request.user.email)
        planners = Planner.objects.filter(student=student)

        progress_data = {}
            
        if not planners:
            # Create empty semesters first
            semesters = [Semester.objects.create(credit_hours=0) for _ in range(8)]

            # Create the planner with the semesters
            planner = Planner.objects.create(
                student=student,
                fall_one=semesters[0],
                spring_one=semesters[1],
                fall_two=semesters[2],
                spring_two=semesters[3],
                fall_three=semesters[4],
                spring_three=semesters[5],
                fall_four=semesters[6],
                spring_four=semesters[7]
            )

            planners = Planner.objects.filter(student=student)
        
        for i, planner in enumerate(planners, start = 1):
            planner.semesters = [
                ('fall_one', planner.fall_one),
                ('spring_one', planner.spring_one),
                ('fall_two', planner.fall_two),
                ('spring_two', planner.spring_two),
                ('fall_three', planner.fall_three),
                ('spring_three', planner.spring_three),
                ('fall_four', planner.fall_four),
                ('spring_four', planner.spring_four),
            ]

            print(planner.spring_one.courses.all())

            progress_data[f'progress{i}'] = sum([sem[1].credit_hours for sem in planner.semesters])
            planner.progress_key = f'progress{i}'
            planner.progress_value = progress_data[planner.progress_key]
            planner.progress_perc = planner.progress_value / 120 * 100
            major_validation = validateMajor(planner, student)
            planner.major_validation = major_validation

        
        context['progress_data'] = progress_data
        context['planners'] = planners
        if isinstance(planner, models.Model):
            planner.save()

        return context
    
    def form_valid(self, form):
        student = Student.objects.get(email=self.request.user.email)
        semesters = [Semester.objects.create(credit_hours=0) for _ in range(8)]
        planner = Planner.objects.create(
            student=student,
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            fall_one=semesters[0],
            spring_one=semesters[1],
            fall_two=semesters[2],
            spring_two=semesters[3],
            fall_three=semesters[4],
            spring_three=semesters[5],
            fall_four=semesters[6],
            spring_four=semesters[7]
        )

        return super().form_valid(form)
    


# Explore Major View
class ExploreMajorView(TemplateView):
    template_name = 'planner/explore_major.html'

# Admin Dashboard View
class AdminDashboardView(TemplateView):
    template_name = 'planner/admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the Advisor instance for the current user
        advisor = Advisor.objects.get(user=self.request.user)
        # Get the list of students assigned to the current admin
        students = Student.objects.filter(advisor=advisor).exclude(eagle_id__isnull=True)
        # Add the students to the context
        context['students'] = students
        return context
    
class StudentDetailView(DetailView):
    model = Student
    template_name = 'planner/student_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Student, eagle_id=self.kwargs.get('eagle_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, eagle_id=self.kwargs.get('eagle_id'))
        planners = Planner.objects.filter(student=student)

        for planner in planners:
            planner.semesters = [
                ('fall_one', planner.fall_one),
                ('spring_one', planner.spring_one),
                ('fall_two', planner.fall_two),
                ('spring_two', planner.spring_two),
                ('fall_three', planner.fall_three),
                ('spring_three', planner.spring_three),
                ('fall_four', planner.fall_four),
                ('spring_four', planner.spring_four),
            ]
        context['planners'] = planners

        return context


class PlanSemester(FormView):
    form_class = SemesterForm
    template_name = 'planner/plan_semester.html'
    success_url = '../create-plan'
    def __init__(self, **kwargs: Any) -> None:
        self.api = PlanningCoursesAPI('http://localhost:8080')

        super().__init__(**kwargs)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else self.success_url
    
    def get(self, request, *args, **kwargs):
        semester_id = kwargs.get('semester_id')
        print(semester_id)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        semester = Semester.objects.get(id = int(self.kwargs.get('semester_id')))

        # Add the selected courses to the semester
        selected_courses = [
            form.cleaned_data['class_one'],
            form.cleaned_data['class_two'],
            form.cleaned_data['class_three'],
            form.cleaned_data['class_four']
        ]

        # Add optional courses if selected
        optional_courses = [
            form.cleaned_data['class_five'],
            form.cleaned_data['class_six']
        ]

        semester.courses.clear()

        credit_hours = 0
        for course in selected_courses + optional_courses:
            if course:
                semester.courses.add(course)
                data = self.api.get_courses_by_code(course.id)
                credit_hours += int(data[0].course['creditOptionIds'][0].split('.')[-2])
            semester.credit_hours = credit_hours
            print(semester.credit_hours)
            semester.save()

        return super().form_valid(form)
    
    def get_initial(self) -> dict[str, Any]:
        def number_to_word(number):
            number_word_map = {
                1: 'one',
                2: 'two',
                3: 'three',
                4: 'four',
                5: 'five',
                6: 'six',
                7: 'seven',
                8: 'eight',
                9: 'nine',
                10: 'ten',
                # Add more numbers here if needed
            }
            return number_word_map.get(number)
        
        semester_id = self.kwargs.get('semester_id')
        semester = Semester.objects.get(id=semester_id)
        courses = semester.courses.all()

        initial = super().get_initial()


        if not courses:
            return super().get_initial()

        for i, course in enumerate(courses):
            print(course)
            initial[f'class_{number_to_word(i+1)}'] = course


        return initial
    
    '''
    def get_initial(self):
        if not self.request.user.is_authenticated:
            return {}
        
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email

        return initial
        '''


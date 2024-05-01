from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from enum import Enum
from django.contrib.auth.models import AbstractUser

class Role(Enum):
    STUDENT = 'Student'
    ADVISOR = 'Advisor'
class User(AbstractUser):
    role = models.CharField(
        max_length=7,
        choices=[(role.name, role.value) for role in Role],
        default=Role.STUDENT.name,
    )
    email = models.EmailField(max_length=254, unique=True)
    registered = models.BooleanField(default=False)

class Subject(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    short_name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=200)

    def __str__(self):
        return self.long_name

class Course(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    title = models.CharField(max_length=100)
    subject_area = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    
    class Meta:
        db_table = 'planner_course'
        
    def __str__(self):
        return self.title


class Major(models.Model):
    title = models.CharField(max_length=4)
    num_credits = models.IntegerField()
    def __str__(self):
        return self.title
        #courses = models.ManyToManyField(Course, blank=True, default=None)
        #Add a many to many field in the Major to then be able to validate with courses 

class Minor(models.Model):
    title = models.CharField(max_length=4)
    num_credits = models.IntegerField()
    def __str__(self):
        return self.title
    
class Advisor(models.Model):
    def __str__(self):
        return self.first_name + " " + self.last_name
      
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, related_name="advisor")
    eagle_id = models.CharField(max_length=8)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length = 254)
    class_year = models.CharField(max_length=4) 

class Student(models.Model):
    def __str__(self):
        return self.first_name + " " + self.last_name
      
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, related_name="student")
    eagle_id = models.CharField(max_length=8)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=254, primary_key=True)
    advisor = models.ForeignKey(Advisor, default=None, on_delete=models.CASCADE, null=True)
    class_year = models.CharField(max_length=4)
    SEMESTER_CHOICES = (
        ('Spring', 'Spring'),
        ('Fall', 'Fall'),
    )
    end_semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES, default='Spring')
    major_one = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE, related_name="major_one")
    major_two = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE, related_name="major_two", null=True)
    minor_one = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE, related_name="minor_one", null=True)
    minor_two = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE, related_name="minor_two", null=True)

    class College(models.TextChoices):
        MCAS = "MCAS", _("Morrissey College of Arts and Sciences")
        CSOM = "CSOM", _("Carroll School of Management")
        CSON = "CSON", _("William F. Connell School of Nursing")
        LYNCH = "LYNCH", _("Carolyn A. and Peter S. Lynch School of Education and Human Development")
    
    college = models.CharField(
        max_length=5,
        choices=College,
    )

class Semester(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(credit_hours__lte=21),
                name='credit_hours_limit'
            )
        ]

    credit_hours = models.PositiveIntegerField(default=0)
    courses = models.ManyToManyField(Course, blank=True, default=None)
    #Add a many to many field in the Major to then be able to validate with courses
    
    

class Planner(models.Model):
    student = models.ForeignKey(Student, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    fall_one = models.ForeignKey(Semester, default=None,on_delete=models.CASCADE, related_name='planner_sem_one', null=True, blank=True)
    spring_one = models.ForeignKey(Semester,default=None, on_delete=models.CASCADE, related_name='planner_sem_two', null=True, blank=True)
    fall_two = models.ForeignKey(Semester,default=None, on_delete=models.CASCADE, related_name='planner_sem_three', null=True, blank=True)
    spring_two = models.ForeignKey(Semester,default=None, on_delete=models.CASCADE, related_name='planner_sem_four', null=True, blank=True)
    fall_three = models.ForeignKey(Semester,default=None, on_delete=models.CASCADE, related_name='planner_sem_five', null=True, blank=True)
    spring_three = models.ForeignKey(Semester, default=None,on_delete=models.CASCADE, related_name='planner_sem_six', null=True, blank=True)
    fall_four = models.ForeignKey(Semester, default=None,on_delete=models.CASCADE, related_name='planner_sem_seven', null=True, blank=True)
    spring_four = models.ForeignKey(Semester, default=None,on_delete=models.CASCADE, related_name='planner_sem_eight', null=True, blank=True)

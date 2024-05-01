from django.core.management.base import BaseCommand
from planner.models import Course, Subject
from planner.api import PlanningCoursesAPI
from tqdm import tqdm

#USAGE: python manage.py load_data <csci>
class Command(BaseCommand):
    help = 'Load data from API into database'

    def add_arguments(self, parser):
        parser.add_argument('searchTerm', nargs='?', default=None)

    def handle(self, *args, **options):
        searchTerm = options['searchTerm']
        api = PlanningCoursesAPI('http://localhost:8080')
        if searchTerm is not None:
            data = api.get_courses_by_code(searchTerm)
        else:
            data = api.get_all_courses()

        if (data != None): #Ensures the API fully transfers data
            for item in tqdm(data):
                if item.subjectArea is None or item.course is None:
                    continue
                else:
                    subject, created = Subject.objects.get_or_create(
                        id=item.subjectArea['id'],
                        defaults={
                            'short_name': item.subjectArea['shortName'],
                            'long_name': item.subjectArea['longName'],
                        }
                    )

                    course, created = Course.objects.get_or_create(
                        id=item.course['courseCode'],
                        defaults={
                            'title': item.course['title'],
                            'subject_area': subject,
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
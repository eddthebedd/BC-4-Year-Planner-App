from django.core.management.base import BaseCommand
from planner.models import Course
import requests

    #function must be run like  {python manage.py fetch_data.py csci}
    #will add all the classes for the sujectAreaId to the data along w their code, and subjectAreaID

class Command(BaseCommand):
    help = 'Fetch and save courses from the API'

    def add_arguments(self, parser): 
        parser.add_argument('subject_area_id', type=str, help='Subject Area ID to fetch courses for')

    def handle(self, *args, **options):
        subject_area_id = options['subject_area_id']
        #api_url = f"http://localhost:8080/waitlist/waitlistcourseofferings?subjectAreaId={subject_area_id}"
        #api_url = f"http://localhost:8080/planning/planningcourses/a22c81e3-a6da-4654-b48a-a434b99ab501"
        api_url = f"http://localhost:8080/planning/planningcourses"
        response = requests.get(api_url)

        if response.status_code == 200:
            print(response)
            json = response.json()

            for course in json:
                try:
                    if course['course']['subjectAreaId'] == subject_area_id:
                        print(f"Processing course: {course['course']['title']}")
                        Course.objects.create(
                            course_code = course['course']['courseCode'],
                            course_title = course['course']['title'],
                            subject_area = course['course']['subjectAreaId']
                        )

                    print(f"Processed course: {course['course']['title']}")
                    print(list(course))
                except Exception as e:
                    print(f"Error processing course {course['course']['title']}")
                    

            self.stdout.write(self.style.SUCCESS("Courses saved successfully!"))
        else:
            self.stderr.write(self.style.ERROR(f"Failed to fetch courses. Status code: {response.status_code}"))
import requests
import json
from typing import List
from .ApiDataClasses import *

class PlanningCoursesAPI:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.base_endpoint = f"{self.base_url}/planning/planningcourses"

    def get_courses_by_code(self, code) -> List[Course]:
        params = {'code': code}
        return self._make_request(self.base_endpoint, params)

    def get_course_by_id(self, course_id) -> List[Course]:
        endpoint = f"{self.base_endpoint}/{course_id}"
        return self._make_request(endpoint)

    def get_all_courses(self) -> List[Course]:
        return self._make_request(self.base_endpoint)

    def _make_request(self, endpoint, params=None):
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return [Course(**item) for item in data]
        except requests.exceptions.RequestException as e:
            # Handle exceptions
            print(f"Error: {e}")
            return None
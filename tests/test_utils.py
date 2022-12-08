import requests
from munch import munchify

base_url = "http://127.0.0.1:8000/api"
schools_url = f"{base_url}/schools"
courses_url = f"{base_url}/courses"
students_url = f"{base_url}/students"
teachers_url = f"{base_url}/teachers"
administrators_url = f"{base_url}/administrators"
transfer_url = f"{base_url}/transfer"
enrollment_url = f"{base_url}/enrollments"


# Get collections

def get_schools():
    """
    Get all schools
    """
    return _get_query_results(schools_url)


def get_students():
    """
    Get all students
    """
    return _get_query_results(students_url)


def get_teachers():
    """
    Get all teachers
    """
    return _get_query_results(teachers_url)


def get_administrators():
    """
    Get all administrators
    """
    return _get_query_results(administrators_url)


def get_courses():
    """
    Get all courses
    """
    return _get_query_results(courses_url)


# CREATE Operations

def create_student(name, school_id=None):
    return _create_person(students_url, name=name, school_id=school_id)


def create_teacher(name, school_id=None):
    return _create_person(teachers_url, name=name, school_id=school_id)


def create_administrator(name, school_id=None):
    return _create_person(administrators_url, name=name, school_id=school_id)


def create_school(name, address):
    return _create_entity(schools_url, name=name, address=address)


def create_course(name, location, teacher_id, school_id):
    return _create_entity(courses_url,
                          name=name, location=location, school=school_id, teacher=teacher_id)


# GET single entity

def get_school(school_id):
    """
    Get a specific school
    """
    return _get_single_result(f"{schools_url}/{school_id}")


def get_student(student_id):
    """
    Get a specific student
    """
    return _get_person(students_url, student_id)


def get_teacher(teacher_id):
    """
    Get a specific teacher
    """
    return _get_person(teachers_url, teacher_id)


def get_administrator(administrator_id):
    """
    Get a specific administrator
    """
    return _get_person(administrators_url, administrator_id)


def get_course(course_id):
    """
    Get a specific course
    """
    return _get_single_result(f"{courses_url}/{course_id}")


# Update single entity

def update_school(school_id, name, address):
    return _update_entity(schools_url, school_id, name=name, address=address)


def update_student(student_id, name, school_id):
    return _update_person(students_url, student_id, name, school_id)


def update_teacher(teacher_id, name, school_id):
    return _update_person(teachers_url, teacher_id, name, school_id)


def update_administrator(administrator_id, name, school_id):
    return _update_person(administrators_url, administrator_id, name, school_id)


def update_course(course_id, name, location, school_id, teacher_id):
    return _update_entity(courses_url, course_id,
                          name=name, location=location, teacher=teacher_id, school=school_id)


# Delete single entity

def delete_school(school_id):
    return _delete_entity(schools_url, school_id)


def delete_student(student_id):
    return _delete_entity(students_url, student_id)


def delete_teacher(teacher_id):
    return _delete_entity(teachers_url, teacher_id)


def delete_administrator(administrator_id):
    return _delete_entity(administrators_url, administrator_id)


def delete_course(course_id):
    return _delete_entity(courses_url, course_id)


def _get_query_results(url):
    response = requests.get(url)
    response.raise_for_status()
    return munchify(response.json()['results'])


def _create_person(url, name, school_id=None):
    if school_id is None:
        school_id = get_schools()[0]["id"]
    return _create_entity(url, name=name, school=school_id)


# Helpers methods

def _create_entity(url, **kwargs):
    response = requests.post(url, data=kwargs)
    response.raise_for_status()
    return munchify(response.json())


def _get_person(url, person_id):
    """
    Generic method to get a specific person
    """
    return _get_single_result(f"{url}/{person_id}")


def _get_single_result(url):
    response = requests.get(url)
    response.raise_for_status()
    return munchify(response.json())


def _update_person(url, person_id, name, school_id):
    return _update_entity(url, person_id, name=name, school=school_id)


def _update_entity(url, entity_id, **kwargs):
    entity_url = f"{url}/{entity_id}"
    response = requests.put(entity_url, data=kwargs)
    response.raise_for_status()
    return munchify(response.json())


def _delete_entity(url, entity_id):
    entity_url = f"{url}/{entity_id}"
    response = requests.delete(entity_url)
    response.raise_for_status()


# Additional
def entity_is_in_collection(entity, collection):
    return entity.id in [item.id for item in collection]


def get_a_school():
    schools = get_schools()
    if len(schools):
        a_school = schools[0]
    else:
        a_school = create_school(name="a_school", address="an address")
    return a_school


def get_a_teacher():
    teachers = get_teachers()
    if len(teachers):
        a_teacher = teachers[0]
    else:
        a_school = get_a_school()
        a_teacher = create_teacher(name="a_teacher", school_id=a_school.id)
    return a_teacher


def transfer(student_id, from_course_id, to_course_id):
    data = dict(
        studentId=student_id,
        fromCourseId=from_course_id,
        toCourseId=to_course_id
    )
    response = requests.post(transfer_url, data=data)
    response.raise_for_status()
    return munchify(response.json())


def create_enrollment(student_id, course_id):
    return _create_entity(enrollment_url, student=student_id, course=course_id)

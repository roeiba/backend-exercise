import pytest
import requests


# test transfer student api
from tests.test_utils import transfer, get_a_school, create_student, delete_student, entity_is_in_collection, \
    get_students, create_course, create_teacher, _create_entity, create_enrollment


@pytest.fixture
def a_student():
    a_school = get_a_school()
    a_student = create_student(name="a_student", school_id=a_school.id)
    yield a_student
    delete_student(a_student.id)
    assert not entity_is_in_collection(a_student, get_students())


def _create_test_course(name):
    a_school = get_a_school()
    a_teacher = create_teacher(name="a_teacher", school_id=a_school.id)
    course = create_course(
        name=name,
        location="Test location",
        school_id=a_school.id,
        teacher_id=a_teacher.id)
    return course


def test_transfer_student_api(a_student):
    """Test transfer student api"""

    course1 = _create_test_course("test_course_1")
    course2 = _create_test_course("test_course_2")

    enrollment = create_enrollment(student_id=a_student.id, course_id=course1.id)
    transfer(student_id=a_student.id, from_course_id=course1.id, to_course_id=course2.id)

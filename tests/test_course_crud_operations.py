"""
This module covers CRUD operations of the Course API
"""
import pytest
# test course
from random import random, randint

from tests.test_utils import get_courses, create_course, get_course, update_course, delete_course, \
    entity_is_in_collection, get_a_school, get_a_teacher, get_teachers, create_teacher, delete_teacher
import logging
_logger = logging.getLogger(__name__)


@pytest.fixture
def a_course():
    courses = get_courses()
    if len(courses):
        a_course = courses[0]
    else:
        a_school = get_a_school()
        a_teacher = get_a_teacher()
        a_course = create_course(
            name="a_course",
            location="Test location",
            school_id=a_school.id,
            teacher_id=a_teacher.id)
    yield a_course
    assert entity_is_in_collection(a_course, get_courses())
    if len(courses) == 0:
        delete_course(a_course.id)
        assert not entity_is_in_collection(a_course, get_courses())


@pytest.fixture
def a_teacher():
    a_school = get_a_school()
    a_teacher = create_teacher(name="test_teacher", school_id=a_school.id)
    yield a_teacher
    assert entity_is_in_collection(a_teacher, get_teachers())
    delete_teacher(a_teacher.id)
    assert not entity_is_in_collection(a_teacher, get_teachers())


def test_get_courses(a_course):
    courses = get_courses()
    _logger.info(courses)
    assert len(courses) > 0


def test_get_course(a_course):
    actual_course = get_course(course_id=a_course.id)
    assert actual_course.id == a_course.id


def test_create_course(a_teacher):
    i = randint(0, 10000)
    name = f"course_{i}"
    a_school = get_a_school()
    courses = get_courses()
    course = create_course(
        name=name,
        location="Test location",
        school_id=a_school.id,
        teacher_id=a_teacher.id)
    assert course.name == name
    assert course.school == a_school.id
    new_courses = get_courses()
    assert len(new_courses) == len(courses) + 1
    return course


def test_update_course(a_course):
    new_name = a_course.name + "_test"
    a_teacher = get_a_teacher()
    updated_course = update_course(
        course_id=a_course.id,
        name=new_name,
        location="Test location",
        school_id=a_course.school,
        teacher_id=a_teacher.id)
    assert new_name == updated_course.name
    # restore course values
    updated_course = update_course(
        course_id=a_course.id,
        name=a_course.name,
        location="Test location",
        school_id=a_course.school,
        teacher_id=a_teacher.id)
    assert updated_course.name == a_course.name




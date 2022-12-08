"""
This module covers CRUD operations of the Student API
"""
import pytest
# test student
from random import random, randint

from tests.test_utils import get_students, create_student, get_student, update_student, delete_student, \
    entity_is_in_collection, get_a_school
import logging
_logger = logging.getLogger(__name__)


@pytest.fixture
def a_student():
    students = get_students()
    if len(students):
        a_student = students[0]
    else:
        a_school = get_a_school()
        a_student = create_student(name="a_student", school_id=a_school.id)
    yield a_student
    assert entity_is_in_collection(a_student, get_students())
    if len(students) == 0:
        delete_student(a_student.id)
        assert not entity_is_in_collection(a_student, get_students())


def test_get_students(a_student):
    students = get_students()
    _logger.info(students)
    assert len(students) > 0


def test_get_student(a_student):
    actual_student = get_student(student_id=a_student.id)
    assert actual_student.id == a_student.id


def test_create_student():
    i = randint(0, 10000)
    name = f"student_{i}"
    a_school = get_a_school()
    students = get_students()
    student = create_student(name=name, school_id=a_school.id)
    assert student.name == name
    assert student.school == a_school.id
    new_students = get_students()
    assert len(new_students) == len(students) + 1
    return student


def test_update_student(a_student):
    new_name = a_student.name + "_test"
    updated_student = update_student(student_id=a_student.id, name=new_name, school_id=a_student.school)
    assert new_name == updated_student.name
    # restore student values
    updated_student = update_student(student_id=a_student.id, name=a_student.name, school_id=a_student.school)
    assert updated_student.name == a_student.name




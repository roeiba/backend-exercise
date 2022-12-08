"""
This module covers CRUD operations of the Teacher API
"""
import pytest
# test teacher
from random import random, randint

from tests.test_utils import get_teachers, create_teacher, get_teacher, update_teacher, delete_teacher, \
    entity_is_in_collection, get_a_school
import logging
_logger = logging.getLogger(__name__)


@pytest.fixture
def a_teacher():
    teachers = get_teachers()
    if len(teachers):
        a_teacher = teachers[0]
    else:
        a_school = get_a_school()
        a_teacher = create_teacher(name="a_teacher", school_id=a_school.id)
    yield a_teacher
    assert entity_is_in_collection(a_teacher, get_teachers())
    if len(teachers) == 0:
        delete_teacher(a_teacher.id)
        assert not entity_is_in_collection(a_teacher, get_teachers())


def test_get_teachers(a_teacher):
    teachers = get_teachers()
    _logger.info(teachers)
    assert len(teachers) > 0


def test_get_teacher(a_teacher):
    actual_teacher = get_teacher(teacher_id=a_teacher.id)
    assert actual_teacher.id == a_teacher.id


def test_create_teacher():
    i = randint(0, 10000)
    name = f"teacher_{i}"
    a_school = get_a_school()
    teachers = get_teachers()
    teacher = create_teacher(name=name, school_id=a_school.id)
    assert teacher.name == name
    assert teacher.school == a_school.id
    new_teachers = get_teachers()
    assert len(new_teachers) == len(teachers) + 1
    return teacher


def test_update_teacher(a_teacher):
    new_name = a_teacher.name + "_test"
    updated_teacher = update_teacher(teacher_id=a_teacher.id, name=new_name, school_id=a_teacher.school)
    assert new_name == updated_teacher.name
    # restore teacher values
    updated_teacher = update_teacher(teacher_id=a_teacher.id, name=a_teacher.name, school_id=a_teacher.school)
    assert updated_teacher.name == a_teacher.name




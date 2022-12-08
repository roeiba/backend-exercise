"""
This module covers CRUD operations of the Administrator API
"""
import pytest
# test administrator
from random import random, randint

from tests.test_utils import get_administrators, create_administrator, get_administrator, update_administrator, delete_administrator, \
    entity_is_in_collection, get_a_school
import logging
_logger = logging.getLogger(__name__)


@pytest.fixture
def a_administrator():
    administrators = get_administrators()
    if len(administrators):
        a_administrator = administrators[0]
    else:
        a_school = get_a_school()
        a_administrator = create_administrator(name="a_administrator", school_id=a_school.id)
    yield a_administrator
    assert entity_is_in_collection(a_administrator, get_administrators())
    if len(administrators) == 0:
        delete_administrator(a_administrator.id)
        assert not entity_is_in_collection(a_administrator, get_administrators())


def test_get_administrators(a_administrator):
    administrators = get_administrators()
    _logger.info(administrators)
    assert len(administrators) > 0


def test_get_administrator(a_administrator):
    actual_administrator = get_administrator(administrator_id=a_administrator.id)
    assert actual_administrator.id == a_administrator.id


def test_create_administrator():
    i = randint(0, 10000)
    name = f"administrator_{i}"
    a_school = get_a_school()
    administrators = get_administrators()
    administrator = create_administrator(name=name, school_id=a_school.id)
    assert administrator.name == name
    assert administrator.school == a_school.id
    new_administrators = get_administrators()
    assert len(new_administrators) == len(administrators) + 1
    return administrator


def test_update_administrator(a_administrator):
    new_name = a_administrator.name + "_test"
    updated_administrator = update_administrator(administrator_id=a_administrator.id, name=new_name, school_id=a_administrator.school)
    assert new_name == updated_administrator.name
    # restore administrator values
    updated_administrator = update_administrator(administrator_id=a_administrator.id, name=a_administrator.name, school_id=a_administrator.school)
    assert updated_administrator.name == a_administrator.name




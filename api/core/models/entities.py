from django.db import models

from core.models import School


class Person(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Administrator(Person):
    pass


class Teacher(Person):
    pass


class Student(Person):
    pass

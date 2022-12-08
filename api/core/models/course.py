from django.db import models

from core.models import School
from core.models.entities import Teacher, Student


class Course(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    location = models.TextField(blank=False, null=False)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """
    Each course can have 0-many students.
    Each student can have 0-many courses.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.student, self.course)

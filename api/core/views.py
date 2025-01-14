import logging

from core.models import (
    School,
    Course,
    Enrollment,
    Student,
    Teacher,
    Administrator,
)
from core.serializers import (
    SchoolSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    StudentSerializer,
    TeacherSerializer,
    AdministratorSerializer,
)
from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, bad_request
from rest_framework.response import Response

_logger = logging.getLogger(__name__)


class EntityCRUD(viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin):
    pass


class SchoolViewSet(EntityCRUD):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetails(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SchoolStats(generics.GenericAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        school = self.get_object()
        result = {
            'id': school.id,
            'courses': _count_items(Course, school_id=school.id),
            'admins': _count_items(Administrator, school_id=school.id),
            'teachers': _count_items(Teacher, school_id=school.id),
            'students': _count_items(Student, school_id=school.id),
        }
        return Response(result)


class CourseViewSet(EntityCRUD):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(EntityCRUD):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class StudentViewSet(EntityCRUD):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(EntityCRUD):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class AdministratorViewSet(EntityCRUD):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer


@api_view(['POST'])
def transfer_student(request):
    """
    Transfer student to another course
    """
    student_id = request.data['studentId']
    from_course_id = request.data['fromCourseId']
    to_course_id = request.data['toCourseId']

    _logger.info("Verify student")
    try:
        Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise NotFound(f"Student {student_id} does not exist")

    _logger.info("Verify from course")
    try:
        Course.objects.get(pk=from_course_id)
    except Course.DoesNotExist:
        raise NotFound(f"Course {from_course_id} does not exist")

    _logger.info("Verify to course")
    try:
        course = Course.objects.get(pk=to_course_id)
    except Course.DoesNotExist:
        raise NotFound(f"Course {to_course_id} does not exist")

    _logger.info("Verify enrollments")
    try:
        enrollment = Enrollment.objects.get(course=from_course_id, student=student_id)
        _logger.info("transferring student...")
        enrollment.course = course
        enrollment.save()
    except Enrollment.DoesNotExist as exception:
        raise bad_request(f"Student {student_id} is not registered for course {from_course_id}", exception)

    _logger.info("Return result")
    return Response({
        "message": "Transferred student {} from course {} to course {}".format(
            student_id, request.data['fromCourseId'], request.data['toCourseId']
        )
    })


def _count_items(model, school_id):
    return model.objects.filter(school=school_id).count()

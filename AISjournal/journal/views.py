from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework.views import APIView

from AISjournal.middle import CsrfExemptSessionAuthentication
from . import serializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from .models import Student, Post, Group, Colleague, PreparationPlan, Speciality, FormAttestation, Disciplines, \
    LevelPreparationPPCCZ, GroupDisciplines, EmployeeHelpLesson, Classes, EvaluationClasses
from .serializer import StudentSerializer, GroupSerializer, ColleagueSerializer, PostSerializer, \
    PreparationPlanSerializer, SpecialitySerializer, FormAttestationSerializer, DisciplinesSerializer, \
    LevelPreparationPPCCZSerializer, GroupDisciplinesSerializer, EmployeeHelpLessonSerializer, ClassesSerializer, \
    EvaluationClassesSerializer, UserSerializer, GroupStudSerializer, GroupStudDelSerializer


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # Экземпляр `django.contrib.auth.User`.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class GetCSRFToken(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})


# Студенты
class StudentAPIView(APIView):
    def get(self, request):
        lst = Student.objects.values('id', 'fist_name', 'last_name', 'patronymic')
        return Response({'students': lst})

    def post(self, request):
        post_new = Student.objects.create(
            fist_name=request.data['fist_name'],
            last_name=request.data['last_name'],
            patronymic=request.data['patronymic'],
            birthday=request.data['birthday'],
            place_residence=request.data['place_residence'],
            place_registration=request.data['place_registration'],
            telephone=request.data['telephone'],
            number_personal_file=request.data['number_personal_file'],
            year_receipt=request.data['year_receipt'],
            email=request.data['email']
        )
        return Response({'post': model_to_dict(post_new)})


class StudentAPIViewID(APIView):
    def get(self, request, pk):
        lst = Student.objects.get(pk=pk)
        serializer = StudentSerializer(instance=lst)
        return Response({'student': serializer.data})

    def delete(self, request, pk):
        Student.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Student.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = StudentSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Должность
class PostAPIView(APIView):
    def get(self, request):
        lst = Post.objects.values_list('id', flat=True)
        return Response({'posts': list(lst)})

    def post(self, request):
        post_new = Post.objects.create(
            name=request.data['name']
        )
        return Response({'post': model_to_dict(post_new)})


class PostAPIViewID(APIView):
    def get(self, request, pk):
        lst = Post.objects.get(pk=pk)
        serializer = PostSerializer(instance=lst)
        return Response({'post': serializer.data})

    def delete(self, request, pk):
        Post.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = PostSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Групппы
class GroupAPIView(APIView):
    def get(self, request, pk=None):
        lst = Group.objects.values('id', 'number')
        return Response({'groups': lst})

    def post(self, request):
        data = request.data

        new_student = Group.objects.create(
            colleague_id=data["colleague_id"],
            plan_id=data['plan_id'],
            speciality_id=data["speciality_id"],
            number=data['number'],
            year_receipt=data['year_receipt'],
            school_graduation_class=data['school_graduation_class'],
            form_education=data['form_education']
        )
        for student in data["student"]:
            student_obj = Student.objects.get(pk=student)
            new_student.student.add(student_obj)

        serializer = GroupSerializer(new_student)

        return Response(serializer.data)


class GroupStudAPIViewID(APIView):
    def get(self, request, pk):
        lst = Group.objects.get(pk=pk)
        serializer = GroupStudSerializer(instance=lst)
        return Response({'group-student': serializer.data})

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Group.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = GroupStudDelSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = GroupStudSerializer(instance=instance)
        return Response({"post": serializer.data})


class GroupStudDelAPIViewID(APIView):
    def get(self, request, pk):
        lst = Group.objects.get(pk=pk)
        serializer = GroupStudDelSerializer(instance=lst)
        return Response({'group-student-del': serializer.data})

    def delete(self, request,):
        Group.objects.filter('student').delete()
        return Response(status=status.HTTP_200_OK)


class GroupAPIViewID(APIView):
    def get(self, request, pk):
        lst = Group.objects.get(pk=pk)
        serializer = GroupSerializer(instance=lst)
        return Response({'group': serializer.data})

    def delete(self, request, pk):
        Group.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Group.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = GroupSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Сотрудники
class ColleagueAPIView(APIView):
    def get(self, request):
        lst = Colleague.objects.values('id', 'name')
        return Response({'colleagues': lst})

    def post(self, request):
        post_colleague = Colleague.objects.create(
            last_name=request.data['last_name'],
            fist_name=request.data['fist_name'],
            patronymic=request.data['patronymic'],
            full_name=request.data['name'],
            telephone=request.data['telephone'],
            post_id=request.data['post'],
        )
        return Response({'Post': model_to_dict(post_colleague)})


class ColleagueAPIViewID(APIView):
    def get(self, request, pk):
        lst = Colleague.objects.get(pk=pk)
        serializer = ColleagueSerializer(instance=lst)
        return Response({'colleague': serializer.data})

    def delete(self, request, pk):
        Colleague.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Colleague.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = ColleagueSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# План подготовки
class PreparationPlanAPIView(APIView):
    def get(self, request):
        lst = PreparationPlan.objects.values_list('id', flat=True)
        return Response({'PreparationPlan': list(lst)})

    def post(self, request):
        post_preparation_plan = PreparationPlan.objects.create(
            level_preparation_PPCCZ=request.data['level_preparation_PPCCZ'],
            number_educational_building=request.data['number_educational_building']
        )
        return Response({'post': model_to_dict(post_preparation_plan)})


class PreparationPlanAPIViewID(APIView):
    def get(self, request, pk):
        lst = PreparationPlan.objects.get(pk=pk)
        serializer = PreparationPlanSerializer(instance=lst)
        return Response({'PreparationPlan': serializer.data})

    def delete(self, request, pk):
        PreparationPlan.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = PreparationPlan.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = PreparationPlanSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Специальность
class SpecialityAPIView(APIView):
    def get(self, request):
        lst = Speciality.objects.values_list('id', flat=True)
        return Response({'speciality': list(lst)})

    def post(self, request):
        post_speciality = Speciality.objects.create(
            cod=request.data['cod'],
            name=request.data['name']
        )
        return Response({'post': model_to_dict(post_speciality)})


class SpecialityAPIViewID(APIView):
    def get(self, request, pk):
        lst = Speciality.objects.get(pk=pk)
        serializer = SpecialitySerializer(instance=lst)
        return Response({'speciality': serializer.data})

    def delete(self, request, pk):
        Speciality.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Speciality.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = SpecialitySerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Форма аттестация
class FormAttestationAPIView(APIView):
    def get(self, request):
        lst = FormAttestation.objects.values_list('id', flat=True)
        return Response({'FormAttestation': list(lst)})

    def post(self, request):
        post_speciality = FormAttestation.objects.create(
            name=request.data['name']
        )
        return Response({'post': model_to_dict(post_speciality)})


class FormAttestationAPIViewID(APIView):
    def get(self, request, pk):
        lst = FormAttestation.objects.get(pk=pk)
        serializer = FormAttestationSerializer(instance=lst)
        return Response({'FormAttestation': serializer.data})

    def delete(self, request, pk):
        FormAttestation.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = FormAttestation.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = FormAttestationSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Дисциплина
class DisciplinesAPIView(APIView):
    def get(self, request):
        lst = Disciplines.objects.values_list('id', flat=True)
        return Response({'Disciplines': list(lst)})

    def post(self, request):
        post_speciality = Disciplines.objects.create(
            index=request.data['index'],
            name=request.data['name']
        )
        return Response({'post': model_to_dict(post_speciality)})


class DisciplinesAPIViewID(APIView):
    def get(self, request, pk):
        lst = Disciplines.objects.get(pk=pk)
        serializer = DisciplinesSerializer(instance=lst)
        return Response({'Disciplines': serializer.data})

    def delete(self, request, pk):
        Disciplines.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Disciplines.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = DisciplinesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Уровень подготовки
class LevelPreparationPPCCZAPIView(APIView):
    def get(self, request):
        lst = LevelPreparationPPCCZ.objects.values_list('id', flat=True)
        return Response({'LevelPreparationPPCCZ': list(lst)})

    def post(self, request):
        post_speciality = LevelPreparationPPCCZ.objects.create(
            name=request.data['name']
        )
        return Response({'post': model_to_dict(post_speciality)})


class LevelPreparationPPCCZAPIViewID(APIView):
    def get(self, request, pk):
        lst = LevelPreparationPPCCZ.objects.get(pk=pk)
        serializer = LevelPreparationPPCCZSerializer(instance=lst)
        return Response({'LevelPreparationPPCCZ': serializer.data})

    def delete(self, request, pk):
        LevelPreparationPPCCZ.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = LevelPreparationPPCCZ.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = LevelPreparationPPCCZSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Дисциплина групп
class GroupDisciplinesAPIView(APIView):
    def get(self, request):
        lst = GroupDisciplines.objects.values_list('id', flat=True)
        return Response({'GroupDisciplines': list(lst)})

    def post(self, request):
        post_speciality = GroupDisciplines.objects.create(
            id_group=request.data['id_group'],
            id_disciplines=request.data['id_disciplines'],
            leading_teacher=request.data['leading_teacher'],
            form_intermediate_certification=request.data['form_intermediate_certification'],
            term=request.data['term'],
            data_compilation=request.data['data_compilation'],
            work_interaction_teacher=request.data['work_interaction_teacher'],
            total_hours_independent_work=request.data['total_hours_independent_work'],
            lab_practice_classes=request.data['lab_practice_classes'],
            lab_division_subgroups=request.data['lab_division_subgroups'],
            course_design=request.data['course_design'],
            course_division_subgroups=request.data['course_division_subgroups'],
            design_course_projects=request.data['design_course_projects'],
            consultations=request.data['consultations'],
            examination=request.data['examination'],
        )
        return Response({'post': model_to_dict(post_speciality)})


class GroupDisciplinesAPIViewID(APIView):
    def get(self, request, pk):
        lst = GroupDisciplines.objects.get(pk=pk)
        serializer = GroupDisciplinesSerializer(instance=lst)
        return Response({'GroupDisciplines': serializer.data})

    def delete(self, request, pk):
        GroupDisciplines.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = GroupDisciplines.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = GroupDisciplinesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Сотрудник_проведенный_занятие
class EmployeeHelpLessonAPIView(APIView):
    def get(self, request):
        lst = EmployeeHelpLesson.objects.values('id')
        return Response({'EmployeeHelpLesson': lst})

    def post(self, request):
        post_speciality = EmployeeHelpLesson.objects.create(
            colleague=request.data['colleague'],
            group_disciplines=request.data['group_disciplines'],
        )
        return Response({'post': model_to_dict(post_speciality)})


class EmployeeHelpLessonAPIViewID(APIView):
    def get(self, request, pk):
        lst = EmployeeHelpLesson.objects.get(pk=pk)
        serializer = EmployeeHelpLessonSerializer(instance=lst)
        return Response({'EmployeeHelpLesson': serializer.data})

    def delete(self, request, pk):
        EmployeeHelpLesson.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = EmployeeHelpLesson.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = EmployeeHelpLessonSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Занятия
class ClassesAPIView(APIView):
    def get(self, request):
        lst = Classes.objects.values('id')
        return Response({'Classes': lst})

    def post(self, request):
        post_speciality = Classes.objects.create(
            id_col_ruled_occupation=request.data['id_col_ruled_occupation'],
            number_classes=request.data['number_classes'],
            names=request.data['names'],
            number_hours=request.data['number_hours'],
            task_independent_work=request.data['task_independent_work'],
        )
        return Response({'post': model_to_dict(post_speciality)})


class ClassesAPIViewID(APIView):
    def get(self, request, pk):
        lst = Classes.objects.get(pk=pk)
        serializer = ClassesSerializer(instance=lst)
        return Response({'Classes': serializer.data})

    def delete(self, request, pk):
        Classes.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Classes.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = ClassesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Оценка занятий
class EvaluationClassesAPIView(APIView):
    def get(self, request):
        lst = EvaluationClasses.objects.values('id')
        return Response({'EvaluationClasses': lst})

    def post(self, request):
        post_speciality = EvaluationClasses.objects.create(
            student=request.data['student'],
            classes=request.data['classes'],
            valuation=request.data['valuation'],
        )
        return Response({'post': model_to_dict(post_speciality)})


class EvaluationClassesAPIViewID(APIView):
    def get(self, request, pk):
        lst = EvaluationClasses.objects.get(pk=pk)
        serializer = EvaluationClassesSerializer(instance=lst)
        return Response({'EvaluationClasses': serializer.data})

    def delete(self, request, pk):
        EvaluationClasses.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = EvaluationClasses.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = EvaluationClassesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


# Пользователи
class UserAPIView(APIView):
    def get(self, request):
        lst = User.objects.values('id', 'username')
        return Response({'User': lst})

    def post(self, request):
        post_speciality = User.objects.create(
            username=request.data['username'],
            password=request.data['password'],
        )
        return Response({'post': model_to_dict(post_speciality)})


class UserAPIViewID(APIView):
    def get(self, request, pk):
        lst = User.objects.get(pk=pk)
        serializer = UserSerializer(instance=lst)
        return Response({'User': serializer.data})

    def delete(self, request, pk):
        User.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


def index(request):
    return render(request, 'main/index.html')



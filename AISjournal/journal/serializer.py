from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import empty

from .models import Student, Post, Group, Colleague, PreparationPlan, Speciality, FormAttestation, Disciplines, \
    LevelPreparationPPCCZ, GroupDisciplines, EmployeeHelpLesson, Classes, EvaluationClasses


# Группы
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('student', 'colleague', 'plan', 'speciality', 'number', 'year_receipt', 'school_graduation_class',
                  'form_education')

    def to_representation(self, instance):
        rep = super(GroupSerializer, self).to_representation(instance)
        rep['student'] = StudentSerializer(instance.student.all(), many=True).data
        rep['colleague'] = instance.colleague.last_name
        rep['plan'] = instance.plan.level_preparation_PPCCZ
        rep['speciality'] = instance.speciality.name
        return rep


class GroupStudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('number', 'student',)


class GroupStudDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('student',)


# Студенты
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'fist_name', 'last_name', 'patronymic', 'birthday', 'place_residence', 'place_registration',
                  'telephone', 'number_personal_file', 'year_receipt', 'email')


# Должность
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'name',)


# Сотрудники
class ColleagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colleague
        fields = ('id', 'fist_name', 'last_name', 'patronymic', 'telephone', 'post')


class ColleagueNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colleague
        fields = ('id', 'name')


# План подготовки
class PreparationPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationPlan
        fields = ('id', 'level_preparation_PPCCZ', 'number_educational_building')


# Специальность
class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ('id', 'cod', 'name')


# Форма аттестация
class FormAttestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAttestation
        fields = ('id', 'name')


# Дисциплина
class DisciplinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplines
        fields = ('id', 'index', 'name')


# Уровень подготовки
class LevelPreparationPPCCZSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelPreparationPPCCZ
        fields = ('id', 'name')


# Дисциплина групп
class GroupDisciplinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDisciplines
        fields = ('id', 'id_group', 'id_disciplines', 'form_intermediate_certification', 'term', 'data_compilation',
                  'work_interaction_teacher', 'total_hours_independent_work', 'lab_practice_classes',
                  'lab_division_subgroups', 'course_design', 'course_division_subgroups', 'design_course_projects',
                  'consultations', 'examination')

    def to_representation(self, instance):
        rep = super(GroupDisciplinesSerializer, self).to_representation(instance)
        rep['id_group'] = instance.id_group.number
        rep['id_disciplines'] = instance.id_disciplines.name
        rep['leading_teacher'] = instance.leading_teacher.last_name
        rep['form_intermediate_certification'] = instance.form_intermediate_certification.name
        return rep


# Сотрудник_проведенный_занятие
class EmployeeHelpLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeHelpLesson
        fields = ('id', 'colleague', 'group_disciplines')

    def to_representation(self, instance):
        rep = super(EmployeeHelpLessonSerializer, self).to_representation(instance)
        rep['colleague'] = instance.colleague.fist_name
        rep['group_disciplines'] = instance.group_disciplines.term
        return rep


# Занятия
class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ('id', 'id_col_ruled_occupation', 'number_classes', 'names', 'number_hours', 'task_independent_work')


# Оценка занятий
class EvaluationClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationClasses
        fields = ('id', 'student', 'classes', 'valuation')

    def to_representation(self, instance):
        rep = super(EvaluationClassesSerializer, self).to_representation(instance)
        rep['student'] = instance.student.last_name
        return rep


# Пользователи
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


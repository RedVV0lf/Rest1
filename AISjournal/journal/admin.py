from django.contrib import admin
from .models import Student, Speciality, Post, Colleague, PreparationPlan, Group, LevelPreparationPPCCZ, Disciplines, FormAttestation, GroupDisciplines, EmployeeHelpLesson, Classes, EvaluationClasses

admin.site.register(Student),
admin.site.register(Speciality),
admin.site.register(Post),
admin.site.register(Colleague),
admin.site.register(PreparationPlan),
admin.site.register(Group),
admin.site.register(LevelPreparationPPCCZ),
admin.site.register(Disciplines),
admin.site.register(FormAttestation),
admin.site.register(GroupDisciplines),
admin.site.register(EmployeeHelpLesson),
admin.site.register(Classes),
admin.site.register(EvaluationClasses)


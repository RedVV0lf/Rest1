from django.db import models


# Студент
class Student(models.Model):
    fist_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=40)
    patronymic = models.CharField('Отчество', max_length=30)
    birthday = models.DateField('Дата рождения')
    place_residence = models.CharField('Место проживания', max_length=100)
    place_registration = models.CharField('Место прописки', max_length=100)
    telephone = models.CharField('Телефон', max_length=12)
    number_personal_file = models.CharField('Личное дело', max_length=50)
    year_receipt = models.DateField('Год поступления')
    email = models.CharField('Email', max_length=50)

    def __str__(self):
        return f'{self.last_name} {self.fist_name} {self.patronymic} {self.birthday}'


# Специальность
class Speciality(models.Model):
    cod = models.CharField('Код ', max_length=8)
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.cod


# Должности
class Post(models.Model):
    name = models.CharField('Должность', max_length=30, db_index=True)

    def __str__(self):
        return self.name


# Сотрудники
class Colleague(models.Model):
    last_name = models.CharField('Фамилия', max_length=40)
    fist_name = models.CharField('Имя', max_length=20)
    patronymic = models.CharField('Отчество', max_length=30)
    name = models.CharField('ФИО', max_length=150)
    telephone = models.CharField('Телефон', max_length=12)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.last_name} {self.fist_name} {self.patronymic}'


# План подготовки
class PreparationPlan(models.Model):
    level_preparation_PPCCZ = models.CharField('Уровень подготовки ППССЗ', max_length=5)
    number_educational_building = models.CharField('№ Учебного корпуса', max_length=2)

    def __str__(self):
        return self.level_preparation_PPCCZ


# Группа и Г/С
class Group(models.Model):
    student = models.ManyToManyField(Student)
    colleague = models.ForeignKey('Colleague', on_delete=models.PROTECT)
    plan = models.ForeignKey('PreparationPlan', on_delete=models.PROTECT)
    speciality = models.ForeignKey('Speciality', on_delete=models.PROTECT)
    number = models.CharField('Номер', max_length=5)
    year_receipt = models.DateField('Год поступления')
    school_graduation_class = models.CharField('Класс окончания школы', max_length=10)
    form_education = models.CharField('Форма обучения', max_length=10)

    def __str__(self):
        return f'{self.number} ({self.year_receipt})'


# Уровень подготовки
class LevelPreparationPPCCZ(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name


# Дисциплина
class Disciplines(models.Model):
    index = models.CharField('Индекс', max_length=10)
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.index


# Форма аттестация
class FormAttestation(models.Model):
    name = models.CharField('Название', max_length=30)

    def __str__(self):
        return self.name


# Дисциплина групп
class GroupDisciplines(models.Model):
    id_group = models.ForeignKey(Group, on_delete=models.PROTECT)
    id_disciplines = models.ForeignKey(Disciplines, on_delete=models.PROTECT, null=True)
    leading_teacher = models.ForeignKey(Colleague, on_delete=models.PROTECT)
    form_intermediate_certification = models.ForeignKey(FormAttestation, on_delete=models.PROTECT)
    term = models.IntegerField('Семестр')
    data_compilation = models.DateField('Дата составления')
    work_interaction_teacher = models.IntegerField('Работа по взаимодействия с преподавателем(часов)')
    total_hours_independent_work = models.IntegerField('Всего часов самостоятельных работ')
    lab_practice_classes = models.IntegerField('Лабораторные или Практические занятия(часов)')
    lab_division_subgroups = models.IntegerField('Лабораторные с делением на подгруппы(часов)')
    course_design = models.IntegerField('Курсовое проектирование')
    course_division_subgroups = models.IntegerField('Курсовые с делением на подгруппы(часов)')
    design_course_projects = models.IntegerField('Проектирование курсовых проектов(часов) ')
    consultations = models.IntegerField('Консультирование(часов)')
    examination = models.IntegerField('Экзамен(часов)')

    def __str__(self):
        return str(self.id_group)


# Сотрудник_проведенный_занятие
class EmployeeHelpLesson(models.Model):
    colleague = models.ForeignKey(Colleague, on_delete=models.CASCADE)
    group_disciplines = models.ForeignKey(GroupDisciplines, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.colleague}'


# Занятия
class Classes(models.Model):
    id_col_ruled_occupation = models.ForeignKey(EmployeeHelpLesson, on_delete=models.PROTECT)
    number_classes = models.IntegerField('№ занятия')
    names = models.CharField('Наименование', max_length=250)
    number_hours = models.IntegerField('Количество часов ')
    task_independent_work = models.CharField('Задание самостоятельной работы', max_length=250)

    def __str__(self):
        return str(self.names)


# Оценка занятий
class EvaluationClasses(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    valuation = models.CharField('Оценка', max_length=5)

    def __str__(self):
        return str(self.student)




from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from journal.views import StudentAPIView, StudentAPIViewID, PostAPIView, PostAPIViewID, GroupAPIView, GroupAPIViewID, \
    ColleagueAPIView, ColleagueAPIViewID, PreparationPlanAPIView, PreparationPlanAPIViewID, SpecialityAPIView, \
    SpecialityAPIViewID, FormAttestationAPIView, FormAttestationAPIViewID, DisciplinesAPIView, DisciplinesAPIViewID, \
    LevelPreparationPPCCZAPIView, LevelPreparationPPCCZAPIViewID, GroupDisciplinesAPIView, GroupDisciplinesAPIViewID, \
    EmployeeHelpLessonAPIView, EmployeeHelpLessonAPIViewID, ClassesAPIView, ClassesAPIViewID, EvaluationClassesAPIView,\
    EvaluationClassesAPIViewID, UserAPIView, UserAPIViewID, GroupStudAPIViewID, GroupStudDelAPIViewID, \
    ExampleView, GetCSRFToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('', include('journal.urls')),
    path('api/v1/studentlist/', StudentAPIView.as_view()),
    path('api/v1/studentlist/<int:pk>', StudentAPIViewID.as_view()),
    path('api/v1/postlist/', PostAPIView.as_view()),
    path('api/v1/postlist/<int:pk>', PostAPIViewID.as_view()),
    path('api/v1/grouplist/', GroupAPIView.as_view()),
    path('api/v1/grouplist/<int:pk>', GroupAPIViewID.as_view()),
    path('api/v1/groupstudlist/<int:pk>', GroupStudAPIViewID.as_view()),
    path('api/v1/group-stud-del/<int:pk>', GroupStudDelAPIViewID.as_view()),
    path('api/v1/colleaguelist/', ColleagueAPIView.as_view()),
    path('api/v1/colleaguelist/<int:pk>', ColleagueAPIViewID.as_view()),
    path('api/v1/preparation_plan_list/', PreparationPlanAPIView.as_view()),
    path('api/v1/preparation_plan_list/<int:pk>', PreparationPlanAPIViewID.as_view()),
    path('api/v1/specialitylist/', SpecialityAPIView.as_view()),
    path('api/v1/specialitylist/<int:pk>', SpecialityAPIViewID.as_view()),
    path('api/v1/formattestationlist/', FormAttestationAPIView.as_view()),
    path('api/v1/formattestationlist/<int:pk>', FormAttestationAPIViewID.as_view()),
    path('api/v1/disciplineslist/', DisciplinesAPIView.as_view()),
    path('api/v1/disciplineslist/<int:pk>', DisciplinesAPIViewID.as_view()),
    path('api/v1/levelpreparationlist/', LevelPreparationPPCCZAPIView.as_view()),
    path('api/v1/levelpreparationlist/<int:pk>', LevelPreparationPPCCZAPIViewID.as_view()),
    path('api/v1/groupdisciplineslist/', GroupDisciplinesAPIView.as_view()),
    path('api/v1/groupdisciplineslist/<int:pk>', GroupDisciplinesAPIViewID.as_view()),
    path('api/v1/employeehelplessonlist/', EmployeeHelpLessonAPIView.as_view()),
    path('api/v1/employeehelplessonlist/<int:pk>', EmployeeHelpLessonAPIViewID.as_view()),
    path('api/v1/classeslist/', ClassesAPIView.as_view()),
    path('api/v1/classeslist/<int:pk>', ClassesAPIViewID.as_view()),
    path('api/v1/evaluationclasseslist/', EvaluationClassesAPIView.as_view()),
    path('api/v1/evaluationclasseslist/<int:pk>', EvaluationClassesAPIViewID.as_view()),
    path('api/v1/userlist/', UserAPIView.as_view()),
    path('api/v1/userlist/<int:pk>', UserAPIViewID.as_view()),
    path('api/login', ExampleView.as_view()),
    path('api/v1/csrf_cookie', GetCSRFToken.as_view()),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

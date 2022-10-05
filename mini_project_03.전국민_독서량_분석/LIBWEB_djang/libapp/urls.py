
from django.urls import path
from . import views 
from . import views

app_name='libapp'


urlpatterns = [
    
    path('list/', views.lib_like),
    path('createTable/', views.createTable),
    # path('insertTest/', views.set_Survey_Insert_test),
    # path('list/', views.view_Survey_List),
    path('survey/', views.view_Survey),
    path('insert/', views.set_Survey_Insert),
    # path('analysis/',views.survey_Analysis),
    path('index/',views.index),
    path('analysis_new/',views.survey_Analysis),
    path('survey_new/',views.survey_new),
    # path('page_control/lib_list_page_new/',views.view_lib_list_Page, name='lib_list_page'),
    path('lib_insert_form_new/',views.lib_insert_form_new),
    path('about/',views.about),
    path('lib_list/',views.view_lib_List),
    path('page_control/lib_list_page/',views.view_lib_list_Page,name='lib_list_page'),
    # path('lib_insert_form/',views.view_lib_Insert),
    path('lib_insert/',views.set_lib_Insert),
    path('register/', views.register_lib),
    path('login/', views.login_lib),
    path('logout/', views.set_Logout),
    # path('main/', views.main),
    path('insertTable/', views.createTable),
    path('insert_mem/', views.set_Member_Insert),
    path('main/', views.getlogin),
    
]

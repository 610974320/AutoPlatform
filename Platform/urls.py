from django.urls import path
from django.conf.urls import url,include
from Platform import views

urlpatterns = [
    url(r'^get_verify/$', views.get_verify),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^index/$', views.index),
    url(r'^query/$', views.query),
    url(r'^user_info/$', views.user_info),
    url(r'^update_info/$', views.update_info),
    url(r'^user_pwd/$', views.user_pwd),
    url(r'^save_pwd/$', views.save_pwd),
    url(r'^get_project/$', views.get_project),
    url(r'^add_project/$', views.add_project),
    url(r'^project_list/$', views.project_list),
    url(r'^update_project/$', views.update_project),
    url(r'^delete_project/$', views.delete_project),
    url(r'^search_project/$', views.search_project),
    url(r'^get_managecase/$', views.get_managecase),
    url(r'^add_case/$', views.add_case),
    url(r'^case_list/$', views.case_list),
    url(r'^update_case/$', views.update_case),
    url(r'^delete_case/$', views.delete_case),
    url(r'^execute_case/$', views.execute_case),
    url(r'^copy_case/$', views.copy_case)
]
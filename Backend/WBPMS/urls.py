from django.urls import path
from WBPMS import views
from WBPMS.views import *
from django.contrib.auth import views as pass_views
urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
 
 ######reset password################################

    path('password_reset/', pass_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',pass_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',pass_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',pass_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('reset',pass_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

####### drug management #########
    path('', views.index, name='index'),
    path('manageDrug', views.manageDrug, name="manageDrug"),
    path('search', views.search, name='search'),
    path('category', views.category, name='category'),
    
    path('viewdrug/<str:id>', views.viewDrug, name='viewDrug'),
    path('J_update/<str:id>', views.J_update, name='J_update'),
    path('L_update/<str:id>', views.L_update, name='L_update'),

    path('viewdrugs', views.viewDrugs, name='viewDrugs'),
    path('add_drugs', views.add_drug, name='add_drug'),
    # path('viewSuper', views.viewSuper, name='viewSuper'),

    # path('expireddrug', views.expireddrug, name='expireddrug'),
    path('productList', views.productList, name='productList'),
    path('aboutus', views.aboutUs, name='aboutUs'),
    path('contactus', views.contactus, name='contactus'),

    path('createbill', views.J_CreateBill, name='J_CreateBill'),
    path('sold_drug', views.sold_drug, name='sold_drug'),
    # path('some_view', views.some_view, name='some_view'),

    
    path('lebu_branch', views.lebu_branch, name='lebu_branch'),
    path('jemo_branch', views.jemo_branch, name='jemo_branch'),
    path('main_branch', views.main_branch, name='main_branch'),

########### Dashboard ##########

    path('dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('search_user/<str:id>', views.search_user, name='search_user'),
   
############customer############
    path('customerReg', views.customerReg, name='customerReg'),    
    path("feedback", views.feedback, name="feedback"),
    # path('delete_drug', views.delete_drug, name='delete_drug'),

#########report##############
    # path('recieve', views.recieve, name='recieve'),
    # path('sendRequest', views.sendRequest, name='sendRequest'),
    # path('viewrequest', views.viewRequest, name='viewRequest'),
    # path('viewresponse', views.viewresponse, name='viewresponse'),
    
    
####### chating ###########
    path('response', views.response, name="response"),
    path("advice/<str:pk>", views.advice, name="advice"),
    path("chat", views.chat, name="chat"),
    path("do_read", views.notification, name="notification"),
    path("chat_delete", views.chat_delete, name="chat_delete"),
   
    #############category##############
    path("ent", views.ENT, name="ENT"),
    path("cns", views.CNS, name="CNS"),
    path("git", views.GIT, name="GIT"),
    path("cvs", views.CVS, name="CVS"),
    path("Vitamins", views.Vitamins, name="Vitamins"),
    path("Cosmotic", views.Cosmotics, name="Cosmotics"),
    path("Minerals", views.Minerals, name="Minerals"),
    path("Hormones", views.Hormones, name="Hormones"),
    path("Anti_virals", views.Anti_virus, name="Anti_virus"),
    path("Anti_infectives", views.Anti_infectives, name="Anti_infectives"),
    path("Anti_helmentics", views.Anti_helmentics, name="Anti_helmentics"),
    path("Maskuloskeletal", views.Maskuloskeletal, name="Maskuloskeletal"),
    path("Medical_Supplies", views.Medical_Supplies, name="Medical_Supplies"),
    path("add_druginLebu", views.add_druginLebu, name="add_druginLebu"),
    path("add_druginJemo", views.add_druginJemo, name="add_druginJemo"),
    path("add_druginMainBranch", views.add_druginMainBranch, name="add_druginMainBranch"),
 



 ###########Medicine API##########
    path('medicine-list/', MedicineList.as_view()),
    path('J_medicine-list/', JemoMedicineList.as_view()),
    path('L_medicine-list/', LebuMedicineList.as_view()),
    # path('user-list/', UserList.as_view()),
    # path('user-add/', AddUser.as_view()),




#     path('create/', CreateMedicine.as_view()),
#     path('medicine/<int:pk>', Medicines.as_view()),
#   #####Customer API########
#     path('customer-list/', CustomerList.as_view()),
#     path('create-customer/', CreateCustomer.as_view()),
#     # path('<str:pk>', CustomerChange.as_view()),

#   ######User API#############
 #   path('user/<int:pk>', UserChange.as_view()),

    path('create_user/', UserCreateView.as_view(), name='create_user'),

]



 
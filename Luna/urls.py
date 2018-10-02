from django.conf.urls import url
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from . import views

calculator_patterns = [
    url(r'^system_performance_calculator/$', views.system_performance_calculator),
    url(r'^system_performance_calculator/pdf$', views.performance_calculator_print, name='System Performance'),
    url(r'^soft_savings_analysis/$', views.soft_savings_calculator),
    url(r'^soft_savings_analysis/pdf$', views.soft_savings_print, name='Soft Savings Analysis'),
    # url(r'^full_benefit_analysis/$', views.full_benefit_calculator),
    # url(r'^full_benefit_analysis/pdf$', views.full_benefit_print, name='Full Benefit Analysis'),
    url(r'^RTS_notes/$', views.RTS_notes),
    url(r'^Customer_Solutions/$', views.customer_solutions),
<<<<<<< Updated upstream
<<<<<<< HEAD
    url(r'^Customer_Solutions/buyout/pdf$', views.customer_solutions_buyout, name='Customer Solutions buyout'),
    url(r'^Customer_Solutions/prepayment/pdf$', views.customer_solutions_prepayment, name='Customer Solutions prepayment'),
=======
    url(r'^Customer_Solutions/buyout/pdf$', views.buyout_print, name='Customer Solutions buyout'),
    url(r'^Customer_Solutions/prepayment/pdf$', views.prepayment_print, name='Customer Solutions prepayment'),
>>>>>>> Buyout_PrepayCalc
=======
    url(r'^Customer_Solutions/buyout/pdf$', views.customer_solutions_buyout, name='Customer Solutions buyout'),
    url(r'^Customer_Solutions/prepayment/pdf$', views.customer_solutions_prepayment, name='Customer Solutions prepayment'),
>>>>>>> Stashed changes
]

automation_patterns =[
    url(r'^$', views.automation_page),
    url(r'^create_new_task/$', views.create_new_task)
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^career_path/$', views.career_path, name='career_path'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('calculators/', include(calculator_patterns)),
    path('automation/', include(automation_patterns)),
]

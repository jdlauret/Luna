from django.conf.urls import url
# from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^global$', views.index, name="global"),
    url(r'^agent$', views.agent, name="agent_view"),
    url(r'^transaction', views.transactions, name="transaction_view"),
    url(r'^submit_transaction', views.submit_transaction, name="submit_transaction"),
    url(r'^overlord_view$', views.overlord_view, name="overlord"),
    url(r'^overlord_view/control_panel$', views.control_panel, name="control"),
    url(r'^overlord_view/employee_load', views.employee_load, name="employee_load"),
    url(r'^overlord_view/trans_load', views.trans_load, name="trans_load"),
    url(r'^overlord_view/overlord_create_trans', views.overlord_create_trans, name="create_trans"),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^global$', views.index, name="global"),
    url(r'^agent$', views.agent, name="agent_view"),
    url(r'^transaction', views.transactions, name="transaction_view"),
    url(r'^submit_transaction', views.submit_transaction, name="submit_transaction"),
    url(r'^overlord_view$', views.overlord_view, name="overlord_view"),
]

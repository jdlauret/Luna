from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^global$', views.index, name="global"),
    url(r'^agent$', views.agent, name="agent_view"),
    # url(r'^accept_coin', views.accept_coin),
    url(r'^transaction', views.transactions, name="transaction_view"),
    url(r'^submit_transaction', views.submit_transaction, name="submit_transaction"),
    url(r'^overlord_view$', views.overlord_view, name="overlord_view"),
]

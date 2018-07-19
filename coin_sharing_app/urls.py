from django.conf.urls import url
from . import views

urlpatterns = [
#   Global View of all the transactions
    url(r'^global$', views.index, name="global"),
#   URL to Agent's personal transaction view
    # url(r'^(?P<badge_id>\d+)$', views.pers_trans_view)
    url(r'^agent$', views.agent, name="agent_view"),
#   URL to page where you can send coins to other people
#     url(r'^(?P<badge_id>\d+)/trans$', views.transaction)
    url(r'^transaction', views.transaction, name="transaction_view"),
    url(r'^submit_transaction', views.submit_transaction, name="submit_transaction"),
]
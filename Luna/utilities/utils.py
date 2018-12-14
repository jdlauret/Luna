from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from operator import itemgetter


def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)


def latest_active_users():
    current_users = get_current_users()
    login_data = [
        [x.first_name, x.last_login.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%m-%d-%Y %H:%M:%S')]
        for x in current_users]
    return list(reversed(sorted(login_data, key=itemgetter(1))))

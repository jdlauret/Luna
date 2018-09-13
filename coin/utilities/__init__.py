from Luna.models import DataWarehouse

def find_badge_id(email):
    dw = DataWarehouse('admin')
    dw.query_results('''SELECT BADGE_ID
                            FROM WORKDAY.V_WORKDAY_CURRENT_V2
                            WHERE lower(WORK_EMAIL_ADDRESS) = LOWER(:email)''',
                     bindvars={'email': email})
    return dw.results[0][0]
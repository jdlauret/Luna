from models import SnowflakeConsole, SnowFlakeDW

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')


def find_badge_id(email):
    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)

        DW.execute_query('''
        SELECT BADGE_ID
        FROM VSLR.HR.T_EMPLOYEE
        WHERE LOWER(WORK_EMAIL_ADDRESS) = LOWER(%s)''', bindvars=[email])
        results = DW.query_results[0][0]
    finally:
        DB.close_connection()

    return results
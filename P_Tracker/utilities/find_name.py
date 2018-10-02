from models import SnowflakeConsole, SnowFlakeDW

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def find_name(badge):
    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)

        DW.execute_query('''SELECT FULL_NAME
                                FROM VSLR.HR.T_EMPLOYEE
                                WHERE BADGE_ID = %s''',
                         bindvars=[badge])
        results = DW.query_results[0][0]
    finally:
        DB.close_connection()

    return results
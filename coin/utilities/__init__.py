from BI.data_warehouse.connector import Snowflake

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')


def find_badge_id(email):
    try:
        DB.open_connection()

        DB.execute_query('''SELECT BADGE_ID
                                FROM VSLR.HR.T_EMPLOYEE
                                WHERE LOWER(WORK_EMAIL_ADDRESS) = LOWER(%s)
                                AND NOT TERMINATED''',
                         bindvars=[email])
        results = DB.query_results[0][0]
    finally:
        DB.close_connection()

    return results
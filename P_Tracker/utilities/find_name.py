from BI.data_warehouse.connector import Snowflake


def find_name(badge):
    db = Snowflake()
    db.set_user('MACK_DAMAVANDI')
    try:
        db.open_connection()

        db.execute_query('''SELECT FULL_NAME
                            FROM VSLR.HR.T_EMPLOYEE
                            WHERE BADGE_ID = %s''',
                         bindvars=[badge])
        results = db.query_results[0][0]
    finally:
        db.close_connection()

    return results

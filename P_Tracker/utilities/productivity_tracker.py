# import os
# from datetime import date, timedelta
# from models import SnowFlakeDW, SnowflakeConsole
#
# main_dir = os.getcwd()
# tracker_dir = os.path.join(main_dir, 'P_Tracker')
# utilities_dir = os.path.join(tracker_dir, 'utilities')
#
# DB = SnowFlakeDW()
# DB.set_user('MACK_DAMAVANDI')
#
# def tracker_list(badge):
#     notes = {}
#     try:
#         DB.open_connection()
#         DW = SnowflakeConsole(DB)
#         with open(os.path.join(utilities_dir, 'productivity_tracker.sql'), 'r') as file:
#             sql = file.read()
#
#         DW.execute_query(sql[0].format(service_number=str(badge)))
#         information = DW.query_results[0]
#         print(information)
#
#     except Exception as e:
#         notes['error'] = e
#         return notes
#
#     finally:
#         DB.close_connection()
#
#     return notes
import os
from models import SnowflakeConsole, SnowFlakeDW

main_dir = os.getcwd()
tracker_dir = os.path.join(main_dir, 'P_Tracker')
utilities_dir = os.path.join(tracker_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def tracker_list(badge):
	auth_list = {}

	try:
		DB.open_connection()
		DW = SnowflakeConsole(DB)
		with open(os.path.join(utilities_dir, 'productivity_tracker.sql'), 'r') as file:
			sql = file.read()
		DW.execute_query(sql.format(badge=str(badge)))
		results = DW.query_results
		column = DW.query_columns
		print(column)
		print(results)

		if len(results) == 0:
			auth_list['error'] = 'Invalid Badge ID'
			return auth_list

	except Exception as e:
		auth_list['error'] = e
		return auth_list

	finally:
		DB.close_connection()
	auth_list['badge'] = results[0][0]
	auth_list['name'] = results[0][1]
	auth_list['supervisor'] = results[0][2]
	auth_list['min_worked'] = results[0][3]
	auth_list['breaks'] = results[0][4]
	auth_list['activity'] = results[0][5]
	auth_list['training'] = results[0][6]
	auth_list['meeting'] = results[0][7] + results[0][8]
	auth_list['project'] = results[0][9]

	return auth_list


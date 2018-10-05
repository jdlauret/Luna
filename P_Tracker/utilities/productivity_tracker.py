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

		if len(results) == 0:
			auth_list['error'] = 'Invalid Badge ID'
			return auth_list

	except Exception as e:
		auth_list['error'] = e
		return auth_list

	finally:
		DB.close_connection()

	auth_list['test'] = results.pop(0)
	print('test', auth_list['test'])

	return auth_list


import os
from datetime import date, timedelta
from Luna.models import DataWarehouse
from models import SnowFlakeDW, SnowflakeConsole

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def notes_wizard (servicenum):
    install_notes = {
        'account_info': {},
        'arrays': {},
        'spec_info': {},
        'roof_sections': {},
        'form_response_complete': False
    }

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-', '')

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
        with open(os.path.join(utilities_dir, 'RTS_notes_wizard.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')
        DW.execute_query(sql[0].format(service_number=str(servicenum)))
        account_information = DW.query_results[0]
        install_notes['account_info'] = account_information
        if install_notes['account_info'][7] == None:
            pass
        else:
            install_notes['account_info'][7] = install_notes['account_info'][7].strftime('%B %#d, %Y')

        # error message if service number is not valid
        if len(account_information) == 0:
            install_notes['error'] = '{} is not a valid service number.'.format(servicenum)
            return install_notes

    except Exception as e:
        install_notes['error'] = e
        return install_notes

    try:
        # Execute second query results
        DW.execute_query(sql[1].format(service_number=str(servicenum)))
        # Second query results
        roof_section_columns = DW.query_columns
        roof_section_info = DW.query_results[0]

        # error message when no installation notes are pulled up
        if len(roof_section_info) == 0:
            install_notes['error'] = 'There was no Installation Notes and ' \
                               'Information found for Service Number {}'.format(servicenum)
            return install_notes

    except Exception as e:
        install_notes['error'] = e
        return install_notes

    finally:
        DB.close_connection()

    # Total Solar Roof Integer
    tsr = 0

    # install notes combine both account information and column information into one list
    # combines roof_section info and column name together
    for j, value in enumerate(roof_section_info):
        install_notes['spec_info'][roof_section_columns[j]] = value

    # pulls the total solar roof information and turns the string into a integer
    tsr = roof_section_info[roof_section_columns.index('TOTAL_SOLAR_ROOFS')]

    t1 = roof_section_info[roof_section_columns.index('NUM_MODULES_DESIGNED')].split(',')
    t2 = roof_section_info[roof_section_columns.index('ROOF_AZIMUTH')].split(',')
    t3 = roof_section_info[roof_section_columns.index('ROOF_TILT')].split(',')

    # for loop for how many roof sections it should create and places the number of modules, azimuth and tilt into each section

    for k in range(int(tsr)):
        new_section = 'Roof Section ' + str(k + 1) + ':'
        install_notes['roof_sections'][new_section] = {
            'Number of Modules': t1[k],
            'Azimuth': t2[k],
            'Tilt': t3[k],
        }

    install_notes['form_response_complete'] = True

    return install_notes

import os
from datetime import date, timedelta
from Luna.models import DataWarehouse

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')


def notes_wizard (servicenum):
    install_notes = {
        'account_info': {},
        'arrays': 0,
        'spec_info': {},
        'roof_sections': {},
        'form_response_complete': False
    }
    dw = DataWarehouse('admin')
    with open(os.path.join(utilities_dir, 'RTS_notes_wizard.sql'),'r') as file:
        sql = file.read()
    sql = sql.split(';')
    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')
    bindvars = {'serviceNum': servicenum}
    try:
        # first query results
        dw.query_results(sql[0], bindvars=bindvars)
        account_information = dw.results[0]
        # error message if service number is not valid
        if len(account_information) == 0:
            install_notes['error'] = '{} is not a valid service number.'.format(servicenum)
            return install_notes
        # first query Column Names
        account_information_columns = dw.column_names

    except Exception as e:
        install_notes['error'] = e
        return install_notes

    try:
        # Execute second query results
        dw.query_results(sql[1], bindvars=bindvars)
        # Second query results
        roof_section_info = dw.results[0]
        # error message when no installation notes are pulled up
        if len(roof_section_info) == 0:
            install_notes['error'] = 'There was no Installation Notes and ' \
                               'Information found for Service Number {}'.format(servicenum)
            return install_notes
        # second query Column Names
        roof_section_columns = dw.column_names

    except Exception as e:
        install_notes['error'] = e
        return install_notes

    # Total Solar Roof Integer
    tsr = 0

    # install notes combine both account information and column information into one list
    # for i, value in enumerate(account_information):
    #     install_notes['account_info'][account_information_columns[i]] = value
    install_notes['account_info'] = account_information
    if install_notes['account_info'][7] == None:
        pass
    else:
        install_notes['account_info'][7] = install_notes['account_info'][7].strftime('%B %#d, %Y')
    # print(type(install_notes['account_info'][7]))
    # print(install_notes['account_info'])
    # combines roof_section info and column name together
    for j, value in enumerate(roof_section_info):
        install_notes['spec_info'][roof_section_columns[j]] = value
    install_notes['spec_column'] = roof_section_columns

    # print('print this section:', install_notes['spec_info'])

    # pulls the total solar roof information and turns the string into a integer
    tsr = int(roof_section_info[roof_section_columns.index('TOTAL_SOLAR_ROOFS')])
    # for loop for how many roof sections it should create and places the number of modules, azimuth and tilt into each section
    for k in range(tsr):
        new_section = 'Roof Section ' + str(k + 1) + ':'
        install_notes['roof_sections'][new_section] = {
            # roof_section_info[roof_section_columns.index('NUM_MODULES_DESIGNED')].split(',')[k],
            # roof_section_info[roof_section_columns.index('ROOF_AZIMUTH_DESIGNED')].split(',')[k],
            # roof_section_info[roof_section_columns.index('ROOF_TILT')].split(',')[k],
            'Number of Modules': roof_section_info[roof_section_columns.index('NUM_MODULES_DESIGNED')].split(',')[k],
            'Azimuth': roof_section_info[roof_section_columns.index('ROOF_AZIMUTH_DESIGNED')].split(',')[k],
            'Tilt': roof_section_info[roof_section_columns.index('ROOF_TILT')].split(',')[k],
        }
    install_notes['form_response_complete'] = True
    # print(install_notes['roof_sections'])

    return install_notes

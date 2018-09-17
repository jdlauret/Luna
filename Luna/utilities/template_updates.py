import os
import json
from django.db.models import Max
from Luna.models import CareerPath
from collections import OrderedDict

JSON_STORAGE_DIR = os.path.join(os.getcwd(), 'Luna\\templates\\json_storage')


def build_career_path():
    departments = [x['department'] for x in CareerPath.objects.order_by().values('department').distinct()]

    new_dict = {}
    most_rows = int(CareerPath.objects.all().aggregate(Max('tier_level'))['tier_level__max'])
    most_cols = int(str(CareerPath.objects.all().aggregate(Max('tier_level'))['tier_level__max'])
                    .split('.')[1]) + 1
    for department in departments:
        department_key = department.replace('_', ' ').title()
        positions = CareerPath.objects.filter(department=department).order_by('tier_level').values()
        functions = list(set([x['function'] for x in positions]))
        max_tier = int(max(x['tier_level'] for x in positions))
        if max_tier > most_rows:
            most_rows = max_tier
        new_dict[department_key] = {}

        for i, function in enumerate(functions):
            function_key = function.replace('_', ' ').title()
            new_dict[department_key][function_key] = {}

            for i in range(most_rows):
                if i == 0:
                    new_dict[department_key][function_key][i + 1] = [{'position': function_key}]
                else:
                    new_dict[department_key][function_key][i + 1] = [{'position': ''}]

        for position in positions:
            column = str(position['tier_level']).split('.')[0]
            row = str(position['tier_level']).split('.')[1]
            function_key = position['function'].replace('_', ' ').title()

            if len(new_dict[department_key][function_key][int(row)]) < int(column):
                for i in range(int(column) - 1):
                    new_dict[department_key][function_key][int(row)].append({'position': ''})
            position_data = {
                'position': position['position'].replace('_', ' ').title(),
                'id': position['id'],
                'position_data': position
            }
            new_dict[department_key][function_key][int(row)].append(position_data)

    for department, value in new_dict.items():
        for function, value2 in value.items():
            for row_num, value3 in value2.items():
                for i in range(most_cols):
                    if len(value3) < most_cols:
                        value3.append({'position': ''})

    rts_key_order = ['Inbound', 'Auxiliary', 'Super Agent', 'Service']
    customer_solutions_order = ['Customer Solutions Admin', 'Customer Solutions', 'Transfer', 'Resolution']
    relations_order = ['Inbound Outbound', 'Email Admin', 'Documents']
    new_dict['Central Scheduling'] = OrderedDict(sorted(new_dict['Central Scheduling'].items(),
                                                          key=lambda j: rts_key_order.index(j[0])))
    new_dict['Customer Solutions'] = OrderedDict(sorted(new_dict['Customer Solutions'].items(),
                                                        key=lambda j: customer_solutions_order.index(j[0])))
    new_dict['Relations'] = OrderedDict(sorted(new_dict['Relations'].items(),
                                               key=lambda j: relations_order.index(j[0])))

    with open(os.path.join(JSON_STORAGE_DIR, 'career_path.json'), 'w') as outfile:
        json.dump(new_dict, outfile, indent=4)


class JsonHandler:

    def __init__(self, json_dir=None):
        if dir is not None:
            self.json_dir = JSON_STORAGE_DIR
        else:
            self.json_dir = json_dir

    def get_json(self, file_name):
        if '.json' not in file_name:
            file_name = file_name + '.json'
        try:
            with open(os.path.join(self.json_dir, file_name)) as infile:
                json_object = json.load(infile)
            return json_object
        except:
            raise

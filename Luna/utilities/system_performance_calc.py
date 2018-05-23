from Luna.models import DataWarehouse

file = open('system_performance_calc.sql','r')
sql = file.read()
file.close()

serviceNum = input("service number: ")
startDate = input("start date: ")
endDate = input("end date: ")

sql = sql.replace('serviceNum', serviceNum)
sql = sql.replace('startDate', startDate)
sql = sql.replace('endDate', endDate)

sql = sql.split(';')

results = {'account': None, 'production': None}

results['account'] = ob.run_query('','',raw_query=sql[0])

print(sql)

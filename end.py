from start import *

page, url, company_name = input_company()

pList = make_pList(url, page)

print_avg(company_name, pList)

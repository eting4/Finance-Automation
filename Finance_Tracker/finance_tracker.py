import csv 
import gspread
import re
import time 

file = "Chase5729_Activity_20231229.CSV"
transactions = []
categories = {
    'subscriptions':['spotify', 'amazon prime', 'apple.com', 'squarespaces',],
    'food':         ['venmo', 'teapioca', 'eats', 'chicken', 'pok pok', 'beijing house', 'bread', 
                     "mcdonald's", '7-eleven', 'braums', "freddy's", 'pho ', 'chipotle', 'little bangkok', 
                     'stella nova', 'starbucks', 'steak', 'raising canes', 'doordash', 'whataburger'],
    'rent & bills': ['discover'],
    'travel':       ['uber   trip', 'oncue'],
    'salary':       ['payroll']
}

def set_month(month, year):
    months = {
        'january': rf"01/[0-3][0-9]/{year}", 
        'february':rf"02/[0-3][0-9]/{year}",
        'march': rf"03/[0-3][0-9]/{year}",
        'april': rf"04/[0-3][0-9]/{year}",
        'may': rf"05/[0-3][0-9]/{year}", 
        'june': rf"06/[0-3][0-9]/{year}",
        'july': rf"07/[0-3][0-9]/{year}",
        'august': rf"08/[0-3][0-9]/{year}",
        'september': rf"09/[0-3][0-9]/{year}",
        'october': rf"10/[0-3][0-9]/{year}",
        'november': rf"11/[0-3][0-9]/{year}", 
        'december': rf"12/[0-3][0-9]/{year}"
    }
    return months.get(month)

# returns category of a given transaction 
def what_category(name, categories): 
    for category, items in categories.items(): 
        for item in items:
            if item.upper() in name.upper(): 
                return category
    return 'other expenses'

# Open csv file 
def file_reader(month, year):
    Sum = 0 
    month = set_month(month, year)
    with open(file, mode='r') as csv_file:  
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader) 
        switch = 0
        temp = 0
        for row in csv_reader:
            if switch < temp: # we've read all the transactions in the month
                break
            try:
                date = row[1] 
                if re.match(month, date):
                    switch += 1
                    temp = switch 
                    name = row[2]
                    amount = float(row[3])
                    Sum += amount
                    transaction = ((date, name, amount, what_category(name, categories)))
                    #print(transaction)
                    #print(round(Sum, 2))
                    transactions.append(transaction)
                elif temp != 0: 
                    switch -= 1
            except StopIteration: 
                break
        return transactions

#print(file_reader('january', 2023))
sa = gspread.service_account()
sh = sa.open("Personal Finances")
wks = sh.worksheet(f"january")
rows = file_reader('january', 2023)

for row in rows: 
    wks.insert_row([row[0], row[1], row[3], row[2]], 8)
    time.sleep(2) #b/c google sheets has limits to how many times you can access the api per second
    


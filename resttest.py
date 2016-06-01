import urllib.request
import json
import re
import math


def url(page_num):
    """
    Return's Api Url with appropriate page number
    :param page_num: page number for url
    """
    return "http://resttest.bench.co/transactions/%s.json" % page_num


def connectAPI():
    """
    Connects to the Api, downloads all transactions and calculates the total balance.
    :return Total Balance and Transaction count both with and without duplicates
    """
    response = None
    transactions = []
    duplicates = []
    totalBalance = 0

    try:
        response = json.loads(urllib.request.urlopen(url(1)).read().decode("utf-8"))
        for t in response['transactions']:
            if t in transactions:
                duplicates.append(t)
            else:
                transactions.append(t)
            totalBalance += float(t['Amount'])

    except Exception as e:
        print("No data available at this page")

    if response is not None:
        totalCount = response['totalCount']

        if len(response['transactions']) < totalCount:
            countPerPage = len(response['transactions'])
            num_pages = math.ceil(totalCount/countPerPage)
        else:
            num_pages = 1

        if num_pages != 1:
            for i in range(2, (num_pages+1)):
                response = json.loads(urllib.request.urlopen(url(i)).read().decode("utf-8"))
                for t in response['transactions']:
                    if t in transactions:
                        duplicates.append(t)
                    else:
                        transactions.append(t)

                    totalBalance += float(t['Amount'])

        f = open('output', 'w')
        f.write("The total number of transactions without accounting for duplicates is %s\n" % totalCount)
        f.write("The total balance without accounting for duplicates is %s \n\n" % totalBalance)

        f.write("The remove_garbage function removes garbage from vendor names. For example: \"%s\" becomes \"%s\".\n\n" %
              (transactions[8]["Company"], remove_garbage([transactions[8]])[0]["Company"]))

        f.write("The total number of duplicates is  %s\n" % len(duplicates))
        f.write("The total number of transactions when accounting for duplicates is %s\n" % (totalCount-len(duplicates)))
        f.write("The total balance when accounting for duplicates is %s \n\n" % (totalBalance - total_balance(duplicates)))

        f.write("The daily_balances function provides a dictionary with all available dates as keys and the "
              "daily balances as values. The daily balances are:\n")
        f.write(json.dumps(daily_balances(transactions), indent=2, sort_keys=True))
        f.write("\n\n")

        f.write("\nThe get_categories function provides a dictionary that lists the expenses as keys and the value holds "
              "an array with the first element being the total expense for that category and the rest of the elements"
              "hold the transactions for that category. The dictionary looks as such: \n")

        f.write(json.dumps(get_categories(transactions), indent=2))
        f.close()

        print("FIN")


def total_balance(transactions):
    """
    Calculates the total balance from a list of transactions.
    If no transactions are passed, return 0
    """
    total = 0
    for t in transactions:
        total += float(t['Amount'])
    return total


def remove_garbage(transactions):
    """
    Removes unnecessary info from vendor names and fixes any double spaces
    :return transactions with fixed vendor names
    """
    garbage = re.compile(r'\w*[#@.\d]\w*|\b(USD)\b|\s+$|')

    for trans in transactions:
        trans['Company'] = garbage.sub('', trans['Company'])
        trans['Company'] = re.sub(' +', ' ', trans['Company']).rstrip()

    return transactions


def get_categories(transactions):
    categories = {}

    for trans in transactions:
        if trans['Ledger'] in categories:
            categories[trans['Ledger']][0] += float(trans['Amount'])
            categories[trans['Ledger']].append(trans)
        else:
            if trans['Ledger'] != "":
                categories[trans['Ledger']] = []
                categories[trans['Ledger']].append(float(trans['Amount']))
                categories[trans['Ledger']].append(trans)

    return categories

def daily_balances(transactions):
    """
    Calculates daily balances for each day and returns a dictionary with the key as date and value as total for that day.
    """
    dates = {}

    for trans in transactions:
        if trans['Date'] in dates:
            dates[trans['Date']] += float(trans['Amount'])
        else:
            dates[trans['Date']] = float(trans['Amount'])

    return dates

if __name__ == '__main__':
    connectAPI()

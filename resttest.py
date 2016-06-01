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
        for t in response["transactions"]:
            if t in transactions:
                duplicates.append(t)
            else:
                transactions.append(t)
            totalBalance += float(t["Amount"])

    except Exception as e:
        print("No data available at this page")

    if response is not None:
        totalCount = response["totalCount"]

        if len(response["transactions"]) < totalCount:
            countPerPage = len(response["transactions"])
            num_pages = math.ceil(totalCount/countPerPage)
        else:
            num_pages = 1

        if num_pages != 1:
            for i in range(2, (num_pages+1)):
                response = json.loads(urllib.request.urlopen(url(i)).read().decode("utf-8"))
                for t in response["transactions"]:
                    if t in transactions:
                        duplicates.append(t)
                    else:
                        transactions.append(t)

                    totalBalance += float(t["Amount"])

        print("The total number of transactions without accounting for duplicates is %s" % totalCount)
        print("The total balance without accounting for duplicates is %s \n" % totalBalance)

        print("The remove_garbage function removes garbage from vendor names. For example: \"%s\" becomes \"%s\".\n" %
              (transactions[8]["Company"], remove_garbage([transactions[8]])[0]["Company"]))

        print("The total number of duplicates is  %s" % len(duplicates))
        print("The total number of transactions when accounting for duplicates is %s" % (totalCount-len(duplicates)))
        print("The total balance when accounting for duplicates is %s" % (totalBalance - total_balance(duplicates)))



def total_balance(transactions):
    """
    Calculates the total balance from a list of transactions.
    If no transactions are passed, return 0
    """
    total = 0
    for t in transactions:
        total += float(t["Amount"])
    return total


def remove_garbage(transactions):
    """
    Removes unnecessary info from vendor names and fixes any double spaces
    :return transactions with fixed vendor names
    """
    garbage = re.compile(r'\w*[#@.\d]\w*|\b(USD)\b|\s+$|')

    for trans in transactions:
        trans["Company"] = garbage.sub('', trans["Company"])
        trans["Company"] = re.sub(' +', ' ', trans["Company"]).rstrip()

    return transactions


connectAPI()
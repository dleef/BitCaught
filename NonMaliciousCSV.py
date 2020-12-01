import csv
import requests
from random import randrange

address_reportcount = {}
address_abusetype = {}
all_malicious = {}

filtered_nonmalicious_addresses = []
already_recorded = []
temp_already_recorded_index = []

def most_frequent(List): 
    return max(set(List), key = List.count) 

with open("Malicious_Records.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        key = lines[1]
        abuse_type = lines[2]
        print(key, abuse_type)
        if key in address_reportcount:
            origcount = address_reportcount[key]
            origcount += 1
            address_reportcount[key] = origcount
            origtypes = address_abusetype[key]
            origtypes.append(abuse_type)
            address_abusetype[key] = origtypes
        else:
            address_reportcount[key] = 1
            newlist = []
            newlist.append(abuse_type)
            address_abusetype[key] = newlist
    validcount = 0
    for k in address_reportcount:
        all_malicious[k] = [address_reportcount[k], most_frequent(address_abusetype[k])]

with open("NonMalicious_Records.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        if address not in all_malicious:
            filtered_nonmalicious_addresses.append(address)


with open("Filtered_NonMalicious_Records_Detailed.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        already_recorded.append(address)


with open("Filtered_NonMalicious_Records_Detailed.csv", "a") as csvfile:
    fieldnames = ["wallet_address", "malicious", "bitcoin_spent", "bitcoin_received", "total_balance", "total_transactions"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer.writeheader()
    count = 5935
    break_loop = False
    while(count < 8000):
        if break_loop:
            break
        malicious = False
        rand = randrange(1048568)
        if rand not in temp_already_recorded_index:
            temp_already_recorded_index.append(rand)
            add = filtered_nonmalicious_addresses[rand]
            if add not in all_malicious and add not in already_recorded:
                response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=0ede61cea6d44b24ac7a2392335ea1d6")
                if (response.status_code == 200):
                    result = response.json()
                    bitcoin_received = result['total_received']
                    bitcoin_sent = result['total_sent']
                    total_balance = result['balance']
                    total_transactions = result['n_tx']
                    writer.writerow({'wallet_address' : add, 'malicious' : malicious, 'bitcoin_spent' : bitcoin_sent, 'bitcoin_received' : bitcoin_received, 'total_balance' : total_balance, 'total_transactions' : total_transactions})
                    count += 1
                elif(response.status_code == 429):
                    print(response)
                    print(response.json())
                    print(response.status_code)
                    print("ended with this count: " + str(count))
                    break_loop = True
                    break

                print(count/8000)

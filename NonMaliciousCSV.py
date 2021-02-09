import csv
import requests
from random import randrange
import random

all_malicious = {}

filtered_nonmalicious_addresses = []
already_recorded = {}
temp_already_recorded_index = {}

with open("data_filtered/Filtered_Malicious_Records_Detailed_BitcoinAbuse.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        key = lines[0]
        if key not in all_malicious:
            all_malicious[key] = 1

with open("data_filtered/Filtered_Malicious_Records_BitcoinHeist.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        key = lines[0]
        if key not in all_malicious:
            all_malicious[key] = 1


with open("data_unfiltered/NonMalicious_Records.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    count = 0
    for lines in csvFile:
        print(count)
        if count > 0:
            address = lines[0]
            if address not in all_malicious and address not in filtered_nonmalicious_addresses:
                filtered_nonmalicious_addresses.append(address)
            if (len(filtered_nonmalicious_addresses) == 40000):
                break
        count += 1

with open("data_filtered/Filtered_NonMalicious_Records_Detailed.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        already_recorded[address] = 1


with open("data_filtered/Filtered_NonMalicious_Records_Detailed.csv", "a") as csvfile, \
    open("data_unfiltered/NonMalicious_Records.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    fieldnames = ["wallet_address", "malicious", "bitcoin_spent", "bitcoin_received", "total_balance", "total_transactions"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer.writeheader()
    count = 7335
    break_loop = False
    while(count < 10000):
        if break_loop:
            break
        malicious = False
        rand = randrange(40000)
        add = filtered_nonmalicious_addresses[rand]
        if (add not in temp_already_recorded_index):
            temp_already_recorded_index[add] = 1
            if add not in all_malicious and add not in already_recorded:
                response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=207c72ae6ebb43d69521234f3a17de13")
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

                print(count/10000)

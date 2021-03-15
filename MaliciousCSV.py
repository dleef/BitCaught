import csv
import requests

address_reportcount = {}
address_abusetype = {}
filtered_addresses = {}

def most_frequent(List): 
    return max(set(List), key = List.count) 

# Cleaning and noisiness management
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
        if (address_reportcount[k] > 5):
            filtered_addresses[k] = [address_reportcount[k], most_frequent(address_abusetype[k])]

# Fetch data from blockchain, calculate basic features, and store in file
with open("Filtered_Malicious_Records_Detailed.csv", "a") as csvfile:
    fieldnames = ["wallet_address", "malicious", "malicious_type", "bitcoin_spent", "bitcoin_received", "total_balance", "total_transactions"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer.writeheader()
    total = len(filtered_addresses.keys())
    count = 0
    start_recording = False
    for add in filtered_addresses:
        if (start_recording):
            malicious = True
            malicious_type = filtered_addresses[add][1]
            response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=362634d27a3c4750ab98e5e8bbb92ffa")
            if (response.status_code == 200):
                result = response.json()
                bitcoin_received = result['total_received']
                bitcoin_sent = result['total_sent']
                total_balance = result['balance']
                total_transactions = result['n_tx']
                writer.writerow({'wallet_address' : add, 'malicious' : malicious, 'malicious_type' : malicious_type, 'bitcoin_spent' : bitcoin_sent, 'bitcoin_received' : bitcoin_received, 'total_balance' : total_balance, 'total_transactions' : total_transactions})
                count += 1
            elif(response.status_code == 429):
                print(response)
                print(response.json())
                print(response.status_code)
                print("ended on this address: " + add)
                print("ended with this count: " + str(count))
                break
            print(count/total)
        elif (count == 5255):
            start_recording = True
        else:
            count += 1
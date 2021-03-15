import csv
import requests

malicious_wallets = []
already_recorded = {}
# nonmalicious_wallets = []

with open("data_unfiltered/BitcoinHeistData.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        wallet = lines[0]
        label = lines[9]
        if label != "white" and wallet not in malicious_wallets:
            malicious_wallets.append(wallet)
        print(len(malicious_wallets))
        if (len(malicious_wallets) == 50000):
            break
    print(len(malicious_wallets))

with open("data_filtered/Filtered_Malicious_Records_BitcoinHeist.csv", "r", encoding = "ISO-8859-1") as csvread:
    csvReader = csv.reader(csvread)
    for lines in csvReader:
        address = lines[0]
        already_recorded[address] = 1

# Fetch data from blockchain and store in file
with open("data_filtered/Filtered_Malicious_Records_BitcoinHeist.csv", "a") as csvfile:
    fieldnames = ["wallet_address", "malicious", "bitcoin_spent", "bitcoin_received", "total_balance", "total_transactions"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer.writeheader()
    total = len(malicious_wallets)
    count = 0
    start_recording = False
    tokens = ["0b564c84ec664dcf8f88deccb18682b0", "0ede61cea6d44b24ac7a2392335ea1d6", "ce86fd4dfb414254841743aa6991aab0", "3e107ad6f05741fdab14a596595abcef", "362634d27a3c4750ab98e5e8bbb92ffa", "6295bc12efb7407ba74b49020048d423", "abe2d75cebe840b38f3f321f09751bec", "fad305b171bf4b5392b2e17728ed282e", "2a413571a5e7463b9bca647a67a2ed22", "3107afc4db9c4500ba53b3a4af9338ca", "5160d81762a8473981f253833a177578", "e697c2e69ba94cf98543ecba045127b7", "511bfa9daa3f4d9f9696163aaa007738", "cbe84c1ea08542de86a88655b7d81563", "207c72ae6ebb43d69521234f3a17de13"]
    tokenIndex = 0
    for add in malicious_wallets:
        if (start_recording and add not in already_recorded):
            malicious = False
            response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=" + tokens[tokenIndex])
            if (response.status_code == 200):
                result = response.json()
                bitcoin_received = result['total_received']
                bitcoin_sent = result['total_sent']
                total_balance = result['balance']
                total_transactions = result['n_tx']
                writer.writerow({'wallet_address' : add, 'malicious' : malicious, 'bitcoin_spent' : bitcoin_sent, 'bitcoin_received' : bitcoin_received, 'total_balance' : total_balance, 'total_transactions' : total_transactions})
                count += 1
            elif(response.status_code == 429):
                if tokenIndex < 14:
                    tokenIndex += 1
                else:
                    print(response)
                    print(response.json())
                    print(response.status_code)
                    print("ended on this address: " + add)
                    print("ended with this count: " + str(count))
                    break
            print(count/total)
        elif (count == 1824):
            start_recording = True
        else:
            count += 1
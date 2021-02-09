import csv
import requests

# malicious_wallets = []
nonmalicious_wallets = []
with open("data_unfiltered/BitcoinHeistData.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        wallet = lines[0]
        label = lines[9]
        if label == "white" and wallet not in nonmalicious_wallets:
            nonmalicious_wallets.append(wallet)
        print(len(nonmalicious_wallets))
        if (len(nonmalicious_wallets) == 50000):
            break
    print(len(nonmalicious_wallets))


with open("Filtered_NonMalicious_Records_Detailed.csv", "a") as csvfile:
    fieldnames = ["wallet_address", "malicious", "bitcoin_spent", "bitcoin_received", "total_balance", "total_transactions"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer.writeheader()
    total = len(nonmalicious_wallets)
    count = 0
    start_recording = False
    for add in nonmalicious_wallets:
        if (start_recording):
            malicious = False
            response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=fad305b171bf4b5392b2e17728ed282e")
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
                print("ended on this address: " + add)
                print("ended with this count: " + str(count))
                break
            print(count/total)
        elif (count == 1824):
            start_recording = True
        else:
            count += 1
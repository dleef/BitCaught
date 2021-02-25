import csv
import requests
import math
import sys
import datetime
import dateutil.parser

already_recorded = {}

# look into accounting for the frequency of a given sender / receiver
# --> weigh their information more heavily than others?
with open("data_filtered/Filtered_Malicious_Records_BitcoinHeist_FTX.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        already_recorded[address] = 1


# N_INPUTS, N_OUTPUTS, NUM_SPENT, NUM_RECEIVED, and FRIENDS ARE HANDLED BY BLOCKCHAININFO API

# this is exclusively for fetching f_tx attribute
# next address has 178 senders, 158 receivers, reason for installing token rotating system
with open("data_filtered/Filtered_Malicious_Records_BitcoinHeist_CloseNetwork.csv", mode = "r", encoding = "ISO-8859-1") as readFile, \
    open("data_filtered/Filtered_Malicious_Records_BitcoinHeist_FTX.csv", mode = "a", newline="") as writeFile:
    csv_reader = csv.reader(readFile)
    csv_writer = csv.writer(writeFile)
    tokenIndex = 6
    tokens = ["0b564c84ec664dcf8f88deccb18682b0", "0ede61cea6d44b24ac7a2392335ea1d6", "ce86fd4dfb414254841743aa6991aab0", "3e107ad6f05741fdab14a596595abcef", "362634d27a3c4750ab98e5e8bbb92ffa", "6295bc12efb7407ba74b49020048d423", "abe2d75cebe840b38f3f321f09751bec", "fad305b171bf4b5392b2e17728ed282e", "2a413571a5e7463b9bca647a67a2ed22", "3107afc4db9c4500ba53b3a4af9338ca", "5160d81762a8473981f253833a177578", "e697c2e69ba94cf98543ecba045127b7", "511bfa9daa3f4d9f9696163aaa007738", "cbe84c1ea08542de86a88655b7d81563", "207c72ae6ebb43d69521234f3a17de13"]
    count = 0
    for row in csv_reader:
        if (count > 1800):
            address = row[0]
            earliest_tx_date = datetime.date.today()
            if (address not in already_recorded):
                already_recorded[address] = 1
                response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + address + "?token=" + tokens[tokenIndex])
                result = response.json()
                num_tx = result['n_tx']
                for transaction in result['txrefs']:
                    date = dateutil.parser.parse(transaction['confirmed'])
                    if (date.date() < earliest_tx_date):
                        earliest_tx_date = date.date()
    
                delta = datetime.date.today() - earliest_tx_date
                f_tx = num_tx / delta.days

                row.append(f_tx)
                # row.append(num_tx)
                csv_writer.writerow(row)
                print(count)
        count += 1
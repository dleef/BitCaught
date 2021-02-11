import csv
import requests
import math
import sys
import datetime
import dateutil.parser

already_recorded = {}

# look into accounting for the frequency of a given sender / receiver
# --> weigh their information more heavily than others?
with open("data_filtered/Filtered_NonMalicious_Records_Detailed_Additional.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        already_recorded[address] = 1



# next address has 178 senders, 158 receivers, reason for installing token rotating system
with open("data_filtered/Filtered_NonMalicious_Records_Detailed_CloseNetwork.csv", mode = "r", encoding = "ISO-8859-1") as readFile, \
    open("data_filtered/Filtered_NonMalicious_Records_Detailed_Additional.csv", mode = "a", newline="") as writeFile:
    csv_reader = csv.reader(readFile)
    csv_writer = csv.writer(writeFile)
    tokenIndex = 14
    tokens = ["0b564c84ec664dcf8f88deccb18682b0", "0ede61cea6d44b24ac7a2392335ea1d6", "ce86fd4dfb414254841743aa6991aab0", "3e107ad6f05741fdab14a596595abcef", "362634d27a3c4750ab98e5e8bbb92ffa", "6295bc12efb7407ba74b49020048d423", "abe2d75cebe840b38f3f321f09751bec", "fad305b171bf4b5392b2e17728ed282e", "2a413571a5e7463b9bca647a67a2ed22", "3107afc4db9c4500ba53b3a4af9338ca", "5160d81762a8473981f253833a177578", "e697c2e69ba94cf98543ecba045127b7", "511bfa9daa3f4d9f9696163aaa007738", "cbe84c1ea08542de86a88655b7d81563", "207c72ae6ebb43d69521234f3a17de13"]
    count = 0
    for row in csv_reader:
        if (count > 0):
            address = row[0]
            num_tx = int(row[5])
            earliest_tx_date = datetime.date.today()
            if (address not in already_recorded):
                num_outputs_spent = 0
                num_inputs_spent = 0
                num_received = 0
                num_spent = 0
                already_recorded[address] = 1
                response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + address + "/full?token=" + tokens[tokenIndex])
                result = response.json()
                senders = []
                receivers = []
                friends = 0
                true_num_tx = result['n_tx']
                for transaction in result['txs']:
                    spending = False
                    for tx_input in transaction['inputs']:
                        if 'addresses' in tx_input and tx_input['addresses'] != None and address in tx_input['addresses']:
                            spending = True
                            break
                    if (spending):
                        num_spent += 1
                    else:
                        num_received += 1

                    date = dateutil.parser.parse(transaction['confirmed'])
                    if (date.date() < earliest_tx_date):
                        earliest_tx_date = date.date()
                    
                    for tx_input in transaction['inputs']:
                        # target address is spending
                        if 'addresses' in tx_input and tx_input['addresses'] != None and address in tx_input['addresses']:
                            for INPUT in tx_input['addresses']:
                                if INPUT not in senders and INPUT != address:
                                    senders.append(INPUT)
                                elif INPUT != address:
                                    friends += 1
                                num_inputs_spent += 1
                            for tx_output in transaction['outputs']:
                                if ('addresses' in tx_output and tx_output['addresses'] != None):
                                    for OUTPUT in tx_output['addresses']:
                                        if OUTPUT not in receivers:
                                            receivers.append(OUTPUT)
                                        else:
                                            friends += 1
                                        num_outputs_spent += 1
                        # target address is receiving
                        else:
                            if ('addresses' in tx_input and tx_input['addresses'] != None):
                                for INPUT in tx_input['addresses']:
                                    if INPUT not in senders:
                                        senders.append(INPUT)
                                    else:
                                        friends += 1
                            for tx_output in transaction['outputs']:
                                if ('addresses' in tx_output and tx_output['addresses'] != None):
                                    for OUTPUT in tx_output['addresses']:
                                        if OUTPUT not in receivers and OUTPUT != address:
                                            receivers.append(OUTPUT)
                                        elif OUTPUT != address:
                                            friends += 1
                print(address)
                print("spent: " + str(num_spent))
                print("received " + str(num_received))
                print(num_spent + num_received == num_tx)
                matching = 0
                if (num_spent + num_received == num_tx):
                    matching = 1
                print(num_tx)
                avg_num_inputs_spent = num_inputs_spent / num_tx
                avg_num_outputs_spent = num_outputs_spent / num_tx
                print("N inputs: " + str(avg_num_inputs_spent))
                print("N outputs: " + str(avg_num_outputs_spent))
                delta = datetime.date.today() - earliest_tx_date
                f_tx = num_tx / delta.days
                print("transaction frequency: " + str(f_tx))
                print("friends: " + str(friends))

                row.append(true_num_tx)
                row.append(num_spent)
                row.append(num_received)
                row.append(avg_num_inputs_spent)
                row.append(avg_num_outputs_spent)
                row.append(f_tx)
                row.append(friends)
                row.append(matching)

                csv_writer.writerow(row)
                print(count)
        count += 1
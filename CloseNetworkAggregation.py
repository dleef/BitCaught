import csv
import requests
import math
import sys

already_recorded = {}

with open("data_filtered/Filtered_NonMalicious_Records_Detailed_CloseNetwork.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        already_recorded[address] = 1

# Fetch data from blockchain, calculated close network features, and store in file
with open("data_filtered/Filtered_NonMalicious_Records_Detailed.csv", mode = "r", encoding = "ISO-8859-1") as readFile, \
    open("data_filtered/Filtered_NonMalicious_Records_Detailed_CloseNetwork.csv", mode = "a", newline="") as writeFile:
    csv_reader = csv.reader(readFile)
    csv_writer = csv.writer(writeFile)
    tokenIndex = 2
    tokens = ["15 tokens go here"]
    count = 0
    for row in csv_reader:
        if (count > 10000):
            address = row[0]
            if (address not in already_recorded):
                already_recorded[address] = 1
                response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + address + "/full?token=" + tokens[tokenIndex])
                result = response.json()
                CN_senders = []
                CN_receivers = []
                for transaction in result['txs']:
                    for tx_input in transaction['inputs']:
                        # the people who are sending
                        if 'addresses' in tx_input and tx_input['addresses'] != None and address not in tx_input['addresses']:
                            for sender in tx_input['addresses']:
                                if sender not in CN_senders:
                                    CN_senders.append(sender)
                        # person is sending, need people receiving
                        else:
                            for tx_output in transaction['outputs']:
                                if ('addresses' in tx_output and tx_output['addresses'] != None):
                                    for receiver in tx_output['addresses']:
                                        if receiver not in CN_receivers:
                                            CN_receivers.append(receiver)
                print(len(CN_receivers))
                print(len(CN_senders))
                # calculating CN_sender info
                CN_sender_bitcoin_received_avg = 0
                CN_sender_bitcoin_sent_avg = 0
                CN_sender_total_balance_avg = 0
                CN_sender_total_transactions_avg = 0
                CN_sender_received = []
                CN_sender_sent = []
                CN_sender_transactions = []
                for add in CN_senders:
                    response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=" + tokens[tokenIndex])
                    if (response.status_code == 200):
                        result = response.json()
                        CN_sender_bitcoin_received_avg += int(result['total_received'])
                        CN_sender_bitcoin_sent_avg += int(result['total_sent'])
                        CN_sender_total_balance_avg += int(result['balance'])
                        CN_sender_total_transactions_avg += int(result['n_tx'])
                        CN_sender_received.append(int(result['total_received']))
                        CN_sender_sent.append(int(result['total_sent']))
                        CN_sender_transactions.append(int(result['n_tx']))
                    elif(response.status_code == 429):
                        if (tokenIndex == 14):
                            print(response)
                            print(response.json())
                            print(response.status_code)
                            print("senders")
                            print("ended on this address: " + add)
                            print("ended with this count: " + str(count))
                            sys.exit()
                        else:
                            tokenIndex += 1
                            new_res = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=" + tokens[tokenIndex])
                            if (new_res.status_code == 200):
                                result = new_res.json()
                                CN_sender_bitcoin_received_avg += int(result['total_received'])
                                CN_sender_bitcoin_sent_avg += int(result['total_sent'])
                                CN_sender_total_balance_avg += int(result['balance'])
                                CN_sender_total_transactions_avg += int(result['n_tx'])
                                CN_sender_received.append(int(result['total_received']))
                                CN_sender_sent.append(int(result['total_sent']))
                                CN_sender_transactions.append(int(result['n_tx']))
                            elif(response.status_code == 429):
                                print(response)
                                print(response.json())
                                print(response.status_code)
                                print("senders")
                                print("ended on this address: " + add)
                                print("ended with this count: " + str(count))
                                sys.exit()

                n_senders = len(CN_senders)

                # avoid divide by 0
                if (n_senders == 0):
                    n_senders = 1

                # get the averages
                CN_sender_bitcoin_received_avg /= n_senders
                CN_sender_bitcoin_sent_avg /= n_senders
                CN_sender_total_balance_avg /= n_senders
                CN_sender_total_transactions_avg /= n_senders

                s_received_sum = 0
                s_sent_sum = 0
                s_tx_sum = 0
                # get the standard deviations
                for s_r in CN_sender_received:
                    diff = s_r - CN_sender_bitcoin_received_avg
                    squared_diff = math.pow(diff, 2)
                    s_received_sum += squared_diff
                
                for s_s in CN_sender_sent:
                    diff = s_s - CN_sender_bitcoin_sent_avg
                    squared_diff = math.pow(diff, 2)
                    s_sent_sum += squared_diff
                
                for s_t in CN_sender_transactions:
                    diff = s_t - CN_sender_total_transactions_avg
                    squared_diff = math.pow(diff, 2)
                    s_tx_sum += squared_diff

                s_received_sum /= n_senders
                s_sent_sum /= n_senders
                s_tx_sum /= n_senders
                CN_sender_bitcoin_received_sd = math.sqrt(s_received_sum)
                CN_sender_bitcoin_sent_sd = math.sqrt(s_sent_sum)
                CN_sender_total_transactions_sd = math.sqrt(s_tx_sum)

                # calculating CN_receiver info
                CN_receiver_bitcoin_received_avg = 0
                CN_receiver_bitcoin_sent_avg = 0
                CN_receiver_total_balance_avg = 0
                CN_receiver_total_transactions_avg = 0
                CN_receiver_received = []
                CN_receiver_sent = []
                CN_receiver_transactions = []
                for add in CN_receivers:
                    response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=" + tokens[tokenIndex])
                    if (response.status_code == 200):
                        result = response.json()
                        CN_receiver_bitcoin_received_avg += int(result['total_received'])
                        CN_receiver_bitcoin_sent_avg += int(result['total_sent'])
                        CN_receiver_total_balance_avg += int(result['balance'])
                        CN_receiver_total_transactions_avg += int(result['n_tx'])
                        CN_receiver_received.append(int(result['total_received']))
                        CN_receiver_sent.append(int(result['total_sent']))
                        CN_receiver_transactions.append(int(result['n_tx']))
                    elif(response.status_code == 429):
                        if (tokenIndex == 14):
                            print(response)
                            print(response.json())
                            print(response.status_code)
                            print("receivers")
                            print("ended on this address: " + add)
                            print("ended with this count: " + str(count))
                            sys.exit()
                        else:
                            tokenIndex += 1
                            new_res = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + add + "?token=" + tokens[tokenIndex])
                            if (new_res.status_code == 200):
                                result = new_res.json()
                                CN_receiver_bitcoin_received_avg += int(result['total_received'])
                                CN_receiver_bitcoin_sent_avg += int(result['total_sent'])
                                CN_receiver_total_balance_avg += int(result['balance'])
                                CN_receiver_total_transactions_avg += int(result['n_tx'])
                                CN_receiver_received.append(int(result['total_received']))
                                CN_receiver_sent.append(int(result['total_sent']))
                                CN_receiver_transactions.append(int(result['n_tx']))
                            elif(response.status_code == 429):
                                print(response)
                                print(response.json())
                                print(response.status_code)
                                print("receivers")
                                print("ended on this address: " + add)
                                print("ended with this count: " + str(count))
                                sys.exit()

                n_receivers = len(CN_receivers)

                # avoid divide by 0
                if (n_receivers == 0):
                    n_receivers = 1

                # get the averages
                CN_receiver_bitcoin_received_avg /= n_receivers
                CN_receiver_bitcoin_sent_avg /= n_receivers
                CN_receiver_total_balance_avg /= n_receivers
                CN_receiver_total_transactions_avg /= n_receivers

                r_received_sum = 0
                r_sent_sum = 0
                r_tx_sum = 0
                # get the standard deviations
                for r_r in CN_receiver_received:
                    diff = r_r - CN_receiver_bitcoin_received_avg
                    squared_diff = math.pow(diff, 2)
                    r_received_sum += squared_diff
                
                for r_s in CN_receiver_sent:
                    diff = r_s - CN_receiver_bitcoin_sent_avg
                    squared_diff = math.pow(diff, 2)
                    r_sent_sum += squared_diff
                
                for r_t in CN_receiver_transactions:
                    diff = r_t - CN_receiver_total_transactions_avg
                    squared_diff = math.pow(diff, 2)
                    r_tx_sum += squared_diff

                r_received_sum /= n_receivers
                r_sent_sum /= n_receivers
                r_tx_sum /= n_receivers
                CN_receiver_bitcoin_received_sd = math.sqrt(r_received_sum)
                CN_receiver_bitcoin_sent_sd = math.sqrt(r_sent_sum)
                CN_receiver_total_transactions_sd = math.sqrt(r_tx_sum)

                row.append(CN_sender_bitcoin_sent_avg)
                row.append(CN_sender_bitcoin_sent_sd)
                row.append(CN_sender_bitcoin_received_avg)
                row.append(CN_sender_bitcoin_received_sd)
                row.append(CN_sender_total_transactions_avg)
                row.append(CN_sender_total_transactions_sd)
                row.append(CN_sender_total_balance_avg)

                row.append(CN_receiver_bitcoin_sent_avg)
                row.append(CN_receiver_bitcoin_sent_sd)
                row.append(CN_receiver_bitcoin_received_avg)
                row.append(CN_receiver_bitcoin_received_sd)
                row.append(CN_receiver_total_transactions_avg)
                row.append(CN_receiver_total_transactions_sd)
                row.append(CN_receiver_total_balance_avg)

                csv_writer.writerow(row)
                print("receivers: ")
                print(CN_receivers)
                print("senders: ")
                print(CN_senders)
        count += 1
import csv
import requests
import math
import sys
import datetime
import dateutil.parser
import time

already_recorded = {}

with open("data_filtered/Filtered_NonMalicious_Records_Detailed_Accurate.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        already_recorded[address] = 1

# Fetch data from blockchain and calculate additional features, incorrect calculations so the resulting data isn't stored in file
with open("data_filtered/Filtered_NonMalicious_Records_Detailed_FTX.csv", mode = "r", encoding = "ISO-8859-1") as readFile, \
    open("data_filtered/Filtered_NonMalicious_Records_Detailed_Accurate.csv", mode = "w", newline="") as writeFile:
    csv_reader = csv.reader(readFile)
    csv_writer = csv.writer(writeFile)
    tokenIndex = 0
    count = 0
    for row in csv_reader:
        if (count > 0):
            address = row[0]
            num_tx = int(row[5])
            if (address not in already_recorded):
                time.sleep(5)
                num_outputs_spent = 0
                num_inputs_spent = 0
                temp_inputs_spent = 0
                temp_outputs_spent = 0
                num_received = 0
                num_spent = 0
                already_recorded[address] = 1
                print(address)
                response = requests.get("https://blockchain.info/rawaddr/" + address)
                result = response.json()
                alt_addresses = {}
                friends = 0
                for transaction in result['txs']:
                    spending = False
                    for tx_input in transaction['inputs']:
                        if 'prev_out' in tx_input:
                            prev_out = tx_input['prev_out']
                            if 'addr' in prev_out:
                                add = prev_out['addr']
                                if add in alt_addresses:
                                    friends += 1
                                if add == address:
                                    spending = True
                                    num_spent += 1
                                else:
                                    alt_addresses[add] = 1
                                temp_inputs_spent += 1
                    for tx_output in transaction['out']:
                        if 'addr' in tx_output:
                            add = tx_output['addr']
                            if add in alt_addresses:
                                friends += 1
                            if add == address:
                                spending = False
                                num_received += 1
                            else:
                                alt_addresses[add] = 1
                            temp_outputs_spent += 1

                    if (spending):
                        num_outputs_spent += temp_outputs_spent
                        num_inputs_spent += temp_inputs_spent
                        temp_inputs_spent = 0
                        temp_outputs_spent = 0

                if (num_spent == 0):
                    avg_num_inputs_spent = 0
                    avg_num_outputs_spent = 0
                else:
                    avg_num_inputs_spent = num_inputs_spent / num_spent
                    avg_num_outputs_spent = num_outputs_spent / num_spent
                print("N inputs: " + str(avg_num_inputs_spent))
                print("N outputs: " + str(avg_num_outputs_spent))
                print("friends: " + str(friends))
                print("num spent: " + str(num_spent) + ", num received: " + str(num_received))
                print(num_spent + num_received == num_tx)
                print(num_tx)
                # row.append(num_spent)
                # row.append(num_received)
                row.append(avg_num_inputs_spent)
                row.append(avg_num_outputs_spent)
                row.append(friends)

                csv_writer.writerow(row)
                print(count)
        count += 1
import csv
import requests
import math
import sys
import datetime
import dateutil.parser

already_recorded = {}

with open("data_filtered/Filtered_Malicious_Records_BitcoinHeist_FTX.csv", mode = "r", encoding = "ISO-8859-1") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        address = lines[0]
        already_recorded[address] = 1


# Fetch data from blockchain, calculate transaction frequency feature, and store in file
with open("data_filtered/Filtered_Malicious_Records_BitcoinHeist_CloseNetwork.csv", mode = "r", encoding = "ISO-8859-1") as readFile, \
    open("data_filtered/Filtered_Malicious_Records_BitcoinHeist_FTX.csv", mode = "a", newline="") as writeFile:
    csv_reader = csv.reader(readFile)
    csv_writer = csv.writer(writeFile)
    tokenIndex = 6
    tokens = ["15 API keys go here"]
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
                csv_writer.writerow(row)
                print(count)
        count += 1
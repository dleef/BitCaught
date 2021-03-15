# BitCaught
Research for Center for Cybersecurity and Privacy as well as a class project for CIS 433: Computer and Network Security


## Data
The raw data sources are stored in the data_unfiltered folder while filtered and feature appended datasets are stored in data_filtered. All files in the parent directory (i.e. basic_large_v1.csv) are prepared and ready to be trained and tested on by the supervised learning models.

## Collection
All of the files corresponding to data collection are in the parent directory and include all of the python files except for MaliciousModel.py and MaliciousModelDeep.py. API keys have been deleted from the files for obvious reasons.

## Usage
To execute a ten-fold cross validation process on the simple neural network, simply type "python3 MaliciousModel.py" into your terminal (or "python3 MaliciousModelDeep.py" for the deep neural network). This will begin training and validating the model on 19-dimensional BitcoinHeist data.


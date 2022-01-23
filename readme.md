# Trend Channel Analysis in Crytpo Currencies

This code helps to extract the data from the gate api and creates possible channel formation in the price index to help in better analysis

## Contents

The given folder contains 
1. run.sh : bash script to run the file
2. Main.py : Main file
3. Utility.py : File containing the methods to find trends and channel
4. TradingData.py : File to get data from gate api
5. Plotter.py : File to plot the graph and save it
6. Plots : where the image file generated of channel analysis is stored

## How to run 

First install the requirements with command. 

```bash 
pip install -r requirements.txt
```

After installing all the requirements, the files could be run directly by bash script but first run.

```bash 
chmod 755 run.sh
```

So that files could run

Then just enter the command. 

```bash 
./run.sh <input_file>
```

#### Input Format

Line 1 contains case number (t)

Line 2 contains n the width of channel

Subsequent t lines contains the input in format

{Coin_Name} {Interval} {Start_date} {End_date}

Interval : among 1h, 4h, 1d, 1w

Date format : mm/dd/yyyy

For more information of the problem statement please view Channel_Assignment.pdf

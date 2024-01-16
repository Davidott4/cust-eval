# cust-eval
A simple package for calculating CLV.

Reads a given .CSV file that contains the columns 'CustomerID', 'Timestamp' and 'PurchaseValue'.
When 'count' is specified, it will write an output .csv file with the top customers by predicted number of products purchased.
When 'spend' is specified, it will write an output .csv file with the top customers by predicted total monetary purchases.

## Installation
#### (Recommended to use virtual environment)

If using virtual env:

$ python -m venv venv
$ source venv/bin/activate 


Then navigate to the this folder and run:

$ pip install -q build
$ python -m pip install .




## Usage
$ cust-eval count

	-or-

$ cust-eval spend


#### Parameters

-n 			: Top (N) customers will be saved.

--input 	: Filepath of input .csv file

--output 	: Filepath (or folder) to write output .csv file.



#### Example Usage
$ cust-eval [count or spend] -n [number of customers] --input [input .csv] --output [output .csv file]

		for example:

$ cust-eval spend -n 50 --input data.csv --output out.csv

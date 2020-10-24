# csv2ucsf

Convert a 2D spectrum in CSV format to UCSF for analysis using Sparky.

## Requirements

* Python 2 or 3
* Nmrglue (pip install nmrglue)
* Numpy (pip install numpy)


## Usage

Simple usage:

	python csv2ucsf.py <csvfile>

This will output a file called test.ucsf if <csvfile> is test.dat

Or if another output file is desired:

	python csv2ucsf.py <csvfile> -o <ucsffile>


## Example CSV input format

Must by of the format: xppm yppm intensity. I.e.:

	79.998   80.089      21131.75000
	79.980   80.089      20717.71000
	79.962   80.089      20316.47000
	79.944   80.089      19944.45000
	79.927   80.089      19616.31000
	79.909   80.089      19344.20000
	....
The order does not matter. The data will be sorted automatically.


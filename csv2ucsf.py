# csv2ucsf: Convert a 2D spectrum in CSV format to UCSF for analysis using Sparky.
#
#
# USAGE
# -----
# python csv2ucsf.py <csv file>
# or if a particular outfile name is prefereed:
# python csv2ucsf.py <csv file> -o <outfile name>
#
#
# CSV FILES
# ---------
# Must be of the format:
#  xppm  yppm  intensity
#  xppm  yppm  intensity
#  ...
#
# I.e., similar to the format used by NMRPipe: pipe2txt.tcl -index PPM spectrum.ft > spectrum.dat
# The order in the file does not matter. It will be sorted automatically.
#
#
# OTHER DETAILS
# -------------
# Written by: Daniel K. Weber (Veglia Lab)
# University of Minnesota
# Last updated: Nov 6 2020 (Manu)

import numpy as np
import nmrglue as ng
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Covert 2D spectrum in CSV format to USCF format.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'infile', type=str,
        help='Input CSV file in format: xppm yppm intensity.'
    )
    parser.add_argument(
        '-o', '--outfile', type=str, default='',
        help='Output file name. Default: <infile>.ucsf.'
    )
    args = parser.parse_args()
    return args

def main():
    # Read Args
    args = parse_args()
    infile = args.infile
    if args.outfile:
        outfile = args.outfile
    else:
        outfile = '{}.ucsf'.format(os.path.splitext(infile)[0])
    
    # Read X, Y, Z (Intensity) file for 2D spectra
    print('Reading {}...'.format(infile))
    x_list = np.genfromtxt(infile,usecols=(0),dtype=float)
    y_list = np.genfromtxt(infile,usecols=(1),dtype=float)
    z_list = np.genfromtxt(infile,usecols=(2),dtype=float)

    # Sort (high to low ppm) and summarize data
    xi = np.unique(x_list)
    xi = np.sort(xi)[::-1]
    yi = np.unique(y_list)
    yi = np.sort(yi)[::-1]
    x_num = xi.size
    x_max = max(xi)
    x_min = min(xi)
    y_num = yi.size
    y_max = max(yi)
    y_min = min(yi)

    # Print details
    print('X Size: {}'.format(x_num))
    print('Y_Size: {}'.format(y_num))
    print('X Min.: {} ppm, X Max.: {} ppm'.format(x_min, x_max))
    print('Y Min.: {} ppm, Y Max.: {} ppm'.format(y_min, y_max))

    # Read data into dictionary
    print('Converting data to Numpy array...')
    array = dict()
    for x,y,z in zip(x_list,y_list,z_list):
        try:
            array[x][y] = z
        except:
            array[x] = dict()
            array[x][y] = z

    # Convert dictionary to 2x2 array
    rows = []
    for y in yi:
        row = []
        for x in xi:
            row.append(array[x][y])
        rows.append(row)

    data = np.array(rows)
    #print(data.shape)

    # Create NMRGlue Dictionary
    print('Writing UCSF file: {}...'.format(outfile))
    udic = {
        'ndim': 2,
        0: {'car': 100*((y_max+y_min)/2),
            'complex': False,
            'encoding': 'states',
            'freq': True,
            'label': 'w2',
            'obs': 100,
            'size': y_num,
            'sw': 100*(y_max-y_min),
            'time': False},
        1: {'car': 100*((x_max+x_min)/2),
            'complex': False,
            'encoding': 'direct',
            'freq': True,
            'label': 'w1',
            'obs': 100,
            'size': x_num,
            'sw': 100*(x_max-x_min),
            'time': False}
    }
    dic = ng.sparky.create_dic(udic)
    ng.sparky.write(outfile, dic, data.astype('float32'), overwrite=True) 
if __name__ == '__main__':
    main()

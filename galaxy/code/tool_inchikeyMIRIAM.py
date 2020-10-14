#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Galaxy script to query rpFBA REST service

"""
import argparse
import sys

sys.path.insert(0, '/home/')
import inchikeyMIRIAM

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to add InChIkey to MIRIAM annotations')
    parser.add_argument('-input_sbml', type=str)
    parser.add_argument('-output_sbml', type=str)
    params = parser.parse_args()
    inchikeyMIRIAM.main(params.input_sbml, params.output_sbml)

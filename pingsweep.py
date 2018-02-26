from __future__ import print_function
import argparse
import re
import sys

parser = argparse.ArgumentParser(description='Ping sweeps an IP range')
parser.add_argument('range', type=str, help='String in the format [lower_bound]-[upper_bound] or in CIDR notation representing the range to sweep.')


def main():
    args = parser.parse_args()
    ipRange = compileRange(args.range)
    if(ipRange == None):
        parser.print_help()
        sys.exit(1)
   

def compileRange(iprange):
    if(re.match("([0-9]{1,3}.){3}[0-9]{1,3}-([0-9]{1,3}.){3}[0-9]{1,3}", iprange)):
        return [[],[]]
    
    if(re.match("([0-9]{1,3}.){3}[0-9]{1,3}/[0-9]{1,2}", iprange)):
        return [[],[]]

    return None

if __name__ == "__main__":
    main()

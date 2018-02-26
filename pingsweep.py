from __future__ import print_function
import argparse

parser = argparse.ArgumentParser(description='Ping sweeps an IP range')
parser.add_argument('range', type=str, help='String in the format [lower_bound]-[upper_bound] or in CIDR notation representing the range to sweep.')

def main():
    args = parser.parse_args()
    print(args.range)
    
if __name__ == "__main__":
    main()

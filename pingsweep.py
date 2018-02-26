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
   
    print(ipRange)

def compileRange(iprange):
    if(re.match("([0-9]{1,3}.){3}[0-9]{1,3}-([0-9]{1,3}.){3}[0-9]{1,3}", iprange)):
        return [iprange.split("-")[0].split("."),iprange.split("-")[1].split(".")]
    
    if(re.match("([0-9]{1,3}.){3}[0-9]{1,3}/[0-9]{1,2}", iprange)):
        lower_bound = iprange.split("/")[0].split(".")
        mask = int(iprange.split("/")[1])
        if not mask % 8 == 0 or mask > 32 or mask < 0:
            return None

        upper_bound = lower_bound[:]
        for block in range((32 - mask) / 8):
            upper_bound[-(block+1)] = 255

        return [lower_bound, upper_bound]

    return None

if __name__ == "__main__":
    main()

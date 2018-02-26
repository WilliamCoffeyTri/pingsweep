import argparse
import re
import sys
import subprocess
import os

parser = argparse.ArgumentParser(description='Ping sweeps an IP range')
parser.add_argument('-c', '--count', type=int, default=4, help='Number of pings to send to each host.')
parser.add_argument('-w', '--timeout', type=int, help='Time to wait for a response from each host.')
parser.add_argument('range', type=str, help='String in the format [lower_bound]-[upper_bound] or in CIDR notation representing the range to sweep.')

args = parser.parse_args()

def main():
    ipRange = compileRange(args.range)
    if(ipRange == None):
        parser.print_help()
        sys.exit(1)

    report(sweepRange(ipRange))


def compileRange(iprange):
    if(re.match("([0-9]{1,3}.){3}[0-9]{1,3}-([0-9]{1,3}.){3}[0-9]{1,3}", iprange)):
        return [map(int, iprange.split("-")[0].split(".")),map(int, iprange.split("-")[1].split("."))]
    
    if(re.match("([0-9]{1,3}.){3}[0-9]{1,3}/[0-9]{1,2}", iprange)):
        lower_bound = iprange.split("/")[0].split(".")
        mask = int(iprange.split("/")[1])
        if not mask % 8 == 0 or mask > 32 or mask < 0:
            return None

        upper_bound = lower_bound[:]
        for block in range((32 - mask) / 8):
            upper_bound[-(block+1)] = 255

        return [map(int, lower_bound), map(int, upper_bound)]

    return None


def sweepRange(iprange):
    addresses = []

    output = open(os.devnull, 'w')

    for a in range(iprange[0][0], iprange[1][0]+1):
        for b in range(iprange[0][1], iprange[1][1]+1):
            for c in range(iprange[0][2], iprange[1][2]+1):
                for d in range(iprange[0][3], iprange[1][3]+1):
                    ip = str(a) + "." + str(b) + "." + str(c) + "." + str(d)
                    print("Querying Address: " + ip)
                    if(ping(ip, output)):
                        addresses.append(ip)             

    return addresses


def report(liveAddresses):
    print("The following addresses on the range responded: ")
    for address in liveAddresses:
        print(address)


def ping(ip, of):
    command = ['ping']

    command.append('-c')
    command.append(str(args.count))
    
    if not args.timeout == None:
        command.append('-w')
        command.append(str(args.timeout))
    command.append(ip)
    return not subprocess.call(command, stdout=of, stderr=of) 


if __name__ == "__main__":
    main()

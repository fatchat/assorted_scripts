# @brief Generate points on conics, insert into SQL DB in preparation for SSAS analysis
# @author rohit
import sys
import argparse
import tablegenerator
import random
# global vars
dbname = "TimeSeries"
# command-line arguments
parser = argparse.ArgumentParser("quadratic generator")
parser.add_argument("-a", type=float, default=0, help="constant coefficient")
parser.add_argument("-b", type=float, default=0, help="linear coefficient")
parser.add_argument("-c", type=float, default=1.0, help="quadratic coefficient")
parser.add_argument("-s", "--start", type=float, required=True, help="starting x value")
parser.add_argument("-e", "--end", type=float, required=True, help="ending x value")
parser.add_argument("-l", "--length", type=int, required=True, help="number of data points")
parser.add_argument("-t", "--tablename", required=True)
parser.add_argument("-v", "--verbose", required=False, action="store_true")
parser.add_argument("-d", "--dryrun", required=False, action="store_true")
args = parser.parse_args()
# create DB table
tg = tablegenerator.TableGenerator()
tg.verbose = args.verbose
tg.dryrun = args.dryrun
try:
    tg.connect(dbname)
except pypyodbc.DatabaseError:
    print ("Could not connect to db [%s]" % dbname)
    sys.exit(1)
# two columns - x and y, both float
tg.create(args.tablename, [{'name':'x','type':'float' },
                           {'name':'y','type':'float'}])
# insert data points from the curve
for p in range(0,args.length):
    x = random.random() * (args.end - args.start) + args.start
    y = args.a + args.b * x + args.c * x * x
    tg.insert([p, x, y])

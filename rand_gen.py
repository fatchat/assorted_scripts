import sys
import os
import argparse
import random
import tablegenerator

dbname = "TimeSeries"

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--num_ticks", type=int, required=True)
parser.add_argument("-g", "--length", type=int, required=True)
parser.add_argument("-i", "--high", type=float, required=True)
parser.add_argument("-l", "--lo", type=float, required=True)
parser.add_argument("-a", "--alternate", required=False, action="store_true")
parser.add_argument("-t", "--tablename", required=True)
parser.add_argument("-v", "--verbose", required=False, action="store_true")
parser.add_argument("-d", "--dryrun", required=False, action="store_true")
args = parser.parse_args()

tg = tablegenerator.TableGenerator()
tg.verbose = args.verbose
tg.dryrun = args.dryrun
try:
    tg.connect(dbname)
except pypyodbc.DatabaseError:
    print ("Could not connect to db [%s]" % dbname)
    sys.exit(1)
column_spec = [{'name' : "col_%d" % x, 'type' : 'float'} for x in range(0, args.num_ticks)]
column_spec.append ({ 'name' : 'outval', 'type' : 'int'})
tg.create(args.tablename, column_spec)

width = args.high - args.lo

for line in range(0, args.length):
    hi = 1
    if random.random() < 0.5:
        hi = 0
    values = [str(line)]
    for n in range(0,args.num_ticks):
        rand_val = (random.random() - 0.5) * width/10
        out_val = 0
        if (hi == 1):
            out_val = args.high + rand_val
        else:
            out_val = args.lo + rand_val
        if (args.alternate):
            hi = 1 - hi
        values.append(str(out_val))
    values.append(str(hi))
    tg.insert(values)

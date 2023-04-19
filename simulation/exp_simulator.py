import math
import random
import scipy.stats
from scipy.stats import lognorm
import datetime
import argparse
import sys
import numpy as np

def getArguments():
  parser =argparse.ArgumentParser(description="Generate expression count for isoforms of genes")

  parser.add_argument('-T', '--trans', required=True, help='Transcripts in fasta file')
  parser.add_argument('-D', '--dis', default="normal", help="distribution of transcritps expression counts: either 'normal' or 'uniform' or 'lognorm'")
  parser.add_argument('-n', '--mean_count', type=float, default=100.0, help="Mean expression count for all transcripts: used in 'normal' mode")
  parser.add_argument('-s', '--stdDev', type=float, default=20.0, help="Standard deviation of expression count for all transcripts: used in 'normal' mode")
  parser.add_argument('-m', '--min', type=float, default=1, help="Minimun expression counts: used in 'uniform' mode")
  parser.add_argument('-x', '--max', type=float, default=1000, help="Maximun expression counts: used in 'uniform' mode")
  parser.add_argument('-o', '--output', help='File to output the expression count')
  
  args = parser.parse_args()
  print "***** Parameters *****"
  for arg in vars(args):
    print arg,":",getattr(args, arg)
  return args

def loadTrans(fname):
  tran_names = []
  with open(fname) as fin:
    line = fin.readline()
    while line:
      if line[0] == '>':
        name=line[1:].split()[0]
        line = fin.readline()
        while line and line[0] != '>':
          line = fin.readline()
        tran_names.append(name)
      else:
        print "Error parsing fasta file"
        print line
        sys.exit(1)
  return tran_names

args = getArguments()
trans_names = loadTrans(args.trans)
trans_num = len(trans_names)

if args.dis == 'normal':
  trans_count = np.random.normal(args.mean_count, args.stdDev, trans_num)
elif args.dis == 'uniform':
  trans_count = np.random.uniform(args.min, args.max+1, trans_num)
elif args.dis == 'lognorm':
  s=1
  trans_count = lognorm.rvs(s, size=trans_num)
  multiplier = 1000
  for idx in range(0, trans_num):
    tmp = trans_count[idx] * multiplier
    tmp = int(tmp)
    if tmp == 0:
      tmp = 1
    trans_count[idx] = tmp
else:
  print "Invalid distribution : ", args.dis,
  print "Only 'normal' and 'uniform' are supported"
  sys.exit(1)
for i in range(0, trans_num):
  if trans_count[i]<0:
    trans_count[i]=1

if not args.output:
  tmp = args.trans.rfind(".")
  args.output = args.trans[0:tmp]+".expr"

with open(args.output, 'w') as fout:
  for i in range(0, trans_num):
    fout.write(trans_names[i]+"\t"+str(int(round(trans_count[i])))+"\n")


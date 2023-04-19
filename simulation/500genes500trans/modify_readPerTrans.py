import math
import random
import scipy.stats
import datetime
import argparse
import sys
import numpy as np
import csv

def getArguments():
  parser =argparse.ArgumentParser(description="Modification")

  parser.add_argument('-t', '--trans_expr', required=True, help='transcript expression file')
  parser.add_argument('-s', '--readsPerTrans', required=True, help="reads per transcript file")
  parser.add_argument('-o', '--output', required=True, help="output file")

  args = parser.parse_args()
  return args

args = getArguments()
trans_names=[]
#load trans_expression, no header
with open(args.trans_expr, 'r') as fin:
  reader = list(csv.reader(fin, delimiter='\t'))
  #reader.sort(key=lambda x: x[0])
  trans_names = [x[0] for x in list(reader)]

readsPerTrans=[]
with open(args.readsPerTrans, 'r') as fin:
  reader = list(csv.reader(fin, delimiter=','))
  readsPerTrans = [x[1] for x in list(reader)]
  readsPerTrans = readsPerTrans[1:]
  #readsPerTrans = [int(x) for x in readsPerTrans]

with open(args.output, 'w') as fout:
  for x in range(0, len(readsPerTrans)):
    fout.write(trans_names[x]+"\t"+readsPerTrans[x]+"\n")



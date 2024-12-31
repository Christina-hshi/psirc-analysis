import math
import random
import scipy.stats
import datetime
import argparse
import numpy as np
import sys

def getArguments():
  parser = argparse.ArgumentParser(description="Separate linear transcripts and circular transcripts into two files")
  
  parser.add_argument('-i', '--input', required=True, help='raw transcript file in fasta format')
  
  args = parser.parse_args()
  return args

args = getArguments()

tmp = args.input.rfind('.')
prefix = args.input[0:tmp]
linear_trans = prefix+".linear.fa"
circular_trans = prefix+".circular.fa"

with open(args.input, 'r') as fin, open(linear_trans, 'w') as fout_linear, open(circular_trans, 'w') as fout_circular:
  line = fin.readline().strip("\r\n")
  while line:
    head = line
    line = fin.readline().strip("\r\n")
    seq = ''
    while line and line[0] != '>':
      seq += line
      line = fin.readline().strip("\r\n")
    if head[-1]=='C':
      fout_circular.write(head+"\n")
      fout_circular.write(seq+"\n")
    else:
      fout_linear.write(head+"\n")
      fout_linear.write(seq+"\n")


import math
import random
import scipy.stats
import datetime
import argparse
import numpy as np
import sys

def float2str(num):
  return "{:.2f}".format(num)

def getArguments():
  parser = argparse.ArgumentParser(description="Generate one linear and one circular transcript for each gene(or raw transcript) with overlap specified.")
  
  parser.add_argument('-i', '--input', required=True, help='gene(or raw transcript) file in fasta format')
  parser.add_argument('-l', '--overlap', type=float, default=0, help="overlap between the linear and circular transcript")
  parser.add_argument('-o', '--output', help="output to transcript file.")

  args = parser.parse_args()

  if not args.output:
    tmp = args.input.rfind("\/")
    args.output = args.input[0:tmp+1]+"trans.fa"
  print "***** Parameters *****"
  for arg in vars(args):
    print arg,":",getattr(args, arg)

  return args

args = getArguments()
with open(args.input, 'r') as fin, open(args.output, 'w') as fout:
  line = fin.readline().strip("\r\n")
  while line:
    while line[0] != ">":
      line = fin.readline().strip("\r\n")
    descrip = line.split(" ")[0]
    line = fin.readline().strip("\r\n")
    seq = ""
    while line and line[0] != ">":
      seq += line
      line = fin.readline().strip("\r\n")
    seq_len = len(seq)
    overlap_len = int(seq_len * args.overlap)
    tmp = int((seq_len-overlap_len)/2)
    linear_seq = seq[0:tmp+overlap_len]
    cir_seq = seq[tmp:]
    fout.write(descrip+"\n")
    fout.write(linear_seq+"\n")
    fout.write(descrip+"_cir\tC\n")
    fout.write(cir_seq+"\n")

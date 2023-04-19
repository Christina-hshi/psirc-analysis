import math
import random
import scipy.stats
import datetime
import argparse
import sys
import numpy as np
import csv

def getArguments():
  parser =argparse.ArgumentParser(description="Calculate correlation statistics for output from Kallisto-cir, Sailfish-cir")

  parser.add_argument('-t', '--trans_expr', required=True, help='transcript expression file')
  parser.add_argument('-s', '--seq_stats', required=True, help="sequence statistics file")
  parser.add_argument('-m', '--tool', default="K", help="prediction from either [K]Kallisto-cir or [S]Sailfish-cir")
  parser.add_argument('-p', '--pred', required=True, help="Transcript abundance file by kallisto")

  args = parser.parse_args()
  return args

def float2str(num):
  return "{:.2f}".format(num)

args = getArguments()
trans_expr=[]
#load trans_expression, no header
with open(args.trans_expr, 'r') as fin:
  reader = list(csv.reader(fin, delimiter='\t'))
  reader.sort(key=lambda x: x[0])
  trans_expr = [float(x[1]) for x in list(reader)]
  

seq_stats=[]
#load sequence statistics, with header
with open(args.seq_stats, 'r') as fin:
  reader = csv.reader(fin, delimiter='\t')
  seq_stats = list(reader)
  seq_stats.sort(key=lambda x: x[0])
  seq_counts = [float(x[1]) for x in seq_stats]

predict=[]
#load prediction of kallisto, with header
with open(args.pred, 'r') as fin:
  reader = csv.reader(fin, delimiter='\t')
  predict = list(reader)[1:]
  predict.sort(key=lambda x: x[0])
  if args.tool == 'K':
    predict_tpm = [float(x[4]) for x in predict]
    predict_counts = [float(x[3]) for x in predict]
  elif args.tool == 'S':
    predict_tpm = [float(x[3]) for x in predict]
    predict_counts = [float(x[4]) for x in predict]

trans_pearson=scipy.stats.pearsonr(trans_expr, predict_tpm)
trans_spearman=scipy.stats.spearmanr(trans_expr, predict_tpm)
print "#predict tpm VS transcript number"
print "pearson",float2str(trans_pearson[0]), float2str(trans_pearson[1])
print "spearman",float2str(trans_spearman[0]), float2str(trans_spearman[1])

counts_pearson=scipy.stats.pearsonr(seq_counts, predict_counts)
counts_spearman=scipy.stats.spearmanr(seq_counts, predict_counts)
print "#predict counts VS read counts in transcripts"
print "pearson",float2str(counts_pearson[0]), float2str(counts_pearson[1])
print "spearman",float2str(counts_spearman[0]), float2str(counts_spearman[1])


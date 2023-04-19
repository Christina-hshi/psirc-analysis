#!/bin/bash

set -e

if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <psirc-quant> <k>" >&2
	echo "e.g. $0 <dir to psirc-quant> 31"
	exit 1
fi

psirc_quant=$1
k=$2

cal_stats=$(dirname "$0")/500genes500trans/cal_stats.py
psirc_quant_bias_log=psirc-quant-bias-k${k}.log

psirc_quant_bias_dir=psirc-quant-bias-k${k}

t=20
fa1=sample_01_1.fasta
fa2=sample_01_2.fasta
trans_exp_file=trans.expr
readPerTrans=readPerTrans.num

se_fa=sample_01.fasta

fragLen=250
fragLen_stdev=25
min_fragLen=150
max_fragLen=350

$psirc_quant index -i trans.k${k}.index -k $k ../trans.fa >> $psirc_quant_bias_log 2>&1

echo "$psirc_quant quant -i trans.k${k}.index -o ${psirc_quant_bias_dir} --bias -l $fragLen -s $fragLen_stdev $fa1 $fa2" >>$psirc_quant_bias_log
$psirc_quant quant -i trans.k${k}.index -o ${psirc_quant_bias_dir} --bias -l $fragLen -s $fragLen_stdev -x $min_fragLen -X $max_fragLen -t $t $fa1 $fa2 >>$psirc_quant_bias_log 2>&1

date >>$psirc_quant_bias_log 2>&1
echo "***** psirc-quant *****" >> $psirc_quant_bias_log 2>&1
python $cal_stats -t ../$trans_exp_file -s $readPerTrans -p ${psirc_quant_bias_dir}/abundance.tsv -m K >> $psirc_quant_bias_log
date >>$psirc_quant_bias_log 2>&1

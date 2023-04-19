#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <sailfish_cir> <k>" >&2
	echo "e.g. $0 <dir to sailfish_cir> 31"
	exit 1
fi

sailfish_cir=$1
k=$2
cal_stats=$(dirname "$0")/500genes500trans/cal_stats.py
separateLinearCir=$(dirname "$0")/500genes500trans/separateLinearCir.py

output_dir=sailfish-cir-k${k}
mean_frag_len=250
log_file=sailfish-cir-k${k}.log
trans_exp_file=trans.expr
readPerTrans=readPerTrans.num

mkdir -p $output_dir

fa1=sample_01_1.fasta
fa2=sample_01_2.fasta

python $sailfish_cir --linearFa=../trans.linear.fa -1 $fa1 -2 $fa2  --circFa=../trans.circular.fa -o $output_dir -k $k --mll=$mean_frag_len >>$log_file 2>&1

python $cal_stats -t ../$trans_exp_file -s $readPerTrans -m S -p ./${output_dir}/quant_circular/quant.sf >>$log_file

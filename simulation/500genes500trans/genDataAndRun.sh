#!/bin/bash

set -e

if [ "$#" -ne 3 ]; then
	echo -e "\nUsage: $0 <psirc-quant> <sailfish-cir> <k>" >&2
	echo "e.g. $0 <absolute path to psirc-quant> <absolute path to sailfish-cir> 31"
	exit 1
fi

psirc_quant=$1
sailfish_cir=$2
k=$3

gen_trans=./gen_trans.py
gene_file=${PWD}/genes.fa
trans_exp_file=trans.expr

overlap_per_min=0
overlap_per_max=100

for (( overlap_per=$overlap_per_min; overlap_per<=$overlap_per_max; overlap_per = overlap_per+10 )) do
	overlap_ratio=$(printf '%.1f\n' "$(echo "scale=1; $overlap_per/100" | bc)")
	echo $overlap_ratio

	mkdir -p overlap.${overlap_per}
	cd overlap.${overlap_per}
		python ../gen_trans.py -i $gene_file -l $overlap_ratio -o trans.fa >trans.log 2>&1
		# separate linear and circular RNA into different files as the input of Sailfish-cir for quantification
		python ../separateLinearCir.py -i trans.fa
		python ../exp_simulator.py -T trans.fa -D uniform -m 0 -x 1000 >trans.expr.log 2>&1

		/research/d5/rshr/hshi/Tools/miniconda2/bin/Rscript ../../run_polyester_LC.R >/dev/null 2>&1

		cd ./polyesterLC.9M.L100
			python ../../modify_readPerTrans.py -t ../trans.expr -s readPerTrans.num -o readPerTrans.num

			../../../run_psirc-quant.sh $psirc_quant $k
			../../../run_sailfish-cir.sh $sailfish_cir $k
		cd ..

	cd ..
done

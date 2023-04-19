# install.packages("./polyesterLC_1.9.7.tar.gz", repos=NULL, type="source")

library(polyesterLC)
library(Biostrings)

read_num=9000000
frag_mean=250
read_len=100
trans_file="trans.fa"
trans_pseudo_file="trans.pseudo.fa"
trans_expr_file="trans.expr"

trans <- readDNAStringSet(trans_file)
trans_num = length(trans)
trans_lens = width(trans)
circular_trans_idxs=grep("cir", names(trans), fixed=TRUE)
linear_trans_idxs=setdiff(seq_len(length(trans)), circular_trans_idxs)
#trans_lens[linear_trans_idxs] = trans_lens[linear_trans_idxs]-frag_mean+1


#trans_pseudo <- readDNAStringSet(trans_pseudo_file)

data <- read.csv(file=trans_expr_file, header=FALSE, sep="\t")
exp = data[,2]
exp_normalized = (exp/sum(exp))*trans_num
exp_readNum = exp_normalized * trans_lens
#/ read_len
exp_readNum_normalized = exp_readNum/sum(exp_readNum)

readspertx = round(exp_readNum_normalized * read_num)
countmat=matrix(readspertx, nrow=trans_num, ncol=1)
#write.csv(countmat, file="coutmat.csv")

#add GC baises, [0..7], 0 means no bias, 1-7 are built in bias model
#bias=2
#countmat_biased=add_gc_bias(countmat, list(bias), trans)
#write.csv(countmat_biased, file="coutmat_biased.csv")

#fold_changes = matrix(rep(1, 2*trans_num), ncol=2)

outdir = paste("polyesterLC.9M.", "L", as.character(read_len) ,sep="")

#outdir = "polyester.LC"
#outdir = paste("polyesterLC.bias",as.character(bias),".9M.", "L", as.character(read_len),sep="")

dir.create(file.path(outdir), showWarnings = FALSE)

write.csv(readspertx, file=paste(outdir, "/readPerTrans.num", sep=""))

#simulate_experiment(trans_pseudo_file, reads_per_transcript=readspertx, num_reps=c(10,10), fold_changes=fold_changes, outdir=outdir)
#simulate_experiment_countmat(trans_pseudo_file, readmat=countmat, outdir=outdir, paired=FALSE)
simulate_experiment_countmat_LC(trans_file, readmat=countmat, outdir=outdir)

#simulate_experiment_countmat_LC(trans_file, readmat=countmat_biased, outdir=outdir)

args=commandArgs(trailingOnly=TRUE)

fn=args[1]

require("ggplot2")

score_df=read.table(fn,sep="\t")

colnames(score_df)=c("Hit","Score")

ggplot(score_df,aes(x=Score))+geom_histogram()

basefn=tools::file_path_sans_ext(fn)
outfn = paste(basefn,".histogram.pdf",sep="")
ggsave(outfn)

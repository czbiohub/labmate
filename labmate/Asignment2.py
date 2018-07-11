import pandas as pd 
import sys 

def asignment2_summarystats(path):
        """
        I want to describe what this function does.
        """
        df=pd.read_csv(path, sep="\t")
        n_del_max=max(df["n_deleted"])
        n_mut_max=max(df["n_mutated"])
        n_ins_max=max(df["n_inserted"])
        unmod_perc=sum(df["%Reads"][df.UNMODIFIED])   
        return n_del_max, n_mut_max, n_ins_max, unmod_perc

if __name__== "__main__":
        n_del_max, n_mut_max, n_ins_max, unmod_perc = asignment2_summarystats(sys.argv[1])
        print ("Max deletion size = " + str(int(n_del_max)))
        print("Max mutation size = " + str(int(n_mut_max)))
        print("Max insertion size = " + str(int(n_ins_max)))
        print("Percent unmodified total = " +str(unmod_perc))
        print("To access values as variables set summary_stats function equal to max_del, max_mut, max_ins, perc_unmod")

        print("we are running from the command line")



# coding: utf-8

# In[5]:


import catheat
import numpy as np
import pandas as pd 
from functools import reduce 

get_ipython().magic('matplotlib inline')
import glob
import os.path


# ### Function that will take in any number of CSVs for metadata for an experiment 

# In[6]:


def make_metadata(path_to_plates, well_type, path_to_data, date):
    ## function that take in formatted csv plates maps from 96 well of 384 well plates and returns metatdata dataframe
    ## path_to_plates = absolute path to csvs for your plate layout 
    ## well_type= well_id_96 or well_id_384
    ## date=date of creating metadata 
    all_csv=glob.glob("{}/*.csv".format(path_to_plates)) #import all plate maps 
    
    dict_of_dfs={}

    for file in all_csv:
        file_name=os.path.splitext(os.path.basename(file))[0] # split based on extension
        df=pd.read_csv(file)
        dict_of_dfs[file_name]=df
    
    def remove_cols(df):
    ### define a function that will drop unwanted columns from your df along the column axis
        cols_to_drop = ['row_letter', 'col_num'] 
        removed_cols = df.drop(cols_to_drop, axis=1)
        return removed_cols

    tidy_files={} ## set and empty dictionary to which we will add key value pairs, your file name and the long format of a given 96 well plate
    
    for file_name, data_frame in dict_of_dfs.items():
        df=pd.melt(data_frame, id_vars="row_letter", var_name="col_num", value_name=file_name) # turn 96 well format into long format, returning a df with a list of values for each well in your 96 well plate.  
        df[well_type]=df["row_letter"] + df["col_num"] # make a new column to combine row letter with col number. 
        tidy_files[file_name]= remove_cols(df) # pass the df into the remove cols function to remove col for row letter and col number and add to dictionary with asoociated file name. 

    dfs=list(tidy_files.values()) # create list of tidy dataframes
    dfs_merged=reduce(lambda left,right: pd.merge(left,right, on=well_type), dfs) # merge all dataframes together on well_id
    dfs_merged.to_csv("{a}/{b}_metadata.csv".format(a=path_to_data, b=date))
    
    return dfs_merged

dataframes=make_metadata(path_to_plates="/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/plate_csv", well_type="well_id_96", path_to_data="/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data", date="20180529")

dataframes


# In[1]:


get_ipython().system(' jupyter nbconvert --to script 20180601_Giana_Aaron_labmate_96_plateconversions.ipynb')


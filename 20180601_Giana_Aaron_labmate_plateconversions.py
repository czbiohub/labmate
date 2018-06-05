
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


# ## import_coords_and_index
# This function will take in the following parameters:
# 
# 1) metadata_df= metadata from make_metadata()function above. Currently this must already be read into the notebook
# 
# 2) path_to_coords= path to the folder containing the 96 to 384 coordinate conversation 
# 
# 3) path_to_i7_384 = path to folder containing i7_indexes from 384 well plate 
# 
# 4) path_to_i5_384 = path to folder containing the i5_indexes from 384 well plate 
# 
# 5) i7_384_coord = coordinate from your i7 384 well plate you want to draw from 
# 
# 6) i7_keyname = name of csv for the particular i7 index plate you are using
# 
# 7) i5_384_coord = coordinate from your i5 384 well plate you want to draw from 
# 
# 8) i5_keyname = name of csv for the particular i5 index plate you are using
# 
# 9) well_type = default is "well_id_96"
# 
# 10) path_to_data=path to folder where you will store your final table
# 
# 11) date= date to be appended to your final sheet 
# 
# 12) name= name of the final file, defaul is "metadata_indexes"

# In[7]:



dfs_merged=pd.read_csv("/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data/20180529_metadata.csv")
dfs_merged=dfs_merged.drop("Unnamed: 0", axis=1)


def import_coords_and_index(metadata_df, path_to_coords, path_to_i7_384, path_to_i5_384, i7_384_coord, i7_keyname, i5_384_coord, i5_keyname, well_type, path_to_data, date, name="metadata_indexes"):
    
    all_coords=glob.glob("{}/*.csv".format(path_to_coords))
    all_i7_index_384=glob.glob("{}/*.csv".format(path_to_i7_384))
    all_i5_index_384=glob.glob("{}/*.csv".format(path_to_i5_384))
    
    dict_all_i7_index_384={}

    for file in all_i7_index_384:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_all_i7_index_384[file_name]=df

    dict_all_i5_index_384={}

    for file in all_i5_index_384:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_all_i5_index_384[file_name]=df

    dict_of_coords={}

    for file in all_coords:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_of_coords[file_name]=df
    
    i7=dict_of_coords[i7_384_coord].merge(dict_all_i7_index_384[i7_keyname],left_on=i7_384_coord, right_on="i7_index_384")
    i5=dict_of_coords[i5_384_coord].merge(dict_all_i5_index_384[i5_keyname],left_on=i5_384_coord, right_on="i5_index_384")
    i7_added=i7.merge(metadata_df, left_on=well_type, right_on=well_type)
    i7_i5_added=i7_added.merge(i5,left_on=well_type, right_on=well_type)
    
    i7_i5_added.to_csv()
    i7_i5_added.to_csv("{a}/{b}_{c}.csv".format(a=path_to_data, b=date, c=name))
    return i7_i5_added
    
    
import_coords_and_index(metadata_df=dfs_merged, path_to_coords='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/coord_maps',path_to_i7_384='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/i7_index_384', path_to_i5_384='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/i5_index_384',i7_384_coord="coord1_384", i7_keyname="i7_index_384", i5_384_coord="coord2_384", i5_keyname="i5_index_384", well_type="well_id_96", path_to_data="/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data", date=20180529)


# In[ ]:



dfs_merged=pd.read_csv("/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data/20180528_metadata.csv")
dfs_merged=dfs_merged.drop("Unnamed: 0", axis=1)


def import_coords_and_index(metadata_df, path_to_coords, path_to_i7_384, path_to_i5_384, i7_384_coord, i7_keyname, i5_384_coord, i5_keyname, well_type, path_to_data, date, name="metadata_indexes"):
    
    all_coords=glob.glob("{}/*.csv".format(path_to_coords))
    all_i7_index_384=glob.glob("{}/*.csv".format(path_to_i7_384))
    all_i5_index_384=glob.glob("{}/*.csv".format(path_to_i5_384))
    
    dict_all_i7_index_384={}

    for file in all_i7_index_384:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_all_i7_index_384[file_name]=df

    dict_all_i5_index_384={}

    for file in all_i5_index_384:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_all_i5_index_384[file_name]=df

    dict_of_coords={}

    for file in all_coords:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_of_coords[file_name]=df
    
    i7=dict_of_coords[i7_384_coord].merge(dict_all_i7_index_384[i7_keyname],left_on=i7_384_coord, right_on="i7_index_384")
    i5=dict_of_coords[i5_384_coord].merge(dict_all_i5_index_384[i5_keyname],left_on=i5_384_coord, right_on="i5_index_384")
    i7_added=i7.merge(metadata_df, left_on=well_type, right_on=well_type)
    i7_i5_added=i7_added.merge(i5,left_on=well_type, right_on=well_type)
    i7_i5_added.to_csv()
    i7_i5_added.to_csv("{a}/{b}_{c}.csv".format(a=path_to_data, b=date, c=name))
    return i7_i5_added
    
    
import_coords_and_index(metadata_df=dfs_merged, path_to_coords='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/coord_maps',path_to_i7_384='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/i7_index_384', path_to_i5_384='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/i5_index_384',i7_384_coord="coord2_384", i7_keyname="i7_index_384", i5_384_coord="coord2_384", i5_keyname="i5_index_384", well_type="well_id_96", path_to_data="/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data", date=20180529)


# In[8]:



dfs_merged=pd.read_csv("/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data/20180529_metadata.csv")
dfs_merged=dfs_merged.drop("Unnamed: 0", axis=1)


def import_coords_and_index(metadata_df, path_to_coords, path_to_i7_384, path_to_i5_384, i7_384_coord, i7_keyname, i5_384_coord, i5_keyname, well_type, path_to_data, date, name="metadata_indexes"):
    
    all_coords=glob.glob("{}/*.csv".format(path_to_coords))
    all_i7_index_384=glob.glob("{}/*.csv".format(path_to_i7_384))
    all_i5_index_384=glob.glob("{}/*.csv".format(path_to_i5_384))
    
    dict_all_i7_index_384={}

    for file in all_i7_index_384:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_all_i7_index_384[file_name]=df

    dict_all_i5_index_384={}

    for file in all_i5_index_384:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_all_i5_index_384[file_name]=df

    dict_of_coords={}

    for file in all_coords:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_of_coords[file_name]=df
    
    i7=dict_of_coords[i7_384_coord].merge(dict_all_i7_index_384[i7_keyname],left_on=i7_384_coord, right_on="i7_index_384")
    i5=dict_of_coords[i5_384_coord].merge(dict_all_i5_index_384[i5_keyname],left_on=i5_384_coord, right_on="i5_index_384")
    i7_added=i7.merge(metadata_df, on=well_type)
    i7_i5_added=i7_added.merge(i5, on=well_type)
    
    i7_i5_added.to_csv()
    i7_i5_added.to_csv("{a}/{b}_{c}.csv".format(a=path_to_data, b=date, c=name))
    return i7_i5_added
    
    
import_coords_and_index(metadata_df=dfs_merged, path_to_coords='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/coord_maps',path_to_i7_384='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/i7_index_384', path_to_i5_384='/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/i5_index_384',i7_384_coord="coord1_384", i7_keyname="i7_index_384", i5_384_coord="coord2_384", i5_keyname="i5_index_384", well_type="well_id_96", path_to_data="/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data", date=20180529)


# In[10]:


get_ipython().system(' jupyter nbconvert --to 20180601_Giana_Aaron_labmate_plateconversions.py 20180601_Giana_Aaron_labmate_plateconversions.ipynb')


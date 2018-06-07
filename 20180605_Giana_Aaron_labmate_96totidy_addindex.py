
# coding: utf-8

# In[1]:


import pandas as pd 
from functools import reduce 

get_ipython().magic('matplotlib inline')
import glob
import os.path


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

# Practice using class methods 

# class MetaData:
#     RETURNED_DATA="returned_data"
#     
#     def __init__(self, merged_metadata_csv_name):
#         self.metadata_path= RETURNED_DATA/merged_metadata_csv_name
#     def read_df():
#         metadata_df=pd.read_csv("self.metadata_path")
# x=MetaData("20180528_metadata.csv")

# In[20]:


class PathTo:
    COORD_CONVS='coordinate_conversion_maps'
    i7_INDEXES='i7_indexes_plates'
    i5_INDEXES='i5_indexes_plates'
    RETURNED_DATA="returned_data"

class IndexPlateChoices: 
    def __init__(self, i7_plate_name, i7_chosen_coord, i5_plate_name, i5_chosen_coord):
        self.i7_plate_name = i7_plate_name
        self.i5_plate_name = i5_plate_name
        self.i7_chosen_coord = i7_chosen_coord
        self.i5_chosen_coord = i5_chosen_coord       


# In[21]:


## define paths and index selections 

data_paths_20180607 = PathTo()
chosen_indices_20180607 = IndexPlateChoices("i7_index_384", "coord1_384", "i5_index_384", "coord1_384")


# In[22]:


## read in df 

dfs_merged=pd.read_csv("/Users/giana.cirolia/Desktop/Nucleofection_Pipelne_Code/returned_data/20180529_metadata.csv")
dfs_merged=dfs_merged.drop("Unnamed: 0", axis=1)


# In[44]:



def convert_csv_to_df(path_to_data):
    all_data=glob.glob("{}/*.csv".format(path_to_data))
    
    dict_of_all_data={}

    for file in all_data:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_of_all_data[file_name]=df
    return dict_of_all_data

def import_coords_and_index(metadata_df,
                            path_to_plates,
                            chosen_indices,
                            well_type, 
                            date, 
                            saved_csv_name="metadata_indexes"):
    
    dict_i7_indices = convert_csv_to_df(data_paths.i7_INDEXES)
    dict_i5_indices = convert_csv_to_df(data_paths.i5_INDEXES)
    dict_of_coords = convert_csv_to_df(data_paths.COORD_CONVS)
    
    
    i7_selected_indices=dict_of_coords[chosen_indices.i7_chosen_coord].merge(dict_i7_indices[chosen_indices.i7_plate_name],left_on=chosen_indices.i7_chosen_coord, right_on=chosen_indices.i7_plate_name)
    i5_selected_indices=dict_of_coords[chosen_indices.i5_chosen_coord].merge(dict_i5_indices[chosen_indices.i5_plate_name],left_on=chosen_indices.i5_chosen_coord, right_on=chosen_indices.i5_plate_name)
    i7_metadata_merged=i7_selected_indices.merge(metadata_df, on=well_type)
    i5_i7_metadata_merged=i7_metadata_merged.merge(i5_selected_indices,on=well_type)
    
    i5_i7_metadata_merged.to_csv("{a}/{b}_{c}.csv".format(a=path_to_plates.RETURNED_DATA, b=date, c=saved_csv_name))
    return i5_i7_metadata_merged
    
import_coords_and_index(metadata_df = dfs_merged,
                            path_to_plates = path_to_plates_20180607,
                            chosen_indices = chosen_indices_20180607,
                            well_type ="well_id_96", 
                            date = "20180607", 
                            saved_csv_name="metadata_with_indices")
    


# ### Convert your work to a python script. 
# 
# `! jupyter nbconvert --to script [yournotebookname].ipynb`

# In[8]:


get_ipython().system(' jupyter nbconvert --to script 20180605_Giana_Aaron_labmate_96totidy_addindex.ipynb')


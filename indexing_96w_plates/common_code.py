## make classes for accessing paths, metadat and indices
import pandas as pd
import os.path
import glob


class MetaData:
    def __init__(self, metadata_dir, metadata_csv):
        self.path = "{a}/{b}".format(a=metadata_dir, b=metadata_csv)
        self.name = os.path.splitext(metadata_csv)[0]

    def make_df(self):
        return pd.read_csv(self.path).drop("Unnamed: 0", axis=1)

    def col_names(self):
        return pd.read_csv(self.path).columns


class PathTo:
    COORD_CONVS='coordinate_conversion_maps'
    i7_INDEXES='i7_indexes_plates'
    i5_INDEXES='i5_indexes_plates'
    RETURNED_DATA="returned_data"


class PlateChoices:
    def __init__(self, i7_plate_name, i7_chosen_coord, i5_plate_name, i5_chosen_coord):
        self.i7_plate_name = i7_plate_name
        self.i5_plate_name = i5_plate_name
        self.i7_chosen_coord = i7_chosen_coord
        self.i5_chosen_coord = i5_chosen_coord
        self.merge_384w = "well_id_384"
        self.merge_96w = "well_id_96"


class MergeParams:
    def __init__(self, index_merge_id, plate_merge_id):
        self.index_merge_id = index_merge_id
        self.plate_merge_id = plate_merge_id


def convert_csv_to_df(path_to_data):
    all_data=glob.glob("{}/*.csv".format(path_to_data))

    dict_of_all_data={}

    for file in all_data:
        file_name=os.path.splitext(os.path.basename(file))[0]
        df=pd.read_csv(file)
        dict_of_all_data[file_name]=df
    return dict_of_all_data


def import_coords_and_index(metadata_df,
                            data_paths,
                            chosen_indices,
                            plate_merge_params,
                            date,
                            saved_csv_name="metadata_w_indexes"):

    dict_i7_indices = convert_csv_to_df(data_paths.i7_INDEXES) ## could also so PathTo.i7_INDEXES bc all constants ( cool)
    dict_i5_indices = convert_csv_to_df(data_paths.i5_INDEXES)
    dict_of_coords = convert_csv_to_df(data_paths.COORD_CONVS)


    i7_selected_indices=dict_of_coords[chosen_indices.i7_chosen_coord].merge(dict_i7_indices[chosen_indices.i7_plate_name],left_on=chosen_indices.i7_chosen_coord, right_on=plate_merge_params.index_merge_id)
    i5_selected_indices=dict_of_coords[chosen_indices.i5_chosen_coord].merge(dict_i5_indices[chosen_indices.i5_plate_name],left_on=chosen_indices.i5_chosen_coord, right_on=plate_merge_params.index_merge_id)
    i7_metadata_merged=i7_selected_indices.merge(metadata_df, on=plate_merge_params.plate_merge_id)
    i5_i7_metadata_merged=i7_metadata_merged.merge(i5_selected_indices,on=plate_merge_params.plate_merge_id)

    i5_i7_metadata_merged.to_csv("{a}/{b}_{c}.csv".format(a=data_paths.RETURNED_DATA, b=date, c=saved_csv_name))
    return i5_i7_metadata_merged

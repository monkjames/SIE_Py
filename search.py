import pandas as pd
import config
import os
import utils as ut
import stf


def load_pickle_files(directory):
    dfs = []  # Initialize an empty list to store dataframes

    # Traverse through all pickle files in the given directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pkl'):  # Check if the file is a pickle file
                filepath = os.path.join(root, file)
                df = pd.read_pickle(filepath)  # Load the pickle file into a DataFrame
                df['full_filepath'] = filepath.replace(config.PICKLE,'')[1:]  # Add a new column with the full file path
                dfs.append(df)  # Append the DataFrame to the list

    master_df = pd.concat(dfs, ignore_index=True)  # Concatenate all DataFrames
    
    return master_df  # Return the final DataFrame

def find(search_value: str, search_field: str = "Value", case_sensitive: bool = True, search_file: str = ""):
    if len(search_file) > 0:
        return sdf[(sdf[search_field].str.contains(search_value, case=case_sensitive, na=False)) & (sdf['full_filepath'].str.contains(search_file.replace('.pkl',''), case=False, na=False))]
    else:
        return sdf[sdf[search_field].str.contains(search_value, case=case_sensitive, na=False)]

def replace(data):
    if not os.path.exists(config.TRE_STAGING):
        os.makedirs(config.TRE_STAGING)
    for d in data:
        file_path = ''
        try:
            file_path = d[3]
        except IndexError:
            pass
        res = find(d[1],d[0],True,file_path)
        for i in range(len(res)):
            exf = ut.get_excel(res.iloc[i,2])
            print(exf)
            prdf = pd.read_excel(exf)
            ndata = []
            for j in range(len(prdf)):
                if prdf.iloc[j,0] == res.iloc[i,0]:
                    ndata.append([prdf.iloc[j,0], prdf.iloc[j,1].replace(d[1],d[2])])
                else:
                    ndata.append([prdf.iloc[j,0], prdf.iloc[j,1]])
            pndf = pd.DataFrame(ndata, columns=['ID', 'Value'])
            pndf.to_excel(exf, index=False)
            nexc = exf.replace(config.EXCEL,'')[1:]
            print(nexc.replace('.xlsx', ''))
            stf.excel_publish(nexc.replace('.xlsx', ''))

sdf = load_pickle_files(config.PICKLE)
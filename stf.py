import os
import sie
import config
import utils as ut
import pandas as pd

import clr
clr.AddReference("System")
from System import Array, Byte

def new_stf_from_df(df: pd.DataFrame, stf_name: str):
    stf_file = ut.get_stf(stf_name)
    if os.path.exists(stf_file):
        raise FileExistsError(f"The file {stf_name} already exists.")
    stf = sie.StringFile()
    stf_file = ut.get_stf(stf_file)
    for row in df.itertuples(index=False):
        stf.Entries.append(sie.StringEntry(row.ID, row.Value))

    iffwr = sie.IffWriter()
    stf.write_object(iffwr)

    data = iffwr.Data() 
    buffer = Array[Byte](data)
    bytes_data = bytes(buffer)

    with open(stf_file, 'wb') as f:
        f.write(bytes_data)

    with open(stf_file.replace(config.STF, config.TRE_STAGING), 'wb') as f:
        f.write(bytes_data)

    stf_to_excel(stf_name)

def new_stf_from_excel(excel_file: str):
    excel = ut.get_excel(excel_file)
    df = pd.read_excel(excel)
    stf_file = ut.get_stf(excel_file)
    if os.path.exists(stf_file):
        raise FileExistsError(f"The file {excel_file} already exists.")
    stf = sie.StringFile()
    stf_file = ut.get_stf(stf_file)
    for row in df.itertuples(index=False):
        stf.Entries.append(sie.StringEntry(row.ID, row.Value))

    iffwr = sie.IffWriter()
    stf.write_object(iffwr)

    data = iffwr.Data() 
    buffer = Array[Byte](data)
    bytes_data = bytes(buffer)

    with open(stf_file, 'wb') as f:
        f.write(bytes_data)

    with open(stf_file.replace(config.STF, config.TRE_STAGING), 'wb') as f:
        f.write(bytes_data)

def add_to_stf(df: pd.DataFrame, stf_file: str):
    sdf = stf_to_df(stf_file)
    mdf, _ = merge_dataframes(df, sdf, True)
    stf = sie.StringFile()
    stf_file = ut.get_stf(stf_file)
    for row in mdf.itertuples(index=False):
        stf.Entries.append(sie.StringEntry(row.ID, row.Value))

    iffwr = sie.IffWriter()
    stf.write_object(iffwr)

    data = iffwr.Data() 
    buffer = Array[Byte](data)
    bytes_data = bytes(buffer)

    with open(stf_file, 'wb') as f:
        f.write(bytes_data)

    with open(stf_file.replace(config.STF, config.TRE_STAGING), 'wb') as f:
        f.write(bytes_data)

def excel_publish(stf_file: str):
    # this takes the excel file and just pushes it as string
    # You CAN break a string file if your IDs are not unique
    df = pd.read_excel(ut.get_excel(stf_file))
    stf = sie.StringFile()
    stf_file = ut.get_stf(stf_file)
    for row in df.itertuples(index=False):
        stf.Entries.append(sie.StringEntry(row.ID, row.Value))

    iffwr = sie.IffWriter()
    stf.write_object(iffwr)

    data = iffwr.Data() 
    buffer = Array[Byte](data)
    bytes_data = bytes(buffer)

    with open(stf_file, 'wb') as f:
        f.write(bytes_data)

    file_path = stf_file.replace(config.STF, config.TRE_STAGING)

    # Get the directory name
    dir_name = os.path.dirname(file_path)

    # If directory does not exist, create it
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Now, you can safely write your file
    with open(file_path, 'wb') as f:
        f.write(bytes_data)

def merge_and_publish(stf_file: str, overwrite: bool=False):
    # This method will take the original STF and excel and make sure the excel doesn't screw up
    # read the string file to df
    df = stf_to_df(stf_file)
    # merge data frames with overwrite = True
    dfn = pd.read_excel(ut.get_excel(stf_file))
    exdn, dupes = merge_dataframes(df, dfn, overwrite)
    stf_file = ut.get_stf(stf_file)
    stf = sie.StringFile()


    for row in exdn.itertuples(index=False):
        stf.Entries.append(sie.StringEntry(row.ID, row.Value))

    
    iffwr = sie.IffWriter()
    stf.write_object(iffwr)

    data = iffwr.Data()  # Assuming iffwr.Data() returns a System.Byte[]

    # Convert System.Byte[] to a Python byte[] (if necessary)
    buffer = Array[Byte](data)
    bytes_data = bytes(buffer)

    # Write the bytes to a file
    with open(stf_file, 'wb') as f:
        f.write(bytes_data)

    with open(stf_file.replace(config.STF, config.TRE_STAGING), 'wb') as f:
        f.write(bytes_data)

    return dupes, exdn
    

def merge_dataframes(df, dfn, overwrite=False):
    if overwrite:
        # Use 'outer' to include all records. Values from dfn will overwrite df by default
        merged = pd.merge(df, dfn, on='ID', how='outer')
        duplicated = merged.duplicated('ID')
    else:
        # Default behavior, append dfn to df, keep the original IDS in df
        merged = pd.concat([df, dfn], ignore_index=True)
        merged.drop_duplicates(subset='ID', keep='first', inplace=True)
        duplicated = merged[merged.duplicated('ID', keep=False)]['ID'].values

    return merged, duplicated


def stf_to_excel(sfile):
    stfile = ut.get_stf(sfile)

    if os.stat(stfile).st_size == 0:
        print(f'File is empty, ignoring it. {stfile}')
        return
    
    iffstr = sie.IffStream(stfile)
    stf = sie.StringFile()
    stf.read_object(iffstr)
    # turn STF into a data table
    df = pd.DataFrame([{'ID': entry.ID, 'Value': entry.Value} for entry in stf.Entries])
    
    excel_file = ut.get_excel(sfile)
    os.makedirs(os.path.dirname(excel_file), exist_ok=True)
    df.to_excel(excel_file, index=False)
    return df

def stf_to_pickle(sfile):
    stfile = ut.get_stf(sfile)

    if os.stat(stfile).st_size == 0:
        print(f'File is empty, ignoring it. {stfile}')
        return
    
    iffstr = sie.IffStream(stfile)
    stf = sie.StringFile()
    stf.read_object(iffstr)
    # turn STF into a data table
    df = pd.DataFrame([{'ID': entry.ID, 'Value': entry.Value} for entry in stf.Entries])
    
    pickle_file = ut.get_pkl(sfile)
    os.makedirs(os.path.dirname(pickle_file), exist_ok=True)

    df.to_pickle(pickle_file)
    return df


def stf_to_df(sfile):
    stfile = ut.get_stf(sfile)

    if os.stat(stfile).st_size == 0:
        print(f'File is empty, ignoring it. {stfile}')
        return
    
    iffstr = sie.IffStream(stfile)
    stf = sie.StringFile()
    stf.read_object(iffstr)
    # turn STF into a data table
    df = pd.DataFrame([{'ID': entry.ID, 'Value': entry.Value} for entry in stf.Entries])
    return df


def update_excel_pickle(make_excel: bool = True, make_pickle: bool = True):
    root = config.STF
    for root, dirs, files in os.walk(root):
        for file in files:
            lpath = os.path.join(root, file).replace(config.STF, '')[1:]
            if make_excel:
                stf_to_excel(lpath)
            if make_pickle and len(config.PICKLE) > 0:
                stf_to_pickle(lpath)

def build_master():
    dfs = []  # Initialize an empty list to store dataframes
    root = config.EXCEL
    for root, dirs, files in os.walk(root):
        for file in files:
            lpath = os.path.join(root, file).replace(config.STF, '')
            df = pd.read_excel(lpath)
            dfs.append(df)  # Append each dataframe to the list
    master_df = pd.concat(dfs, ignore_index=True)  # Concatenate all dataframes in the list
    return master_df  # Return the final dataframe
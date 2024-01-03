import os
import config
import re

def get_file(file, extension):
    parts = split_file_path(file)
    if not parts[-1].endswith(extension):
        parts[-1] = replace_extension(parts[-1], extension)

    # Choose the appropriate root config based on the extension
    if extension == '.xlsx':
        root_config = config.EXCEL
    elif extension == '.stf':
        root_config = config.STF
    elif extension == '.pkl':
        root_config = config.PICKLE
    else:
        raise ValueError(f"Unsupported file extension: {extension}")
    
    return os.path.join(root_config, *parts)


def get_stf(file):
    return get_file(file, '.stf')

def get_pkl(file):
    return get_file(file, '.pkl')

def get_excel(file):
    return get_file(file, '.xlsx')

def split_file_path(file_path):
    return re.split('[\\\\/]', file_path)

def replace_extension(file_name, new_extension):
    name, ext = os.path.splitext(file_name)
    return name + new_extension

def remove_root_from_parts(parts, root):
    root_parts = split_file_path(root)
    if parts[:len(root_parts)] == root_parts:
        parts = parts[len(root_parts):]
    return parts

def stf_to_excel(stf_file):
    parts = split_file_path(stf_file)
    if parts[-1].endswith('.stf'):
        parts[-1] = replace_extension(parts[-1], '.xlsx')
    parts = remove_root_from_parts(parts, config.STF)        
    return os.path.join(config.EXCEL, *parts)

def stf_to_pickle(stf_file):
    parts = split_file_path(stf_file)
    if parts[-1].endswith('.stf'):
        parts[-1] = replace_extension(parts[-1], '.pkl')
    parts = remove_root_from_parts(parts, config.STF)        
    return os.path.join(config.PICKLE, *parts)

def excel_to_stf(excel_file):
    parts = split_file_path(excel_file)
    if parts[-1].endswith('.xlsx'):
        parts[-1] = replace_extension(parts[-1], '.stf')
    parts = remove_root_from_parts(parts, config.EXCEL)        
    return os.path.join(config.STF, *parts)

def excel_to_pickle(excel_file):
    parts = split_file_path(excel_file)
    if parts[-1].endswith('.xlsx'):
        parts[-1] = replace_extension(parts[-1], '.pkl')
    parts = remove_root_from_parts(parts, config.EXCEL)        
    return os.path.join(config.PICKLE, *parts)

def pickle_to_excel(pickle_file):
    parts = split_file_path(pickle_file)
    if parts[-1].endswith('.pkl'):
        parts[-1] = replace_extension(parts[-1], '.xlsx')
    parts = remove_root_from_parts(parts, config.PICKLE)        
    return os.path.join(config.EXCEL, *parts)
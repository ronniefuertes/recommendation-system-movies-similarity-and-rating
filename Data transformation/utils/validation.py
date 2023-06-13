"""
This module provides functions to transform and standardize data.

Available Functions:
- convert_to_numeric: Convert the values in a column to numeric type.
- date_pattern: Check "yyyy-mm-dd" date pattern.
- count_duplicates: Check and count duplated values from a column.
- remove_duplicates: Remove rows of a DataFrame with duplacated values from the specified column.
- count_blanks: Counts the number of blank values in a column of a DataFrame.
- remove_blanks: Remove rows of a DataFrame with blank values from the specified column.
- check_valid_expression: Check valid Python expressions in the values of a column.
- directories_duplicates: Check for duplicate directories.
- extract_values: Extract nested data from columns.
- extract_dir_values: Extract values from a dictionary.
"""

import re
import ast
import pandas as pd
import numpy as np


def convert_to_numeric(dataset, column_name, fillna=None):
    """
    Convert the values in a column to numeric type, with optional filling of non-convertible values.

    Parameters:
        dataset: The DataFrame containing the column.
        column_name: The name of the column to convert.
        fillna (optional): The value to fill for non-convertible values. 
                            If None, original values are used.

    Returns:
        The DataFrame with the converted column.

    """
    # Convert the column to numeric type, with optional filling of non-convertible values
    converted_column = pd.to_numeric(dataset[column_name], errors='coerce')
    
    # Replace NaN values with the specified fillna value
    if fillna is not None:
        converted_column.fillna(fillna, inplace=True) # Replacing values
    else:
        converted_column.fillna(dataset[column_name], inplace=True) # Original values
    
    # Update the column with the converted values
    dataset[column_name] = converted_column
    
    return dataset


def date_pattern(column_name, pattern=0):
    """ 
    Check "yyyy-mm-dd" date pattern.

    Parameters:
    - column_name: Name of the column to check for the "yyyy-mm-dd" pattern.
    - pattern: choose between option 0 or 1,  default is 0.

    Returns:
    - 0: List with values that DO match the pattern.
    - 1: List with values that DON'T match the pattern.
    """
    if pattern not in [0, 1]:
        return "2nd parameter must be 0 or 1"
    
    standard_dates = []
    non_standard_dates = []

    if pattern == 1:
        for value in column_name:
            if not re.match(r"\d{4}-\d{2}-\d{2}", str(value)):
                non_standard_dates.append(value)
    else:
        for value in column_name:
            if re.match(r"\d{4}-\d{2}-\d{2}", str(value)):
                standard_dates.append(value)

    return non_standard_dates if pattern == 1 else standard_dates


def count_duplicates(column_name):
    """ 
    Check and count duplated values from a column.
    
    Parameters:
    - column_name: Name of the column to check for duplicates.

    Returns:
    - List of duplicated values and the quantity of them.
    """
    duplicates = column_name[column_name.duplicated()]
    duplicates_count = duplicates.value_counts()
    return duplicates_count


def remove_duplicates(dataset, column_name):
    """ 
    Remove rows of a DataFrame with duplacated values from the specified column.
    
    Parameters:
    - dataset: DataFrame containing the data.
    - column_name: Name of the column to check for duplicates.

    Returns:
    - DataFrame without rows containing duplicated values in the specified column.
    """
    data_without_duplicates = dataset.drop_duplicates(subset=[column_name], keep='first')
    return data_without_duplicates


def count_blanks(dataset, column_name):
    """
    Counts the number of blank values in a column of a DataFrame.
    
    Parameters:
    - dataset: DataFrame containing the data.
    - column_name: Name of the column to count the blank values.
    
    Returns:
        int: The number of blank values in the column.
    """
    blank_count = dataset[column_name].fillna('').apply(lambda x: x == '').sum()
    return blank_count


def remove_blanks(dataset, column_name):
    """
    Remove rows of a DataFrame with blank values from the specified column.

    Parameters:
    - dataset: DataFrame containing the data.
    - column_name: Name of the column to check for blanks.

    Returns:
    - DataFrame without rows containing blank values in the specified column.
    """
    data_without_blanks = dataset[dataset[column_name].notna()]
    data_without_blanks = data_without_blanks[data_without_blanks[column_name] != '']
    return data_without_blanks


def check_valid_expression(dataset, column_name):
    """
    Checks if the values in a column of a DataFrame are valid Python expressions.

    Args:
        dataset: The DataFrame containing the column.
        column_name: The name of the column to check.

    Returns:
        dict: A dictionary containing the count of valid and invalid expressions,
              along with a list of the invalid values.
    """
    valid_count = 0
    invalid_count = 0
    nan_count = 0
    blank_count = 0
    error_count = 0
    invalid_values = []
    error_values = []

    for value in dataset[column_name]:
        if pd.isna(value):
            invalid_count += 1
            nan_count += 1
        elif value == "":
            blank_count += 1
            invalid_count += 1
        else:
            try:
                ast.literal_eval(value)
                valid_count += 1
            except (SyntaxError, ValueError):
                invalid_count += 1
                error_count += 1
                error_values.append(value)

    return {
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'nan_count': nan_count,
        'blank_count': blank_count,
        'error_count': error_count,
        'invalid_values': invalid_values,
        'error_values': error_values
    }


def directories_duplicates(directories, keys, delete_duplicates=False, summary=False):
    """
    Check for duplicate directories.
    
    Parameters:
    - directories: A list with directories.
    - keys: A list of key to search for duplicated values.
    - delete_duplicates (optional): The option to delete duplicates.
    - summary (optional): The option to return a summary of the analysis.

    Returns:
        directories: A list with directories with or without duplicates.
        summary (optional): A summary of the performed analysis.
    """
        
    unique_files = []
    idx_duplicates = []
    #total_duplicates = 0

    if len(directories) > 1:
        for idx_directory, directory in enumerate(directories):
            if idx_directory == 0:
                # Add the 1st directory to start the comparison
                unique_files.append(directory)
            else:
                # Compare the directory to every unique directory
                is_duplicate = False
                for unique in unique_files:
                    # If all the values of the keys are the same, add idx_directory to idx_duplicates list
                    # Else add directory to unique_files list
                    try:
                        is_duplicate = all(directory.get(key) == unique.get(key) for key in keys)
                        if is_duplicate:
                            idx_duplicates.append(idx_directory)
                            break
                    except AttributeError:
                        pass
                
                if not is_duplicate:
                    unique_files.append(directory)        
        
        if delete_duplicates:
            # Delete directories using idx_duplicates list
            directories = [directory for idx, directory in enumerate(directories) if idx not in idx_duplicates]
    
    if summary:
        summary_txt = f"Total duplicates found: {len(idx_duplicates)}"
        if delete_duplicates:
            summary_txt += " Duplicates have been deleted."
        else:
            summary_txt += " Duplicates have not been deleted."

        return directories, summary_txt
    else:
        return directories


def extract_values(dataset, column_name, keys, new_columns):
    """
    Extract values from nested data.
    
    Parameters:
    - dataset: DataFrame containing the data.
    - column_name: Name of the column to extract the data.
    - keys: A list with the name of the keys.
    - new_columns: A list with the names of the new columns.

    Returns:
        dataset: DataFrame containing the data.
    """
    # Evaluating lenght of keys and new_columns lists
    if len(keys) != len(new_columns):
        raise ValueError("keys and new_columns length must be the same")

    # Createing new columns in the dataset using new_columns
    for column in new_columns:
        dataset[column] = pd.Series([], dtype='object')

    # Reading each value of the column
    for indx_column_name, value in dataset[column_name].items():
        # Evaluating the value of the column
        # value_evaluated = []
        try:
            value_evaluated = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass
        # Checking for duplicate values
        value_evaluated = directories_duplicates(value_evaluated, keys, True)

        extracted_values = {key: [] for key in keys}

        # Extracting items from dictionaries based on a key
        for item in value_evaluated:
            for key in keys:
                if item.get(key) is not None:
                    extracted_values[key].append(item.get(key))
                else:
                    extracted_values[key].append(None)

        # Going through every new column to store extracted values
        for indx_new_column, column in enumerate(new_columns):
            
            indx_extracted_values = keys[indx_new_column]
            
            if indx_extracted_values in extracted_values:
                # without assigning the values to a variable returns an error
                key_value = extracted_values[indx_extracted_values] 
            
            dataset.at[indx_column_name, column] = key_value
    
    return dataset


def extract_dict_values(dataset, column_name, keys, new_columns):
    """
    Extract values from a dictionary.
    
    Parameters:
    - dataset: DataFrame containing the data.
    - column_name: Name of the column to extract the data.
    - keys: A list with the name of the keys.
    - new_columns: A list with the names of the new columns.

    Returns:
        dataset: DataFrame containing the data.
    """
    if len(keys) != len(new_columns):
        raise ValueError("keys and new_columns length must be the same")

    for column in new_columns:
        dataset[column] = pd.Series([], dtype='object')

    for indx_column_name, value in dataset[column_name].items():
        value_evaluated = None

        try:
            value_evaluated = ast.literal_eval(value)
        except (ValueError, SyntaxError): 
            pass

        extracted_values = {key: [] for key in keys}
        keys_extracted = False

        if isinstance(value_evaluated, dict):
            for key in keys:
                if value_evaluated.get(key) is not None:
                    extracted_values[key].append(value_evaluated.get(key))
                    keys_extracted = True
                else:
                    extracted_values[key].append(None)

        if keys_extracted:
            for indx_new_column, column in enumerate(new_columns):
                indx_extracted_values = keys[indx_new_column]
                
                if indx_extracted_values in extracted_values:
                    key_value = extracted_values[indx_extracted_values]
                
                dataset.at[indx_column_name, column] = key_value
        else:
            for column in new_columns:
                dataset.at[indx_column_name, column] = None
    
    return dataset


def replace_nan_with_empty_string(dataset, column_name):
    """
    Replace NaN values with empty strings in a specific column of a DataFrame.

    Parameters:
    - dataset: The DataFrame containing the data.
    - column_name: The name of the column to replace NaN values.

    Returns:
    - None (modifies the DataFrame in-place).
    """
    dataset[column_name] = dataset[column_name].apply(lambda x: '' if pd.isna(x) and np.issubdtype(type(x), np.number) else x)
    return dataset


def get_column_summary(dataset, column_name):
    """
    Generates a summary of data types and their quantities in a column.

    Args:
        dataset: The DataFrame containing the column.
        column_name: The name of the column.

    Returns:
        A Series containing the data types as the index and their respective counts.
    """
    column_summary = dataset[column_name].apply(type).value_counts()
    return column_summary, "total values:", dataset.shape[0]

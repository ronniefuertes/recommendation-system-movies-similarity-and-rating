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


def get_column_summary(dataset, column_name):
    """
    Generates a summary of data types and their quantities in a column.

    Args:
        dataset: The DataFrame containing the column.
        column_name: The name of the column.

    Parameters:
        A Series containing the data types as the index and their respective counts.
    """
    column_summary = dataset[column_name].apply(type).value_counts()
    return column_summary, "total values:", dataset.shape[0]


def delete_rows(dataset, indices):
    """
    Deletes rows from a dataset based on the given list of indices.

    Parameters:
        dataset (list or pandas.DataFrame): The dataset from which rows will be deleted.
        indices (list): A list of indices corresponding to the rows to be deleted.

    Returns:
        list or pandas.DataFrame: The modified dataset with rows deleted.

    """
    # Loop through the indices in reverse order to avoid index shifting issues
    for index in sorted(indices, reverse=True):
        # Delete the row at the current index from the dataset
        del dataset[index]
    
    # Return the modified dataset
    return dataset

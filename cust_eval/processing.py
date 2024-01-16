import os
import pandas as pd
from lifetimes.utils import summary_data_from_transaction_data


def read_df(input_filepath):
    """
    Reads a .csv dataframe from filepath. Should have columns 'CustomerID', 'Timestamp' and 'PurchaseValue'.
    :param input_filepath: (Str) CSV filepath
    :return: pandas.dataframe
    """
    if not os.path.abspath(input_filepath):
        input_filepath = os.path.join(os.getcwd(), input_filepath)
    if not os.path.exists(input_filepath):
        print("No such input filename. Please check and try again.")
        return
    df = pd.read_csv(input_filepath)
    if("CustomerID" not in df.columns) or ("Timestamp" not in df.columns) or ("PurchaseValue" not in df.columns):
        print("CSV file should contain columns: 'CustomerID', 'Timestamp' and 'PurchaseValue'. Please check and try again.")
        return

    return df

def build_summary_from_df(df):
    """
    Builds a lifetimes.summary dataframe from an  input dataframe.
    :param df: pandas.dataframe. Should have columns 'CustomerID', 'Timestamp' and 'PurchaseValue'.
    :return: pandas.dataframe
    """
    summary = summary_data_from_transaction_data(df,
                                                 customer_id_col='CustomerID',
                                                 datetime_col='Timestamp',
                                                 monetary_value_col='PurchaseValue',
                                                 observation_period_end=max(df["Timestamp"]))
    return summary

def write_csv(output_filepath, df, suffix):
    """
    Writes a .csv to the file or folderpath
    :param output_filepath: (Str) filepath
    :param df: pandas.df
    :param suffix: (Str) either 'count.csv' or 'spend.csv'
    :return: none
    """
    if not os.path.abspath(output_filepath):
        output_filepath = os.path.join(os.getcwd(), output_filepath)
    if os.path.isdir(output_filepath):
        write_path = os.path.join(output_filepath, suffix)
    elif os.path.exists(output_filepath):
        print("Your chosen output file exists. Please check the path and try again.")
        return
    else:
        write_path = output_filepath
    df.to_csv(write_path, index=False)
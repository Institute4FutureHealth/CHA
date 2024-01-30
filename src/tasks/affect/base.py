"""
Affect - Base
"""
import os
from typing import List

import pandas as pd
import requests
from scipy.stats import linregress

from tasks.task import BaseTask


class Affect(BaseTask):
    """
    **Description:**

        This class is the base affect class for common methods and analysis.
    """

    def _get_data(
        self,
        local_dir: str,
        file_name: str,
        start_date: str,
        end_date: str = "",
        usecols: List[str] = None,
        date_column: str = "date",
    ) -> pd.DataFrame:
        local_dir = os.path.join(os.getcwd(), local_dir)
        if usecols is None:
            try:
                df = pd.read_csv(os.path.join(local_dir, file_name))
            except FileNotFoundError:
                return pd.DataFrame()
        else:
            try:
                df = pd.read_csv(
                    os.path.join(local_dir, file_name),
                    usecols=usecols,
                )
                df = df[usecols]
            except FileNotFoundError:
                return pd.DataFrame(columns=usecols)
        # Convert the "date" column to a datetime object with the format "YYYY-MM-DD"
        if date_column == "date":
            df[date_column] = pd.to_datetime(
                df[date_column], format="%Y-%m-%d"
            )
        else:
            df[date_column] = pd.to_datetime(
                df[date_column], unit="ms"
            )

        if end_date or end_date == start_date:
            # Filter the DataFrame to get the rows for the input dates (multiple dates)
            selected_rows = df[
                (
                    df[date_column]
                    >= pd.to_datetime(start_date, format="%Y-%m-%d")
                )
                & (
                    df[date_column]
                    <= pd.to_datetime(end_date, format="%Y-%m-%d")
                    + pd.Timedelta(days=1)
                )
            ]
        else:
            # Filter the DataFrame to get the rows for the input date (single dates)
            selected_rows = df[
                (
                    df[date_column]
                    == pd.to_datetime(start_date, format="%Y-%m-%d")
                )
            ]

        # Check if the input date exists in the DataFrame
        if selected_rows.empty:
            print(
                f"No data found between the date {start_date} and {end_date}."
            )
        return selected_rows

    def _download_data(
        self,
        local_dir: str = "data/affect",
        download_url: str = "https://www.example.com",
        file_name: str = "sleep.csv",
    ) -> str:
        local_dir = os.path.join(os.getcwd(), local_dir)
        # Create new directory if it is not there
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)

        # Get the data from the provided link
        response = requests.get(download_url, timeout=120)
        if response.status_code == 200:
            with open(
                os.path.join(local_dir, file_name), "wb"
            ) as file:
                file.write(response.content)
            return f"Downloaded {file_name} to {local_dir}."
        else:
            return (
                f"Failed to download {file_name} from {download_url}."
            )

    def _convert_seconds_to_minutes(
        self, df: pd.DataFrame, column_names: List[str]
    ) -> pd.DataFrame:
        for column_name in column_names:
            if column_name in df.columns:
                df[column_name] = df[column_name] / 60
        return df

    def _dataframe_to_string_output(self, df: pd.DataFrame) -> str:
        # Create a formatted string for each column and its corresponding value
        formatted_values = [
            f"{col} = {val}" for col, val in df.items()
        ]

        # Join the formatted values into a single string using a comma and space
        result_string = ", ".join(formatted_values)

        return result_string

    def _string_output_to_dataframe(
        self, input_string: str
    ) -> pd.DataFrame:
        # Split the input string into individual column-value pairs
        column_value_pairs = [
            pair.strip() for pair in input_string.split(",")
        ]
        # Create a dictionary to store column-value pairs
        data_dict = {}
        # Iterate through the pairs and extract column and value
        for pair in column_value_pairs:
            print("pair", pair)
            # Split each pair into column and value
            column, value = pair.split("=")
            # Strip any leading or trailing whitespaces
            column = column.strip()
            value = value.strip()
            # Add the column-value pair to the dictionary
            data_dict[column] = [value]
        # Create a DataFrame from the dictionary
        return pd.DataFrame(data_dict)

    def _calculate_slope(self, df: pd.DataFrame) -> pd.DataFrame:
        # Create a new DataFrame to store the slopes
        df_out = pd.DataFrame()
        # Iterate over columns
        columns_list = [
            col for col in df.columns if "date" not in col.lower()
        ]
        for column in columns_list:
            # Get the x values (dates) and y values (column values)
            # Convert date to numeric days
            x = pd.to_numeric(
                (df["date"] - df["date"].min())
                / pd.to_timedelta(1, unit="D")
            )
            y = df[column]
            # Calculate linear regression parameters
            slope, intercept, r_value, p_value, std_err = linregress(
                x, y
            )
            # Add the slope to the result DataFrame
            df_out[column] = [slope]
        return df_out

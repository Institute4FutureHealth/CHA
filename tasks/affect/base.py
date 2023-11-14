'''
Affect - Base
'''

import os
import pandas as pd
import requests
from tasks.task import BaseTask
from typing import List


class Affect(BaseTask):
    def _get_data(
            self,
            local_dir: str,
            file_name: str,
            start_date: str,
            end_date: str = "",
    ) -> pd.DataFrame:
        local_dir = os.path.join(os.getcwd(), local_dir)
        df = pd.read_csv(
            os.path.join(local_dir, file_name))
        # Convert the "date" column to a datetime object with the format "YYYY-MM-DD"
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

        if end_date:
            # Filter the DataFrame to get the rows for the input dates (multiple dates)
            selected_rows = df[(df['date'] >= pd.to_datetime(start_date, format='%Y-%m-%d')) & (
                df['date'] <= pd.to_datetime(end_date, format='%Y-%m-%d'))]
        else:
            # Filter the DataFrame to get the rows for the input date (single dates)
            selected_rows = df[(df['date'] == pd.to_datetime(start_date, format='%Y-%m-%d'))]

        # Check if the input date exists in the DataFrame
        if selected_rows.empty:
            return f"No data found between the date {start_date} and {end_date}."
        else:
            return selected_rows


    def _download_data(
            self,
            local_dir: str = 'data/affect',
            download_url: str = 'https://www.example.com',
            file_name: str = 'sleep.csv'
    ) -> str:
        local_dir = os.path.join(os.getcwd(), local_dir)
        # Create new directory if it is not there
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)

        # Get the data from the provided link
        response = requests.get(download_url, timeout=120)
        if response.status_code == 200:
            with open(os.path.join(local_dir, file_name), 'wb') as file:
                file.write(response.content)
            return f"Downloaded {file_name} to {local_dir}."
        else:
            return f"Failed to download {file_name} from {download_url}."


    def _convert_seconds_to_minutes(
            self,
            df: pd.DataFrame,
            column_names: List[str]
    ) -> pd.DataFrame:
        for column_name in column_names:
            if column_name in df.columns:
                df[column_name] = df[column_name] / 60
        return df


    def _dataframe_to_string_output(
            self,
            df: pd.DataFrame
    ) -> str:
        # Create a formatted string for each column and its corresponding value
        formatted_values = [f"{col} = {val}" for col, val in df.items()]

        # Join the formatted values into a single string using a comma and space
        result_string = ", ".join(formatted_values)

        return result_string

'''
Affect - Base
'''

import os
from typing import List
from datetime import datetime
import csv
import pandas as pd
from scipy.stats import linregress
import requests
from tasks.task import BaseTask
import pytz
import json


class Affect(BaseTask):
    def _get_data(
            self,
            local_dir: str,
            file_name: str,
            start_date: str,
            end_date: str = "",
            usecols: str = None,
    ) -> pd.DataFrame:
        local_dir = os.path.join(os.getcwd(), local_dir)
        if usecols is None:
            df = pd.read_csv(
                os.path.join(local_dir, file_name))
        else:
            df = pd.read_csv(os.path.join(local_dir, file_name),
                             usecols=usecols)
            df = df[usecols]
        # Convert the "date" column to a datetime object with the format "YYYY-MM-DD"
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

        if end_date or end_date == start_date:
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


    def _get_data_with_timestamp(
            self,
            local_dir: str,
            file_name: str,
            start_date: str,
            end_date: str = "",
    ) -> pd.DataFrame:
        local_dir = os.path.join(os.getcwd(), local_dir)

        # Convert start_date and end_date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        start_date = pytz.utc.localize(start_date)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            end_date = pytz.utc.localize(end_date)
        else:
            # Set the time to the last second of the day if there is no end_date
            end_date = start_date.replace(hour=23, minute=59, second=59)
        selected_rows = []
        # Open the CSV file and create a CSV reader
        with open(os.path.join(local_dir, file_name), 'r') as file:
            csv_reader = csv.DictReader(file)
            # Iterate through each row in the CSV file
            for row in csv_reader:
                # Convert the timestamp to a datetime object
                timestamp = datetime.strptime(datetime.fromtimestamp(
                    int(row['timestamp'])/1000).strftime(
                        '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                timestamp = pytz.utc.localize(timestamp)
                timestamp = timestamp.astimezone(pytz.timezone('America/Los_Angeles'))
                # Check if the timestamp is within the specified date range
                if start_date <= timestamp <= end_date:
                    selected_rows.append(row)
                elif timestamp > end_date:
                    # Break the loop if we've passed the end date
                    break
        # Convert the list of dictionaries to a DataFrame
        selected_df = pd.DataFrame(selected_rows)
        # Return the filtered DataFrame
        return selected_df


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


    def _string_output_to_dataframe(
            self,
            input_string: str
    ) -> pd.DataFrame:
        # Split the input string into individual column-value pairs
        column_value_pairs = [pair.strip() for pair in input_string.split(',')]
        # Create a dictionary to store column-value pairs
        data_dict = {}
        # Iterate through the pairs and extract column and value
        for pair in column_value_pairs:
            print("pair", pair)
            # Split each pair into column and value
            column, value = pair.split('=')
            # Strip any leading or trailing whitespaces
            column = column.strip()
            value = value.strip()
            # Add the column-value pair to the dictionary
            data_dict[column] = [value]
        # Create a DataFrame from the dictionary
        return pd.DataFrame(data_dict)


    def _calculate_slope(
            self,
            df: pd.DataFrame
    ) -> pd.DataFrame:
        # Create a new DataFrame to store the slopes
        df_out = pd.DataFrame()
        # Iterate over columns
        columns_list = [col for col in df.columns if 'date' not in col.lower()]
        for column in columns_list:
            # Get the x values (dates) and y values (column values)
            # Convert date to numeric days
            x = pd.to_numeric((
                df['date'] - df['date'].min()) / pd.to_timedelta(1, unit='D'))
            y = df[column]
            # Calculate linear regression parameters
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            # Add the slope to the result DataFrame
            df_out[column] = [slope]
        return df_out


    def _split_dataframe_by_time(
            self,
            df: pd.DataFrame,
            sampling_frequency: int,
            window_length: int = 5,
    ) -> List:
        # Ensure the 'timestamp' column is of datetime type
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize(
            'UTC').dt.tz_convert('America/Los_Angeles')
        # Group by 5-minute intervals and convert to a list of DataFrames
        chunks = [group for name, group in df.groupby(
            pd.Grouper(key='timestamp', freq='5min'))]
        err_rate = 0.95
        chunks_filtered = [sublist for sublist in chunks if len(
            sublist) > window_length*60*sampling_frequency*err_rate]
        return chunks_filtered


    def _ppg_dataframes_and_fs_to_json(
            self,
            dataframes_list: List[pd.DataFrame],
            sampling_frequency: int,
    ) -> str:
        # PPG
        json_dict = {}
        for i, df in enumerate(dataframes_list):
            key = f'df_{i}'
            json_dict[key] = df.to_json(orient='records')

        # Sampling frequency
        int_dict = {'value': sampling_frequency}

        # Combine both into a single dictionary
        combined_dict = {'ppg': json_dict, 'sampling_frequency': int_dict}
        # Convert the combined dictionary to JSON
        json_out = json.dumps(combined_dict)
        return json_out


    def _json_to_ppg_dataframes_and_fs(
            self,
            json_data: str
    ):
        # Load the JSON data
        combined_dict = json.loads(json_data)

        # Extract the dataframe JSONs and the value from the combined dictionary
        df_json = combined_dict.get('ppg', {})
        int_dict = combined_dict.get('sampling_frequency', {})

        # Initialize lists to store dataframes
        ppg_dataframes_list = []

        # Iterate through dataframe JSONs and convert them back to dataframes
        for _, df_json_str in df_json.items():
            df = pd.read_json(df_json_str, orient='records')
            ppg_dataframes_list.append(df)

        return ppg_dataframes_list, int_dict['value']

import pandas as pd
import json
import re


def load_data():
    df = pd.read_csv('../data/raw_data/vegan_recipes.csv')
    return df


def delete_columns(df):
    # Delete unnecessary columns:
    df = df.drop(
        columns=['collection', 'recipie_collection_idx', 'descripition', 'Neutretion'])
    return df


'''
Replace single quote with double quote, so json.loads() could make a direct conversion of a string representation of list into list in Python. 
This is required for further conversion of the data frame into JSON file.
'''


def replace_single_quote_with_double_quote(df):
    col_list = ['ingredients', 'steps']
    df[col_list] = df[col_list].replace({'\'': '"'}, regex=True)
    return df


def convert_str_to_list(df):
    # Convert string representation of list into list in Python.
    df['steps'] = df['steps'].apply(json.loads)
    df['ingredients'] = df['ingredients'].apply(json.loads)
    return df


def check_for_nan(df):
    # Check for Nan
    column_nan_count = df.isnull().sum()
    print("NaN count per column:")
    print(column_nan_count)

    null_mask = df.isnull().any(axis=1)
    null_rows = df[null_mask]
    print("Null rows:")
    print(null_rows)


def split_steps(step_list):
    # Split 'steps' into more number of items, to avoid too long steps in one line. + lstrip() each step line.
    # Function to split sentences while preserving the list structure

    result = []
    for step in step_list:
        # Split using regex that looks for a period followed by a space and an uppercase letter
        split_text = re.split(r'(?<=\.)\s+(?=[A-Z])', step.lstrip())
        result.extend(split_text)
    return result


def save_to_csv(df):
    # Save cleaned data
    df.to_csv('../data/prepared_data/cleaned_vegan_recipes_data.csv', index=False)


if __name__ == "__main__":
    df = load_data()
    df = delete_columns(df)
    df = replace_single_quote_with_double_quote(df)
    df = convert_str_to_list(df)

    df['steps'] = df['steps'].apply(split_steps)
    save_to_csv(df)

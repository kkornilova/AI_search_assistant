import pandas as pd
from bs4 import BeautifulSoup
import requests
import random
import time


def load_data():
    df = pd.read_csv('../data/raw_data/recipes_data.csv')
    return df


def delete_columns(df):
    # Delete unnecessary columns:
    df.drop(columns=['source', 'NER'])
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


'''
There are no recipes images_url in this dataset, so we need to scrape them from the Web using BeautifulSoup. 
The existing links are not in the correct format.
'''


def get_random_row(df, column, value):
    filtered_df = df[df[column] == value]  # Filter the DataFrame
    # Return a random row
    return filtered_df.sample(n=1) if not filtered_df.empty else None


def get_random_links(site_list):
    site_links = []
    for site in site_list:
        # Get a random row where for each site
        random_row = get_random_row(df, 'site', site)
        site_links.append(random_row['link'].item())

    return site_links


def normalize_urls(df, column):
    def modify_url(url):
        if url.startswith('www.'):
            return 'http://' + url[4:]
        elif not url.startswith('http://'):
            return 'http://' + url
        return url

    df[column] = df[column].apply(modify_url)
    return df


def add_image_column(df):
    df['image'] = pd.Series(dtype='object')
    return df


sites_for_scraping = ['www.food.com', 'food52.com']


def get_link_for_scraping():
    site = random.choice(sites_for_scraping)

    # Filter DataFrame for rows matching the site and missing images
    filtered_df = df[(df['site'] == site) & (df['image'].isna())]

    if filtered_df.empty:
        print(f"No rows found for site: {site} with missing images.")
        return df

    # Pick a random row
    row = filtered_df.sample(n=1).iloc[0]
    link = row['link']

    return link, row


def extract_image_link(link, response):
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        if 'food52' in link:
            img_tag = soup.find("picture")
            img_link = soup.find("img")['data-pin-media']
            return img_link

        else:
            img_tag = soup.find("div", class_="primary-image")
            img_link = soup.find("img")['src']
            return img_link
    except:
        print(f"Wrong tag")


def request_site_html(link):
    try:
        response = requests.get(link, timeout=5)

        if response.ok:
            try:
                image_link = extract_image_link(link, response)
                return image_link
            except:
                print("Oops")

    except requests.RequestException as e:
        print(f"Error fetching {link}: {e}")


def save_image_link_to_df(image_link, row):

    try:
        df.at[row.name, 'image'] = image_link
        print(f"Saved image for {image_link}: {image_link}")
    except:
        print("Nothing to save")


def save_to_csv(df):
    # Save cleaned data
    df.to_csv('../data/prepared_data/recipes_data_with_images.csv', index=False)


if __name__ == "__main__":
    df = load_data()
    df = delete_columns(df)
    df = normalize_urls(df, 'link')
    df = add_image_column(df)

    for _ in range(100):
        link_for_scrap, df_row = get_link_for_scraping()
        image_link = request_site_html(link_for_scrap)
        save_image_link_to_df(image_link, df_row)
        print(f"New link: {link_for_scrap}")
    print(f"Final link stored: {link_for_scrap}")

    save_to_csv(df)

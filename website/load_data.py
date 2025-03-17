from elasticsearch import helpers
import pandas as pd
from sentence_transformers import SentenceTransformer
from .elasticsearch_connection import get_elasticsearch_client


def create_es_index(es_client, index_name):
    index_mapping = {
        "properties": {
            "recipe_name": {
                "type": "text"},
            "ingredients": {
                "type": "text"},
            "steps": {
                "type": "text"},
            "image": {
                "type": "text"},
            "recipe_name_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True},
            "ingredients_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True}
        }
    }
    if es_client.indices.exists(index=index_name):
        print(f"Index {index_name} already exists.")
    else:
        es_client.indices.create(index=index_name, mappings=index_mapping)

    print(f"Index {index_name} has been created.")


# Prepare datasets
vegan_recipes_data = "website/data/prepared_data/cleaned_vegan_recipes_data.csv"
recipes_big_dataset = 'website/data/prepared_data/recipes_data_with_images.csv'


def read_vegan_data(file_name):
    df_vegan = pd.read_csv(file_name, dtype='object')
    df_vegan.rename(columns={'name': 'recipe_name'}, inplace=True)
    return df_vegan


def read_big_recipes_data(file_name):
    df_big_dataset = pd.read_csv(file_name, dtype='object')
    df_big_dataset = df_big_dataset.drop(columns=['link', 'site'])
    df_big_dataset.rename(
        columns={'title': 'recipe_name', 'directions': 'steps'}, inplace=True)
    return df_big_dataset


def slice_big_dataset(df_big_dataset):
    df_with_images = df_big_dataset[df_big_dataset['image'].notnull()]
    df_without_images = df_big_dataset[df_big_dataset['image'].isnull()]

    df_without_images = df_without_images.sample(
        frac=1, random_state=42).reset_index(drop=True)
    df_big_dataset_slice = pd.concat(
        [df_with_images, df_without_images.iloc[0:2000]], ignore_index=True)
    return df_big_dataset_slice


def combine_datasets_to_one_df(df_vegan, df_big_dataset_slice):
    cols = ['recipe_name', 'ingredients', 'steps', 'image']

    df_vegan = df_vegan.reindex(columns=cols)
    df_big_dataset_slice = df_big_dataset_slice.reindex(columns=cols)

    df_combined = pd.concat(
        [df_vegan, df_big_dataset_slice], ignore_index=True)
    df_combined = df_combined.sample(
        frac=1, random_state=42).reset_index(drop=True)
    df_combined.fillna("None", inplace=True)

    return df_combined


def add_vector_columns(model, df):
    df['recipe_name_vector'] = df['recipe_name'].apply(
        lambda x: model.encode(x))
    df['ingredients_vector'] = df['ingredients'].apply(
        lambda x: model.encode(x))

    records = df.to_dict('records')  # return list of dicts
    return records


def dict_to_elastic(records, index_name, es):

    actions = [
        {
            "_index": index_name,
            "_source": doc
        }
        for doc in records
    ]

    # returns a tuple with summary information - number of successfully executed actions and either list of errors or number of errors
    print(helpers.bulk(es, actions))


def main():
    """Main function to set up Elasticsearch and load data."""

    es = get_elasticsearch_client()
    client_info = es.info()
    print('Connected to Elasticsearch')
    print(client_info.body)

    index_name = 'recipes'

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    create_es_index(es, index_name)
    df_vegan = read_vegan_data(vegan_recipes_data)
    df_big_dataset = read_big_recipes_data(recipes_big_dataset)
    df_big_dataset_slice = slice_big_dataset(df_big_dataset)
    df_combined = combine_datasets_to_one_df(df_vegan, df_big_dataset_slice)
    records = add_vector_columns(model, df_combined)
    dict_to_elastic(records, index_name, es)

    print("Data loaded to Elasticsearch successfully!")


if __name__ == "__main__":
    main()

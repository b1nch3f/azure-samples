import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]


def get_embeddings(text: str):
    # There are a few ways to get embeddings. This is just one example.
    import openai

    open_ai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    open_ai_key = os.getenv("AZURE_OPENAI_API_KEY")

    client = openai.AzureOpenAI(
        azure_endpoint=open_ai_endpoint,
        api_key=open_ai_key,
        api_version="2023-05-15",
    )
    embedding = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return embedding.data[0].embedding


def get_index(name: str):
    from azure.search.documents.indexes.models import (
        SearchIndex,
        SearchField,
        SearchFieldDataType,
        SimpleField,
        SearchableField,
        VectorSearch,
        VectorSearchProfile,
        HnswAlgorithmConfiguration,
    )

    fields = [
        SimpleField(name="chunkId", type=SearchFieldDataType.String, key=True),
        SearchableField(
            name="parentDoc",
            type=SearchFieldDataType.String,
            sortable=True,
            filterable=True,
            facetable=True,
        ),
        SearchableField(name="chunk", type=SearchFieldDataType.String),
        SearchField(
            name="chunkVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="my-vector-config",
        ),
    ]
    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="my-vector-config",
                algorithm_configuration_name="my-algorithms-config",
            )
        ],
        algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config")],
    )
    return SearchIndex(name=name, fields=fields, vector_search=vector_search)


if __name__ == "__main__":
    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(service_endpoint, credential)
    index = get_index(index_name)
    index_client.create_or_update_index(index)

    # Delete Index
    # index_client.delete_index(index_name)

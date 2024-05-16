from algoliasearch.search_client import SearchClient

client = SearchClient.create("8SYE9PPQXH", "320f3dea5088a0f273a764527b790978")
vocab_index = client.init_index("vocab_en_vi")
settings = {"searchableAttributes": ["word", "translation"]}
vocab_index.set_settings(settings)

# User index
user_index = client.init_index("users")


def autocomplete(text):
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Auto complete search for English words with prefix matching.
    """
    try:
        results = vocab_index.search(
            text,
            {
                "attributesToRetrieve": ["word", "translation"],
                "hitsPerPage": 5,
                "restrictSearchableAttributes": ["word"],
            },
        )
        return results
    except Exception as e:
        raise e


def save_to_algolia(index, data):
    """
    * Author: Phan Van Tai, created at: 16/05/2024
    Save data to Algolia index
    """
    try:
        vocab_index = client.init_index(index)
        vocab_index.save_object(data)
        print(f"Saved to Algolia: {data}")
    except Exception as e:
        print(f"Failed to save to Algolia: {str(e)}")


def get_user_by_query(query):
    search_result = user_index.search(
        query,
        {
            "attributesToRetrieve": ["display_name", "email"],
            "hitsPerPage": 5,
            "attributesToHighlight": [
                "picture"
            ],  # Bổ sung trường 'picture' để nó được trả về
        },
    )

    hits = search_result["hits"]
    results = [
        {
            "email": hit["email"],
            "display_name": hit["display_name"],
            "picture": hit.get("_highlightResult", {})
            .get("picture", {})
            .get("value", ""),
        }
        for hit in hits
    ]
    return results

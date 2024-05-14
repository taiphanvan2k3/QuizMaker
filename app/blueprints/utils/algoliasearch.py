from algoliasearch.search_client import SearchClient

client = SearchClient.create("8SYE9PPQXH", "320f3dea5088a0f273a764527b790978")
algolia_index = client.init_index("vocab_en_vi")
settings = {
    'searchableAttributes': ['word', 'translation']
}
algolia_index.set_settings(settings)

def autocomplete(text):
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Auto complete search for English words with prefix matching.
    """
    try:
        results = algolia_index.search(text, {
            'attributesToRetrieve': ['word', 'translation'],
            'hitsPerPage': 5,
            'restrictSearchableAttributes': ['word']
        })
        return results
    except Exception as e:
        raise e
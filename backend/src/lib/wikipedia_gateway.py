import requests


class WikipediaGateway:
    def __init__(self):
        self.session = requests.Session()

    def wiki_to_wikibase_item(self, wiki_link):
        """
        Obtain WikiBase entity ID from Wikipedia link.
        Return first of redirects found, so it does not necessary return 'expected' results.

        Input string should be in format like '/wiki/Paris'
        """
        if not wiki_link.startswith('/wiki/'):
            return ""
        wiki_title = wiki_link.split('/', 2)[2]
        result = self.session.get(f'https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&titles={wiki_title}&format=json')
        pages = result.json()['query']['pages']
        results = []
        for p in pages:
            results.append(pages[p]['pageprops']['wikibase_item'])

        # Assuming that first wiki page will lead to correct entity
        return results[0] if results else ""
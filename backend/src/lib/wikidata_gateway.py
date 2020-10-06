import sys
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT_URL = "https://query.wikidata.org/sparql"


class WikiDataGateway:
    """
    Wrapper for running SPARQL queries on wikidata.org.
    Based on the documentation and examples from:
    https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/Wikidata_Query_Help
    """
    def __init__(self, endpoint_url=ENDPOINT_URL):
        self.endpoint_url = endpoint_url
        self.user_agent = "MuseumDB/1.0 (https://github.com/xhresko/museumdb/) wikidata_gateway/1.0 Python/{}.{}" \
                     "".format(sys.version_info[0], sys.version_info[1])
        self.sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)

    def get_results(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()

    def get_all_cities_name_and_population(self):
        query_cities_population = """
        SELECT DISTINCT ?cityLabel ?population
        WHERE
        {
          ?city wdt:P31/wdt:P279* wd:Q515 .
          ?city wdt:P1082 ?population .
          SERVICE wikibase:label {
            bd:serviceParam wikibase:language "en" .
          }
        }
        ORDER BY DESC(?population)"""

        query_result = self.get_results(query_cities_population)
        result = dict()
        for detail in query_result["results"]["bindings"]:
            city_name = detail['cityLabel']['value']
            if city_name not in result:
                result[city_name] = detail['population']['value']
        return result

    def get_all_countries_name_and_population(self):
        query_countries_population = """
        SELECT DISTINCT ?countryLabel ?population
        {
          ?country wdt:P31 wd:Q3624078 ;
           wdt:P1082 ?population .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
        }
        ORDER BY DESC(?population)"""

        query_result = self.get_results(query_countries_population)
        result = dict()
        for detail in query_result["results"]["bindings"]:
            country_name = detail['countryLabel']['value']
            if country_name not in result:
                result[country_name] = detail['population']['value']
        return result

    def get_museum_types_by_name(self, museum_name):
        query_types = f"""
        SELECT DISTINCT ?item ?itemLabel ?class ?classLabel
        WHERE
        {{
          ?item wdt:P31/wdt:P279* ?class .
          ?article schema:about ?item .
          ?article schema:isPartOf <https://en.wikipedia.org/>;
           schema:name "{museum_name}"@en ;.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
        }}"""
        query_result = self.get_results(query_types)
        result = set()
        for detail in query_result["results"]["bindings"]:
            result.add(detail['classLabel']['value'])
        return result

    def get_country_population_by_name(self, country_name):
        country_population_query = f"""
        SELECT DISTINCT ?countryLabel ?population ?article
        {{
          ?article schema:about ?country .
          ?article schema:isPartOf <https://en.wikipedia.org/>;
               schema:name "{country_name}"@en ;.
          ?country wdt:P31 wd:Q3624078 ;
               wdt:P1082 ?population .
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
        }}
        ORDER BY DESC(?population)"""
        query_result = self.get_results(country_population_query)
        result = list()
        for detail in query_result["results"]["bindings"]:
            result.append(detail['population']['value'])
        return result

    def get_population_by_entity(self, wikidata_entity):
        population_query = f"""
        SELECT
        DISTINCT ?population
        {{
            wd:{wikidata_entity} wdt:P1082 ?population.
        }}
        ORDER
        BY
        DESC(?population)
        """
        query_result = self.get_results(population_query)
        for detail in query_result['results']['bindings']:
            return int(detail['population']['value'])
        return None

    def get_wiki_languages_by_entity(self, wikidata_entity):
        wiki_referenced_query = f"""
        SELECT
        DISTINCT ?wiki
        WHERE
        {{
        ?article schema:about wd:{wikidata_entity};
        schema:isPartOf ?wiki.
        }}
        """

        query_result = self.get_results(wiki_referenced_query)
        result = []
        for detail in query_result['results']['bindings']:
            result.append(detail['wiki']['value'])
        return result

    def get_continent_by_entity(self, wikidata_entity):
        continent_query = f"""
        SELECT
        DISTINCT ?continent ?continentLabel
        WHERE
        {{
            wd:{wikidata_entity} wdt:P30 ?continent.
            SERVICE wikibase:label {{bd:serviceParam wikibase:language "en"}}
        }}
        ORDER BY ASC(?continentLabel)"""
        query_result = self.get_results(continent_query)
        for detail in query_result['results']['bindings']:
            return detail['continentLabel']['value']
        return ""

    def get_museum_types_by_entity(self, wikidata_entity):
        museum_type_query = f"""
        SELECT DISTINCT ?class ?classLabel
        WHERE
        {{
          wd:{wikidata_entity} wdt:P31/wdt:P279* ?class.
          ?class wdt:P279* wd:Q33506.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
        }}"""
        result = []
        query_result = self.get_results(museum_type_query)

        for detail in query_result['results']['bindings']:
            result.append(detail['classLabel']['value'])
        return result

import bs4 as bs
import pandas as pd
import requests
import re
import logging

logger = logging.getLogger(__name__)

from lib.wikidata_gateway import WikiDataGateway
from lib.wikipedia_gateway import WikipediaGateway

BASE_HEADER = ['Museum',
               'Museum Wiki',
               'Museum Wikidata ID',
               'Country',
               'Country Wiki',
               'Country Wikidata ID',
               'City',
               'City Wiki',
               'City Wikidata ID',
               'Visitors per year']

def generate_museum_db_to_csv(csv_file_path):
    generate_full_museum_df().to_csv(csv_file_path)

def generate_full_museum_df():
    base_df = get_most_visited_museums_in_df()
    return get_enriched_museum_df(base_df)

def get_enriched_museum_df(df):
    """
    Add more details into dataframe with most visited museums and return new dataframe.
    Expected is header defined in BASE_HEADER constant of this module.
    """
    wd_gateway = WikiDataGateway()
    result = df.copy()
    logger.info('Reading cities population from WikiData.')
    result['City population'] = result.apply(lambda row: int(wd_gateway.get_population_by_entity(row['City Wikidata ID'])), axis=1)
    logger.info('Reading countries population from WikiData.')
    result['Country population'] = result.apply(lambda row: int(wd_gateway.get_population_by_entity(row['Country Wikidata ID'])), axis=1)
    logger.info('Reading wiki languages used from WikiData.')
    result['Wiki languages count'] = result.apply(lambda row: len(wd_gateway.get_wiki_languages_by_entity(row['Museum Wikidata ID'])), axis=1)
    logger.info('Reading continents from WikiData.')
    result['Continent'] = result.apply(lambda row: wd_gateway.get_continent_by_entity(row['City Wikidata ID']) or
                                               wd_gateway.get_continent_by_entity(row['Country Wikidata ID']),
                                   axis=1)
    logger.info('Reading museum types from WikiData.')
    result['Museum types'] = result.apply(lambda row: ", ".join(wd_gateway.get_museum_types_by_entity(row['Museum Wikidata ID'])),
                                      axis=1)
    result['Art/culture museum'] = result.apply(
        lambda row: 'art museum' in row['Museum types'] or 'museum of culture' in row['Museum types'],
        axis=1)

    return result


def get_most_visited_museums_in_df():
    """
    Parse data from table on list of most visited museums on english wikipedia
    and return it as a DataFrame.

    Assumes a lot about formatting of the page and the table so it can easily get outdated.
    """
    museum_url = 'https://en.wikipedia.org/wiki/List_of_most-visited_museums'
    logger.info(f'Reading content of URL ({museum_url}) to parse list of museums')
    wg = WikipediaGateway()
    article = requests.get(museum_url)
    soup = bs.BeautifulSoup(article.content, 'lxml')

    # Assuming the table will be the first on the page
    parsed_table = soup.find_all('table')[0]

    data = list()


    for row in parsed_table.find_all('tr')[1:]:  # Ignore the header
        name_cell, place_cell, visitor_cell, _ = row.find_all('td')

        museum_wiki = name_cell.a.get('href')
        museum = re.sub(r'\[[^\[]*\]', '', name_cell.get_text())
        museum_wikibase = wg.wiki_to_wikibase_item(museum_wiki)

        place_links = place_cell.find_all('a')

        country_wiki = place_links[0].get('href')
        country = place_links[0].get('title')
        country_wikibase = wg.wiki_to_wikibase_item(country_wiki)

        city_wiki = place_links[1].get('href')
        city = place_links[1].get('title')
        city_wikibase = wg.wiki_to_wikibase_item(city_wiki)

        visitors = int(visitor_cell.get_text().replace(',', ''))

        data.append([museum, museum_wiki, museum_wikibase,
                     country, country_wiki, country_wikibase,
                     city, city_wiki, city_wikibase, visitors])
    return pd.DataFrame(data, columns=BASE_HEADER)

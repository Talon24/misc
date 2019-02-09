"""Get media in which specified actors worked together. Uses IMDB"""

import argparse
import functools

import requests
import bs4 as bs

def find_media(urls):
    """
    Get all media in which an actor participated and
    return the intersection of all. Also get actor names.
    Args:
        urls: Iterable of URLs that direct to IMDB imdb.com/name/ pages
    Returns:
        actor_names: List of Actor Names taken from the url
        intersecion: Set of Media in which all actors participated
    """
    media_sets = []
    actor_names = []
    for url in urls:
        text = requests.get(url).text
        soup = bs.BeautifulSoup(text, "lxml")
        actor_names.append(soup.find("span", class_="itemprop").text)
        rows = soup.find_all("div", class_="filmo-row")
        media = {row.find("a").text for row in rows}
        media_sets.append(media)

    intersection = functools.reduce(set.intersection, media_sets)
    return actor_names, intersection

def main():
    """get arguments, execute, print"""
    urls = ["https://www.imdb.com/name/nm0354937/", # Jennifer Hale
            "https://www.imdb.com/name/nm1035752/"] # Mark Meer
    # ^ Default values

    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="*", default=urls, help="List of IMDB "
                        "urls or keys (after /name/ in the url) to process")
    arg = parser.parse_args()
    arg.urls[:] = ["https://www.imdb.com/name/" + url
                   if not url.startswith("http") else url
                   for url in arg.urls]
    actors, media = find_media(arg.urls)
    print("--- Media in which {} cooperated:".format(" and ".join(actors)))
    for medium in sorted(media):
        print(medium)

if __name__ == '__main__':
    main()

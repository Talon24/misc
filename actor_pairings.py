"""media where 2 actors or voice actors participated together. uses imdb links"""

import argparse
import functools

import requests
import bs4 as bs
# import ipdb

def main():
    """main"""
    urls = ["https://www.imdb.com/name/nm0354937/", # Jennifer Hale
            "https://www.imdb.com/name/nm1035752/"] # Mark Meer

    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="*", default=urls, help="List of imbd urls"
                        " or keys (after /name/ in the url) to process")
    arg = parser.parse_args()
    arg.urls[:] = ["https://www.imdb.com/name/" + url
                   if not url.startswith("http") else url
                   for url in arg.urls]

    media_sets = []
    actor_names = []
    for url in arg.urls:
        text = requests.get(url).text
        soup = bs.BeautifulSoup(text, "lxml")
        actor_names.append(soup.find("span", class_="itemprop").text)
        rows = soup.find_all("div", class_="filmo-row")
        media = {row.find("a").text for row in rows}
        media_sets.append(media)

    actors = " and ".join(actor_names)
    print("--- Media in which {} cooperated:".format(actors))
    intersection = functools.reduce(set.intersection, media_sets)
    # intersection = media_sets[0].intersection(media_sets[1])
    for medium in sorted(intersection):
        print(medium)

if __name__ == '__main__':
    main()

import csv
import html
import requests
from bs4 import BeautifulSoup



def get_soup(url):
    """
    
    """
    response = requests.get(url)
    html_ = html.unescape(response.text)
    return BeautifulSoup(html_, "html.parser")


def write_csv(file, named_indexes):
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile, #delimiter='\t'
            )
            writer.writerow(['idx','name'])
            
            for row in named_indexes:
                writer.writerow(row)



class NamesParser:
    """
    
    """
    def __init__(self, url, lang, **kwargs):
        """
        
        """
        self.url = url
        self.lang = lang
        self.soup = get_soup(url)
        self.named_indexes = self.get_named_indexes()

        self.kwargs = kwargs


    def get_named_indexes(self):
        """
        
        """
        pokemon_htmls = self.soup.find_all('tr', style='background:#FFF')

        named_indexes = []
        for pokemon_html in pokemon_htmls:

            if self.lang == 'en':
                idx_name = self._en_parser(pokemon_html)
            elif self.lang == 'zh':
                idx_name = self._zh_parser(pokemon_html, **self.kwargs)
            else:
                idx_name = self._default_parser(pokemon_html, lang=self.lang)

            idx, name = idx_name
            idx = self._clean_idx(idx)

            named_indexes.append((idx, name))

        return named_indexes


    def to_csv(self, file):
        write_csv(file, self.named_indexes)


    @staticmethod
    def _clean_idx(idx):
        try:
            return str(int(idx.replace('#', ''))).zfill(3)
        except:
            return "???"

    
    @staticmethod
    def _en_parser(pokemon_html):
        idx  = pokemon_html.find_all('td')[1].text.strip()
        name = pokemon_html.find_all('td')[2].text.strip()
        return idx, name

    @staticmethod
    def _zh_parser(pokemon_html, simplified=True, **kwargs):
        idx  = pokemon_html.td.text.strip()

        if simplified:
            name = pokemon_html.find_all('td', lang='zh')[1].text.strip()
        else:
            name = pokemon_html.find_all('td', lang='zh')[0].text.strip()
        return idx, name

    @staticmethod
    def _default_parser(pokemon_html, lang):
        idx  = pokemon_html.td.text.strip()
        name = pokemon_html.find('td', lang=lang).text.strip()
        return idx, name





if __name__ == '__main__':

    lang_mapping = {
        'en': 'English',
        'ko': 'Korean',
        'de': 'German',
        'ja': 'Japanese',
        'fr': 'French',
        'ru': 'Russian',
        'th': 'Thai',
    }

    base_source_url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_{}_Pok%C3%A9mon_names'
    base_out_path   = '/home/jayckaiser/code/korean-pokemon/korean-pokemon/names/{}.txt'

    for lang_code, lang in lang_mapping.items():

        source_url = base_source_url.format(lang)
        out_path = base_out_path.format(lang_code)

        pokemon_names = NamesParser(source_url, lang=lang_code)
        pokemon_names.to_csv(out_path)

        print(f"Wrote out Pokemon names for {lang}.")

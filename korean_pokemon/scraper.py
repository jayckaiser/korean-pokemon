import csv
import html
import requests
import time

from bs4 import BeautifulSoup



class LanguagePokemonScraper:
    """
    
    """
    def __init__(self, url, lang, **kwargs):
        """
        
        """
        self.url = url
        self.lang = lang
        self.kwargs = kwargs

        self.soup = self.get_soup(url)
        self.lang_tuples = self.get_lang_tuples()



    @staticmethod
    def get_pokemon_htmls(soup):
        return soup.find_all('tr', style='background:#FFF')


    @staticmethod
    def parse_pokemon_html(pokemon_html, lang):
        idx  = pokemon_html.td.text.strip()
        name = pokemon_html.find('td', lang=lang).text.strip()
        return idx, name


    
    @staticmethod
    def get_soup(url):
        """
        
        """
        response = requests.get(url)
        html_ = html.unescape(response.text)
        time.sleep(1)
        return BeautifulSoup(html_, "html.parser")


    def get_lang_tuples(self):
        """
        
        """
        pokemon_htmls = self.get_pokemon_htmls(self.soup)

        lang_tuples = []
        for pokemon_html in pokemon_htmls:
            idx, name = self.parse_pokemon_html(pokemon_html, lang=self.lang)
            idx = self._clean_idx(idx)

            lang_tuples.append((idx, name))

        return dict(lang_tuples)


    @staticmethod
    def _clean_idx(idx):
        try:
            return str(int(idx.replace('#', ''))).zfill(3)
        except:
            return "???"


    def to_csv(self, file):
        """
        
        """
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile, #delimiter='\t'
            )
            writer.writerow(['idx','name'])
            
            for row in self.lang_tuples.items():
                writer.writerow(row)

        print(f"Wrote CSV file to `{file}`.")





class EnglishPokemonScraper(LanguagePokemonScraper):
    """
    
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @staticmethod
    def parse_pokemon_html(pokemon_html, **kwargs):
        idx  = pokemon_html.find_all('td')[1].text.strip()
        name = pokemon_html.find_all('td')[2].text.strip()
        return idx, name

    


class ChinesePokemonScraper(LanguagePokemonScraper):
    """
    
    """
    def __init__(self, *args, simplified=True, **kwargs):
        self.simplified=simplified
        super().__init__(*args, **kwargs)

    
    def parse_pokemon_html(self, pokemon_html, **kwargs):
        idx  = pokemon_html.td.text.strip()

        if self.simplified:
            name = pokemon_html.find_all('td', lang='zh')[1].text.strip()
        else:
            name = pokemon_html.find_all('td', lang='zh')[0].text.strip()

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
        'zh': 'Chinese',
    }


    base_source_url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_{}_Pok%C3%A9mon_names'
    base_out_path   = '/home/jayckaiser/code/korean-pokemon/korean_pokemon/names/{}.txt'

    for lang_code, lang in lang_mapping.items():

        source_url = base_source_url.format(lang)
        out_path = base_out_path.format(lang_code)

        if lang_code == 'en':
            pokemon_names = EnglishPokemonScraper(source_url, lang=lang_code)

        elif lang_code == 'zh':
            pokemon_names = ChinesePokemonScraper(source_url, lang=lang_code, simplified=True)

        else:
            pokemon_names = LanguagePokemonScraper(source_url, lang=lang_code)
        
        pokemon_names.to_csv(out_path)
        print(f"Wrote out Pokemon names for {lang}.")

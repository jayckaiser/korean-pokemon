import csv
import os
import re

from collections import defaultdict
from pathlib import Path




class Pokedex:
    """
    
    """
    def __init__(self, lang_dir, image_dir, remove_unknown=True):
        self.languages = self.get_lang_mappings(lang_dir)
        self.images    = self.get_image_mapping(image_dir)

        self.pokemons = self.build_pokemons()

        if remove_unknown:
            self.pokemons = self.filter_unknown(self.pokemons)



    def build_pokemons(self):
        """
        
        """
        pokemons = defaultdict(dict)

        for idx, image in self.images.items():
            pokemons[idx]['image'] = image

        for lang_code, lang_mapping in self.languages.items():
            for idx, name in lang_mapping.items():
                pokemons[idx][lang_code] = name

        return pokemons


    def get_lang_mappings(self, dir):
        """
        
        """
        lang_mappings = {}

        for lang_file in os.listdir(dir):
            lang_path = os.path.join(dir, lang_file)
            mapping = self.parse_lang_mapping_file(lang_path)
            lang_code = Path(lang_file).stem

            lang_mappings[lang_code] = mapping

        return lang_mappings


    @staticmethod
    def parse_lang_mapping_file(file):
        """
        
        """
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            return dict(
                idx_name
                for idx_name in reader
            )


    @staticmethod
    def get_image_mapping(dir):
        """
        
        """
        image_mapping = {}
        
        for image_file in os.listdir(dir):
            idx = Path(image_file).stem
            image_path = os.path.join(dir, image_file)
            
            image_mapping[idx] = image_path

        return image_mapping


    @staticmethod
    def filter_unknown(pokemons):
        return {
            idx: pokemon
            for idx, pokemon in pokemons.items()
            if re.match(r"\d{3}", idx)
            and pokemon.get('image') is not None
        }



if __name__ == '__main__':

    lang_dir = "names"
    image_dir = "images"

    pokedex_ = Pokedex(lang_dir, image_dir)

    print(pokedex_.pokemons['176'])

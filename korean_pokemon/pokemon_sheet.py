import itertools
import os
import operator

import pygame as pg
pg.font.init()


# Set the color properties
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY  = (120, 120, 120)


class PokemonSheet:
    """
    
    """
    def __init__(self,

        page_num: int,
        pokemons: dict,

        name_lang: str = 'ko',
        trans_lang: str = 'en',

        *,
        name_font_size : int = 20,
        trans_font_size: int = 16,
        nums_font_size : int = 16,

        name_font : str = 'notosansmonocjkkr',
        trans_font: str = 'arial',
        nums_font : str = 'arial',

        dpi: int = 120,
        page_height: float = 11.0,
        page_width : float = 8.5,
        page_margin: int = 30,

        pokemon_size: int = 120,
        num_rows: int = 6,
        num_columns: int = 6,
        
        **kwargs
    ):
        """
        
        """
        self.page_num = page_num
        self.pokemons = pokemons

        self.name_lang  = name_lang
        self.trans_lang = trans_lang

        self.name_font_size  = name_font_size
        self.trans_font_size = trans_font_size
        self.nums_font_size  = nums_font_size

        self.name_font  = pg.font.SysFont(name_font, name_font_size)
        self.trans_font = pg.font.SysFont(trans_font, trans_font_size)
        self.nums_font  = pg.font.SysFont(nums_font, nums_font_size)

        self.dpi = dpi
        self.page_height = int(dpi * page_height)
        self.page_width  = int(dpi * page_width)
        self.page_margin = page_margin

        self.pokemon_size = pokemon_size
        self.num_rows = num_rows
        self.num_columns = num_columns

        self.left_margin, self.right_margin = self.set_margins()
        self.bubble_indices = self.set_bubble_indices()

        self.window = pg.display.set_mode( (self.page_width, self.page_height) )
        self.window.fill(WHITE)

        self.populate_page_bubbles()


    def populate_page_bubbles(self):
        """
        
        """
        for indice_idx, indice in enumerate(self.bubble_indices):
            pokemon_idx = self.page_num * (self.num_columns * self.num_rows) + indice_idx + 1
            pokemon_idx = str(pokemon_idx).zfill(3)
            x, y = indice
            
            pokemon = self.pokemons[pokemon_idx]
            self.add_bubble(
                x, y,
                idx=pokemon_idx,
                name = pokemon.get(self.name_lang),
                trans = pokemon.get(self.trans_lang),
                image = pokemon.get('image'),
            )


    def add_bubble(self,
            x,
            y,
            
            *,
            idx,
            name,
            trans,
            image
    ):
        """
        Dynamically build the Pokedex entry on the page,
        based on the number of images per page.
        """
        #
        center_x = x + self.pokemon_size // 2

        
        image_obj  = self.get_image(image)
        num_text   = self.nums_font.render(idx, False, BLACK)
        name_text  = self.name_font.render(name, False, BLACK)
        trans_text = self.trans_font.render(trans, False, BLACK)

        # 
        num_rect = num_text.get_rect(midbottom=(center_x, y))

        image_y = num_rect.midbottom[1]
        image_rect = image_obj.get_rect(midtop=(center_x, image_y))
        
        # name_y = image_rect.midbottom[1]
        name_y = image_rect.midtop[1] + self.pokemon_size
        name_rect = name_text.get_rect(midtop=(center_x, name_y))
        
        trans_y = name_rect.midbottom[1]
        trans_rect = trans_text.get_rect(midtop=(center_x, trans_y))

        # 
        self.window.blit(num_text  , num_rect  )
        self.window.blit(image_obj , image_rect)
        self.window.blit(name_text , name_rect )
        self.window.blit(trans_text, trans_rect)


    @staticmethod
    def get_image(image_path):
        return pg.image.load(image_path).convert_alpha()


    def set_margins(self):
        """
        Add slight whitespace on the side with the holes.
        """
        if self.page_num % 2 == 0:  # This is a right page.
            left_margin  = self.page_margin * 2
            right_margin = self.page_width - self.page_margin

        else:  # This is a left page.
            left_margin  = self.page_margin
            right_margin = self.page_width - (self.page_margin * 2)

        return left_margin, right_margin


    def set_bubble_indices(self):
        """
        
        """
        column_positions = list(
            range(
                self.left_margin, self.right_margin,
                (self.page_width - (2 * self.page_margin)) // self.num_columns
            )
        )

        row_positions = list(
            range(

                self.page_margin, self.page_height - self.page_margin,
                (self.page_height - (2 * self.page_margin)) // self.num_rows
            )
        )

        # Combine and reorder the indexes for proper structuring
        bubble_indices = list(itertools.product(column_positions, row_positions))
        return sorted(bubble_indices, key=operator.itemgetter(1))


    def to_png(self, dir):
        """
        
        """
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

        file = f"page_{self.page_num}.png"
        filepath = os.path.join(dir, file)
        pg.image.save(self.window, filepath)



if __name__ == '__main__':

    from pokedex import Pokedex


    name_lang  = 'ko'
    trans_lang = 'de'

    # name_font = 'arialms'
    # trans_font = 'arialms'
    # num_font = 'arialms'


    lang_dir = "names"
    image_dir = "images"
    pages_dir = f"pages/{name_lang}_to_{trans_lang}"

    pokedex_ = Pokedex(lang_dir, image_dir)



    num_columns = 6
    num_rows = 6

    total_pages = (
        len(pokedex_.pokemons.keys())
        // (num_columns * num_rows)
    )

    for page_num in range(total_pages):

        sheet = PokemonSheet(
            page_num,
            pokedex_.pokemons,
            name_lang=name_lang,
            trans_lang=trans_lang,

            # name_font=name_font,
            # trans_font=trans_font,
            # num_font=num_font,

            num_rows=num_rows,
            num_columns=num_columns
        )

        sheet.to_png(pages_dir)
        print(f"Wrote out page number {page_num} for {name_lang} to {trans_lang}.")

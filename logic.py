import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.height = None
        self.weight = None
        self.level = 1              # Yeni: Seviye sistemi
        self.experience = 0        # Yeni: XP puanı
        self.feeds = 0             # Yeni: Beslenme sayısı
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def load_data(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json() 
                    self.height = data["height"]
                    self.weight =data["weight"]
                    self.name = data['forms'][0]['name']
                else:
                    self.name="Pikachu"

    async def info(self):
        # Tüm veriler yoksa yüklenmesini sağla
        await self.load_data()

        return (
            f"Pokémonunuzun ismi: {self.name}\n"
            f"Seviye: {self.level}\n"
            f"Pokemonun boyu : {self.height} metre\n"
            f"Pokemonun kilosu : {self.weight} kilogram\n"
            f"Toplam Besleme: {self.feeds}"
        )

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url
                
    def feed(self):
        self.feeds += 1
        self.experience += 10
        if self.experience >= self.level * 20:
            self.level += 1
            self.experience = 0
            return f"{self.name.upper()} seviye atladı! Şimdi {self.level}. seviyede!"
        return f"{self.name.upper()} beslendi! Şu anki XP: {self.experience}/{self.level * 20}"

import discord
from discord.ext import commands
from config import token
from logic import Pokemon

# Bot için yetkileri/intents ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='-', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Botun adını konsola çıktı olarak verir

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        pokemon = Pokemon(author)
        await pokemon.load_data()  # <-- Verileri yükle
        await ctx.send(await pokemon.info())
        
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)

            embed.add_field(name="İsim", value=pokemon.name.upper(), inline=False)
            embed.add_field(name="Boy", value=f"{pokemon.height / 10:.1f} m", inline=True)
            embed.add_field(name="Kilo", value=f"{pokemon.weight / 10:.1f} kg", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        msg = pokemon.feed()
        await ctx.send(msg)
    else:
        await ctx.send("Önce bir Pokémon yakalamalısınız! Komut: `*go`")

@bot.command()
async def pokeinfo(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await pokemon.load_data()  # Güncel verileri yükle
        info_text = await pokemon.info()

        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed(title=f"{pokemon.name.upper()} - SEVİYE {pokemon.level}")
            embed.set_image(url=image_url)
            embed.add_field(name="Boy", value=f"{pokemon.height / 10:.1f} m", inline=True)
            embed.add_field(name="Kilo", value=f"{pokemon.weight / 10:.1f} kg", inline=True)
            embed.add_field(name="Besleme", value=str(pokemon.feeds), inline=True)
            embed.add_field(name="XP", value=f"{pokemon.experience}/{pokemon.level * 20}", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(info_text)
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok. `*go` yazarak bir Pokémon yakalayın!")

@bot.command()
async def gameinfo(ctx):
    await ctx.send("İyi oyunlar dilerim") 
    await ctx.send("Oyun komutları ;")
    await ctx.send("-go pokemonunuzu oluşturur")
    await ctx.send("-feed pokemonunuzu besler.Böylece seviyesi ve XP artar")
    await ctx.send("-pokeinfo pokemonunuz hakkında güncel bilgiler verir")

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.send(content)
# Botun çalıştırılması
bot.run(token)

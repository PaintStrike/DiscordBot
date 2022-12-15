import discord
from discord.ext import commands
import youtube_dl
import asyncio
import os
import time
import subprocess

#This bot is thought to be run on Linux. Some Bash it's applied in this bot.


######################## Variables no tocar ##########################################

token = subprocess.getoutput("cat ./token")

intent = discord.Intents.default()
intent.members = True
intent.message_content = True
client = discord.Client(intents=intent)

##############################Variables editables#######################################################

ayuda = """ ```
---- Comandos de Pansito ---

!vivo  - Checkea si Pansito esta vivo
!pan   - Foto de Pan
!rango - Muestra rango actual de Rainbow Six Ranked.
!play  - Reproduce musica desde youtube (Solo links - No usar playlists)
!pause - Pausa la musica
!stop  - Frena la musica y desconecta a Pansito
!ayuda - Muestra este comando 

--- Integrantes Especiales ---

!psicopata
!Juanma
!NatiEnLaDucha
!PeruanoCoca
!HIV
!hugo
!macacos
!Anger

```
"""

################################################## Start Bot #############################################

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


################################################## Variables Globales #############################################

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}


################################################## Inicio de bot #############################################
@client.event
async def on_message(msg):
################################################## Bot de Musica #############################################
  if msg.content.startswith("!play"):
    url = msg.content.split()[1]
    urllen = len(url)
    if urllen > 45:
          await msg.channel.send('¡Pansito solo acepta links de Youtube! Por Favor, asegurate que si es de youtube, no estes compartiendo un link de playlist.')
    else:
      try:
          voice_clients[msg.guild.id].stop()
          await voice_clients[msg.guild.id].disconnect()
      except:
        print("Bot no esta conectado")
          
      try:
          voice_client = await msg.author.voice.channel.connect()
          voice_clients[voice_client.guild.id] = voice_client
      except:
          print("error")
      try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

            voice_clients[msg.guild.id].play(player)
            await msg.channel.send('¡Pansito esta reproduciendo tu cancion!')
      except Exception as err:
          print(err)
          await msg.channel.send(err)

    if msg.content.startswith("!pause"):
        try:
            voice_clients[msg.guild.id].pause()
            await msg.channel.send('¡Pansito puso en pausa la cancion!')
        except Exception as err:
            print(err)

    if msg.content.startswith("!resume"):
        try:
            voice_clients[msg.guild.id].resume()
            await msg.channel.send('¡Pansito saco la pausa de la cancion!')
        except Exception as err:
            print(err)

    if msg.content.startswith("!stop"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
            await msg.channel.send('¡Pansito dejo de reproducir musica en el canal!')
        except Exception as err:
            print(err)

################################################## Bot de Rango #############################################

  if msg.content.startswith('!rango'):
    profile = msg.content.split()[1]
    web = "https://r6.tracker.network/profile/pc/"
    completeurl = web + profile
    os.system("wget " + completeurl )
    file = subprocess.getoutput("ls /home/kali/Desktop/Bot/" + profile + " | wc -l")
    print(file)
    if file == "1":
      ComandoImagen = "cat " + profile + " | grep \"trn-card__content trn-card--light pt8 pb8\" -A 10 | grep \"src=\" | awk '{print $4}' | cut -c 5- | sed 's/\"//g' " # URL de Imagen Rango
      ComandoRango = "cat " + profile + " | grep \"trn-card__content trn-card--light pt8 pb8\" -A 10 | grep trn-text--dimmed | awk '{print $4, $5 }' | cut -c 10- | sed 's#</div>##g' " # Rango
      ComandoMmr = "cat " + profile + " | grep \"trn-card__content trn-card--light pt8 pb8\" -A 10 | grep \"Rajdhani\" | awk '{print $5}' | sed 's#3rem;\">##g' | sed 's#</div>##g'"
      ImagenText = subprocess.getoutput(ComandoImagen)
      RangoText = subprocess.getoutput(ComandoRango)
      MmrText = subprocess.getoutput(ComandoMmr)
      if ImagenText == "":
        await msg.channel.send("¡Este jugador no esta en la base de datos!")
      else:
        os.system("rm -f " + profile) #Remueve el ultimo wget.
        await msg.channel.send(ImagenText)
        await msg.channel.send(profile + " es rango: " + RangoText)
        await msg.channel.send("MMR: " + MmrText )
    else:
      await msg.channel.send("¡Este perfil no existe!")


############################ Eventos de Chat ###########################################
  if msg.content.startswith('!vivo'):
    await msg.channel.send('¡Pansito esta vivo!') 
  if msg.content.startswith('!pan'):
    await msg.channel.send(file=discord.File('13954_1baguetteclsica250g37uds250g.png'))
  if msg.content.startswith('!ayuda'):
    await msg.channel.send(ayuda)
  if msg.content.startswith('!NatiEnLaDucha'):
    await msg.channel.send("https://tenor.com/view/rat-roedor-limpio-gif-14132762") 
  if msg.content.startswith('!Juanma'):
    await msg.channel.send("https://tenor.com/view/big-teeth-flying-kiss-ramzan-shahrukh-flying-kiss-gif-19826856")
  if msg.content.startswith('!PeruanoCoca'):
    await msg.channel.send("https://tenor.com/view/meme-peru-cocacola-peruano-que-rico-gif-24268451")
  if msg.content.startswith('!HIV'):
    await msg.channel.send("https://tenor.com/view/gordito-bailarin-gif-20860785")
  if msg.content.startswith('!psicopata'):
    await msg.channel.send("https://tenor.com/view/smooth-shift-gif-25067223")
  if msg.content.startswith('!hugo'):
    await msg.channel.send("https://tenor.com/view/peruvian-reaction-gif-23691675")
  if msg.content.startswith('!macaco'):
    await msg.channel.send("https://tenor.com/view/alerta-macaco-gif-25033741")
  if msg.content.startswith('!Anger'):
    await msg.channel.send("https://cdn.discordapp.com/attachments/954225382624735233/1052080604839170108/unknown.png")

client.run(token)
import discord
from discord_slash import SlashCommand
from discord.ext import commands
import os
import requests
import bs4


def pinterest_image(url):
    url = url
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    request_data = requests.get(url, headers=headers)
    soup=bs4.BeautifulSoup(request_data.text,"html.parser")
    image_link = str(soup.find_all("link")[6]).split("=")[2].replace("nonce"," ").replace('"'," ")
    return image_link

def pinterest_video(link):
    url = link
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    request_data = requests.get(url, headers=headers)
    video_link = str(str(str(request_data.text).split("video_list")[1]).split(".mp4")[0]).removeprefix("""":{"V_720P":{""").removeprefix(""""url":""").removeprefix('"')+".mp4"
    return video_link


bot = commands.Bot(command_prefix = "/")
slash = SlashCommand(bot,sync_commands=True)

@slash.slash(description="with this command you can download pinterest paid images for free ")
async def pinterestimage(ctx, *, imagelink):
    try:
        image = pinterest_image(imagelink)
        embedVar = discord.Embed(title="Your image is ready to be downloaded", description=f"{ctx.author.mention} visit this link to download the image 👇 \n {image}", color=0xf80404)
        await ctx.send(embed=embedVar)
    except Exception as e:
        embedVar = discord.Embed(title="💀 error", description=e, color=0xf80404)
        await ctx.channel.send(embed=embedVar)

@slash.slash(description="with this command you can download pinterest paid videos for free ")
async def pinterestvideo(ctx, *, videolink):
    try:
        video = pinterest_video(videolink)
        embedVar = discord.Embed(title="Your video is ready to be downloaded", description=f"{ctx.author.mention} visit this link to download the video 👇 \n {video}", color=0xf80404)
        await ctx.send(embed=embedVar)
    except Exception as e:
        embedVar = discord.Embed(title="💀 error", description=e, color=0xf80404)
        await ctx.channel.send(embed=embedVar)


bot.run(os.environ["Token"])

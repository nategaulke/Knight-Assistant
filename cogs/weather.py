#This script was written by Conroy

import discord, requests, os
from discord.ext import commands

#inherit from commands.Cog
class Weather(commands.Cog):

    def __init__(self, bot):

        #reference the bot object from Main.py
        self.bot = bot


    @commands.command(help = "Shows the current weather information for a specific city. Simply type the zip code after \"!weather\". Currently, this only works for US cities.")
    async def weather(self, ctx, *, zip_code: str):

        weather_api_key = os.getenv('WEATHER_API_KEY')
        weather_api_base_url = "http://api.openweathermap.org/data/2.5/weather?zip="

        weather_api_complete_url = weather_api_base_url + zip_code + "&appid=" + weather_api_key + "&units=imperial"
        response = requests.get(weather_api_complete_url)
        x = response.json()
        channel = ctx.message.channel   

        if x["cod"] != "404":
            #get the weather information
            y = x["main"]
            current_temp = y["temp"] 
            current_temp_celsiuis = (current_temp - 32) * (5/9)
            high_temp = y["temp_max"]
            high_temp_celsiuis = (high_temp - 32) * (5/9)
            low_temp = y["temp_min"]
            low_temp_celsiuis = (low_temp - 32) * (5/9)
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            #now we need to put the weather information inside a discord.Embed
            embed = discord.Embed(title="Weather in " + x["name"], color=ctx.guild.me.top_role.color, timestamp=ctx.message.created_at)
            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature", value=f"**now - {round(current_temp,1)}°F ({round(current_temp_celsiuis,1)}°C)\nlow - {round(low_temp,1)}°F ({round(low_temp_celsiuis,1)}°C)\nhigh - {round(high_temp,1)}°F ({round(high_temp_celsiuis,1)}°C)**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")

            #send the embed!
            await channel.send(embed=embed)        
        else:
            await channel.send("City not found.")

#this function connects this cog (via the Weather class) to the bot object
def setup(bot):
    bot.add_cog(Weather(bot))
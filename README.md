# Knight Assistant

## About
Knight Assistant is a Team Project by University of Central Florida students Nathanael Gaulke, Conroy Ricketts, and Christine Stevens for the Knight Hack's Projects Team. 

Knight Hacks is a Registered Student Organization at the University of Central Florida which specializes in Software Development and its annual Hackathon. The KnightHacks Projects Team is an opportunity for students to be able to work on projects outside of class with other like-minded students.

We started the design process in February and decided to work on a Discord bot to gain more experience working with standard technologies outside of our Computer Science curriculum. We collaborated on GitHub and reviewed each other's commits before merging them into our code base.  We held weekly meetings and also received mentorship from the Projects Team Leaders. We were glad to present a demo of our Bot during the Knight Hacks Projects Showcase. We were proud of our project and won 1st place in the competition. 


Knight Assistant is a Discord Bot written in python using the following technologies: 

* Discord.py
* MongoDB
* googletrans
* Weather API
* JSON Requests
* Hosted on Heroku


## Features

* :calendar: Events: `Add`  `Show`  `Delete` 
* :white_check_mark: Tasks: `Add`  `Show`  `Delete`  `Check-Off`  `Uncheck`
* :sun_behind_rain_cloud: Weather
* :christmas_tree: Show Holiday
* 🏖️ Next UCF Break Finder
* :heavy_division_sign: Calculator 
* :money_with_wings: Tip Calculator
* :speaking_head: Translator

## How to Use

### Run Locally

Clone this repository to your computer

Set up the virual environment with
`python -m pip install -r requirements.txt`


Once .env file is set up then run
`python Main.py`

### Run on Heroku 
(easiest method)

Fork this repository

Open Heroku Account and Create a New App

Select Github as deployment method and link forked repository

Go to Settings -> Config Vars to setup up environmental variables

Go to Resources -> Dynos to turn on 
`worker: python Main.py`

### Setup Environmental Variables

To run, Knight Assistant needs:
* Discord Application Token (Go [here](https://discord.com/developers/applications) to create a new bot application with token)
* MongoDB Client URL (Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas2) to create a cluster with database "Database" and collections "Events" and "Tasks")
* Weather API Key (go [here](https://openweathermap.org/api) to setup)
(Note: More in-depth instructions can be found online)

In the .env file/config variables settings set
* TOKEN = {Your bot token}
* WEATHER_API_KEY = {API key}
* MONGO_URL = {URL to cluster with database username and password inserted into link}

## License
Released under the [MIT License](https://github.com/nategaulke/Discord_Personal_Assistant/blob/main/LICENSE)

## Credits
* [Nathanael Gaulke](https://github.com/nategaulke)
* [Conroy Ricketts](https://github.com/conroyr41)
* [Christine Stevens](https://github.com/cmstevens02)



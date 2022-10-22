# Chelper
Right from the creation of the server, Chelper guides teachers through the configuration, there is almost no actions needed from the teacher. Here's what we implemented

- When students will join the Discord, it will ask them for their student ID to verify them, rename them to their real name and assign them the right role to give them permissions to what they need. This way, no more Discord raid!
- Teachers can give assignments with a due date and students will be able to submit their hard work directly to the bot, in his direct messages which will redirect it only to the teacher.
- Teachers are able to start online class at any moment, which opens the voice channel for the students to join

Explanation video : https://www.youtube.com/watch?v=kRZdfa6JB8M

## Inspiration

Some of our team members have been in online discord classes before. We noticed that, for teachers, Discord can be a bit complicated to learn with all those text channels, vocal channels, permissions, roles, etc. We think Discord could be a very good platform for online classes plus it's free! So, how about a bot that manages a class for the teacher?

## Instruction to launch the project

1. Create a discord application with a discord bot inside it https://discord.com/developers/applications
2. Be sure to have python 3.9 installed and in your path (Test in a cmd: "python --version")
3. Install poetry using a PowerShell shell : (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
4. Open a cmd in the project directory
5. In that cmd, run "poetry install" to install every dependencies
6. Also in that cmd, run "poetry shell" to enter the VE

You are now in the project virtual environment. Now you can run and test script using "py scriptName.py" 

To add package dependencies, use "poetry install myPackage"

To exit the virtual environment, run "exit"

Don't forget to add a .env file with these variables:
- DISCORD_TOKEN={Insert discord bot token}
- DB_SERVER={Insert SQL DB server}
- DB_NAME={Insert DB Name}

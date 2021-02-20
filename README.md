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

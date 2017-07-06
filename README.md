# WAT

## Installation
First use :

`git clone git@github.com:TanguyLe/WAT.git`

### WebService
The webService used by WAT is a python (bottle.py) application using sqlite. Consequently you need to have those 3 dependencies installed.
#### Ubuntu
Install python and sqlite packages, and follow [bottle's tutorial](https://bottlepy.org/docs/dev/tutorial.html#installation) to set up a virtual environnement.
#### Windows
First install the latest python 3 release from [python's website](https://www.python.org/downloads/windows/), then download [bottle file](https://github.com/bottlepy/bottle/raw/master/bottle.py) and put that file in the webService/app folder of your project.

And finally [sqlite](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm) following the instructions.
## QuickStart
### WebService
First run the script webService/db/db_init.py in its own directory to set up the database with sample data.

Then after setting up with your OS (see below), you can browse at localhost:8080 to use the webService, see localhost:8080/help.
#### Ubuntu
Switch to your virtual environnement by running `. ./env/bin/activate` (if your environnement is env) in the correct directory and then `python ./main.py`. (May vary according to your python command)
#### Windows
Get to the webService/app folder and then use `py ./main.py` to run the bottle server. (May vary according to your python command) 
## Documentation

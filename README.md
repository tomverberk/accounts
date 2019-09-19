# accounts
Online help for studying mathematics

## Setting up the working
1. Download github desktop
1. Download some sort of coding environment (I use visual studio code)
1. Press 'file' -> clone repository -> 'tomverberk/accounts'
1. define the location of the repository, preferably to a location without spaces or other non-alphanumerical characters in it. Having spaces or other non-alphanumerical characters in the path can cause strange issues later down the road.
1. Press 'fetch origin'.
1. Open your coding environment
1. Press 'file' -> 'open folder' -> 'select the folder as declared earlier'
Now you are somewhat ready to start coding


## Getting started with development

1. Install the latest version of Python 3. If you are on Windows, you can download Python from [python.org]. If you are not, check if you already have a recent version by runnning `python3 --version`. As of writing, Python 3.5 or higher is recent enough, but this may change in the future.
1. Start a command prompt/terminal in the folder you have put the Squire sources in. Use this terminal to execute the rest of the commands (in order)
1. Move to the account folder
1. Create a new virtual environment. On Windows, this can be done by running `py -3 -m venv venv`. On other operating systems this is done by running `python3 -m venv venv`. This ensures that this project's dependencies don't conflict with other Python applications on your system.
1. Activate your virtual environment by running `venv\Scripts\activate` if you are on Windows. Otherwise run `source venv/bin/activate`. If this is successful, your terminal line will start with `(venv)`. We assume that any commands ran beyond this point are ran inside a virtualenv for this project. This step needs to be done for each terminal you are using for this project, so if you later return to continue working on the program, you need to rerun this command.
1. Install the dependencies: `pip install -r requirements/dev.txt`. These dependencies include common dependencies (such as *Django*) as well as dev-dependencies that speed up or ease the development process (such as *coverage.py*). For more information about dependencies, view the *Dependencies* section below.
1. Setup the database by running `python manage.py migrate`. This ensures your database can store the items we expect to store in it.
1. Start the server: `python manage.py runserver`. This starts a web server, which you can access using your webbrowser and going to `localhost:8000`.
<br/><br/>

## How to start writing code
Since we are working with multiple people at the same pieces of code we have to make sure that things are done in the right way.
To do this we first go to the github website.
1. Go to the correct project folder.
1. press Issues.
1. Make a new issue, state in the description what you are going to do (for example, Get question from database).
1. Go to github desktop
1. Create a new branch, let it look like this "#<ID>:<Description>" Where #ID is the id number of the issue found on the github webpage.
1. After you are done working you go to github desktop, you give a summary of your commit and you commit your work.
1. Once you have completed the assignment you   go to the github webpage: press -> pull request and create a new pull request, this way the code you made will be visible for everyone.
1. this will ensure we don't do double stuff.
  
  If you have trouble working with python I can recommand this tutorial.
  https://tutorial.djangogirls.org/en/dynamic_data_in_templates/

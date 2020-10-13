import shutil, os, zipfile
from pathlib import Path
import PySimpleGUI as sg
from bs4 import BeautifulSoup
import requests


# Declare some variables
kattis_dir = Path('/Users/andreas/Google Drev/Programming/Kattis')
script_dir = Path('/Users/andreas/Google Drev/Programming/Python/NewKattis')

# Get the name of the problem, used for creating the correct directory
problem_url = sg.popup_get_text('Insert problem URL', 'What is the URL for the problem?')
template = sg.popup_get_text('Programming language', 'Type in desired programming language to solve this Kattis problem with')

# DEV ENV shortcut
#roblem_url = 'https://open.kattis.com/problems/basicprogramming1'
#template = 'java'


# Handle errors, proceed if there is none:
if problem_url is not None and len(problem_url) > 0:
    if template is not None and len(template) > 0:
        template_file = f"{template}.template"
        # We're golden! Lets go make some Kattis setups!
    
        # First make sure there is a template for the programming language!
        for file in script_dir.glob('*.template'):
            if str(file).split('/')[-1] == template_file:
                
                # Get the problem name from the website
                with requests.get(problem_url) as page:
                    if not page.status_code == 200:
                        sg.popup('Error', 'The response from the website was not O-K')
                        exit(2)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    
                    # Cut out the title from the Kattis problem page
                    title = str(soup.find('h1')).replace('</h1>', '').replace('<h1>', '')

                    # TODO: Do the local directory stuff - make sure it doesn't exist, 
                    # create new dir and copy the template file
                    problem_dir = kattis_dir / title

                    if problem_dir.exists():
                        sg.popup('Error', 'There was already a kattis project created for this problem.')
                        exit(1)    

                    os.makedirs(kattis_dir / title)

                    # Get the samples file
                    with requests.get(problem_url + '/file/statement/samples.zip') as samples:
                        with open(problem_dir / 'samples.zip', 'wb') as file:
                            for chunk in samples.iter_content(chunk_size=128):
                                file.write(chunk)

                    # Extracting the zip file into the problem directory
                    samples = zipfile.ZipFile(problem_dir / 'samples.zip')
                    samples.extractall(problem_dir)


                    # Start to work with both the name of the file, but also the class name
                    class_name = title
                    numbers = {'0': 'Zero', '1' : 'One', '2' : 'Two', '3': 'Three', '4': 'Four',
                                '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight',
                                '9': 'Nine'}

                    for k, v in numbers.items():
                        class_name = class_name.replace(k, v)

                    class_name = class_name.replace(' ', '').replace('-', '')
                    file_name = class_name  + '.' + template

                    # Copy the file over, substituting the changes into the template
                    with open(script_dir / template_file, 'r') as file_in:
                        with open(problem_dir / file_name, 'w') as file_out:
                            file_out.write(file_in.read().replace('[0]', class_name))
                    
    else:
        sg.popup('Error', 'Error with programming language! Either none was given, or the programming language is too short!')
else:
    sg.popup('Error', 'Error with problem URL! Not set or not long enough ')

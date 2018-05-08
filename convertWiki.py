# WikiToManual by Liam Fruzyna
# Takes a github wiki directory and converts it to a PDF
# Requires a _Sidebar.md file as that is where the order is from
# Does not work with tables for now

# imports
from md2pdf.core import md2pdf
from os import listdir
from os.path import isfile, join, splitext
import re
import sys

# get path of wiki
path = 'markdown/'
if len(sys.argv) > 1:
    path = sys.argv[1]
    print('Using directory of ' + path)

# get all files in wiki
files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.md')]
files

# read a file given only the name
def readFile(name):
    f = open(path + name, 'r')
    return f.read()

# write to a file given only the name and output
def writeFile(name, text):
    f = open(name, 'w+')
    f.write(text)
    f.close()
    
# get the order of all the files names according to the sidebar
def getPageOrder(sidebarText):
    return [getFileName(re.findall('^.*\((.*)\).*$', line)[0]) for line in sidebarText.split('\n') if '[' in line]

# get the names of all the pages
def getPageNames(sidebarText):
    return [re.findall('^.*\[(.*)\].*$', line)[0] for line in sidebarText.split('\n') if '[' in line]

# get the actual file name, ignoring case
def getFileName(name):
    for file in files:
        if splitext(file)[0].lower() == name.lower():
            return file
    return 'bad name'

# get the title of the page
def getPageTitle(fileName):
    return names[pages.index(fileName)]

# sidebar file is requires
sidebar = '_Sidebar.md'
if sidebar in files:
    # process sidebar
    sidebarText = readFile(sidebar)
    pages = getPageOrder(sidebarText)
    names = getPageNames(sidebarText)

    # combine files and write to both markdown and pdf
    combined = '\n\n---\n\n'.join(['#' + getPageTitle(name) + '\n\n' + readFile(name) for name in pages if name != 'bad name'])
    writeFile('combined.md', combined)
    print('Combined markdown finished!')
    md2pdf('combined.pdf', md_content=combined, css_file_path='styles.css', base_url=path)
    print('PDF finished!')
else:
    print('Failed to find _Sidebar.md')


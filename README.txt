# Quick Notes:
- Users are assumed to have a basic understanding of Python and Jupyter Notebooks
- This app was written using VS Code on a Windows computer with SIE installed

# Prerequisites
- the following should be installed, they all have pip installs if you google for them
pythonnet
pandas


# Getting Started
1- install and make sure SIE is working.
2- Get your path to where SIE is installed
3- edit config.py 
3a- set the path to LibSIE.dll which is at the root of where SIE is installed (usually)
3b- set the path to your working TRE directory. I tend to put it on the desktop but it can be anywhere. 
3c- Create two folders in this project for string and string_excel. These are in the GIT ignore file and are not automatically created.
4- Open SIE and export strings (only the /en) folder to the directory you setup in step 3b. It can be easier to export to desktop and copy it in. Your goal is to have a folder in this project that is just string/en/... as opposed to something like string/string/en.
5- open getting_started.ipynb and go through the setup The first step is to create all the excel files which takes about 3 mins.




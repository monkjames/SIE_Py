import os
## do not edit these ###################
notebook_dir = os.getcwd()
########################################


# add all global configuration vars here
# using os.join ensures the paths are accurate with the correct slash for your OS 
# but you can use regular strings if you prefer

# this is where you installed SIE
SIE_DLL = os.path.join('C:',  os.sep, 'sytners_iff_editor_3_7_0_95_release','LibSIE.dll')

# this is used to 'publish' a new string to your working directory
TRE_STAGING = os.path.join('C:', os.sep, 'Users', 'micha', 'Desktop', 'a_working_tre')

# local path where you want to store excel files
EXCEL = os.path.join(notebook_dir, 'string_excel', 'en')

# local path where you exported the string STF files
STF = os.path.join(notebook_dir, 'string', 'en')



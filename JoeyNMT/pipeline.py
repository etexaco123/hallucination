# TODO: Set your source and target languages. Keep in mind, these traditionally use language codes as found here:
# These will also become the suffix's of all vocab and corpus files used throughout

import os
import sys
import subprocess

source_language = "de"
target_language = "en" 
lc = False  # If True, lowercase the data.
seed = 42  # Random seed for shuffling.
tag = "baseline" # Give a unique name to your folder - this is to ensure you don't rewrite any models you've already submitted

os.environ["src"] = source_language # Sets them in bash as well, since we often use bash scripts
os.environ["tgt"] = target_language
os.environ["tag"] = tag

src = os.getenv('src')
tgt = os.getenv('src')

fullpath = './'+src+'-'+tgt+'-'+tag

# This will save it to a folder in our gdrive instead!
subprocess.run('mkdir -p '+fullpath)
os.environ["home_path"] = "./%s-%s-%s" % (source_language, target_language, tag)

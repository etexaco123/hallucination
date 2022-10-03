from pathlib import Path
import sys
import re

# os.chdir('E:/project_backup/predictions')
test1 = sys.argv[1]  # Test file argument
test2 = sys.argv[2]  # MTed file argument

de_orig = Path(test1).read_text().splitlines()
en_orig = Path(test2).read_text().splitlines()


assert len(en_orig) == len(de_orig)

en_valid = [] 
de_valid = []
for de , en in zip(de_orig, en_orig):
    de_clean = de.lower()
    en_clean = en.lower()
    if (len(str(de_clean)) > 3 and len(str(en_clean)) > 3 and str(de_clean) != str(en_clean)): #ensures that a string is present in src and tgt and are not dupicates
        de_valid.append(de_clean)
        en_valid.append(en_clean)
assert len(de_valid) == len(en_valid)

Path('JRC2.clean.de').write_text('\n'.join(de_valid))
Path('JRC2.clean.en').write_text('\n'.join(en_valid))
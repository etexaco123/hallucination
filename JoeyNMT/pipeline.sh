#!/bin/bash

# TODO: Set your source and target languages. Keep in mind, these traditionally use language codes as found here:
# These will also become the suffix's of all vocab and corpus files used throughout

python3 - <<'EOF'
import os
source_language = "de"
target_language = "en" 
lc = False  # If True, lowercase the data.
seed = 42  # Random seed for shuffling.
tag = "baseline" # Give a unique name to your folder - this is to ensure you don't rewrite any models you've already submitted

os.environ["src"] = source_language # Sets them in bash as well, since we often use bash scripts
os.environ["tgt"] = target_language
os.environ["tag"] = tag
EOF

# This will save it to a folder in our gdrive instead!
mkdir -p "./$src-$tgt-$tag"
mkdir -p "./$src-$tgt-$tag/data"

python3 - <<'EOF'
os.environ["ex_path"] = "./%s-%s-%s" % (source_language, target_language, tag)

# specify the file paths here
source_file = "../corpus/EMEA/MOSES/EMEA.de-en.de"
target_file = "../corpus/EMEA/MOSES/EMEA.de-en.en"
EOF

# They should both have the same length.
wc -l "$source_file"
wc -l "$target_file"

#print the first 15 lines of bothe the source and target
head -n 15 "$source_file" "$target_file"

python3 - <<'EOF'
#there is need for tokenization, thise can be done via sacremoses
tok_source_file = source_file+".tok"
tok_target_file = target_file+".tok"
EOF

# Tokenize the source
sacremoses -l "$source_language" tokenize < "$source_file" > "$tok_source_file"
# Tokenize the target
sacremoses -l "$target_language" tokenize < "$target_file" > "$tok_target_file"

# Let's take a look what tokenization did to the text.
head "$source_file"*
head "$target_file"*

#split the dataset by 70%,20%,10% for train, dev, test
head -n 776126 "$source_file" > /de-en-baseline/data/train.de
head -n 776126 "$target_file" > /de-en-baseline/data/train.en
tail -n 332625 "$source_file" | head -n 221750 > /de-en-baseline/data/dev.de
tail -n 332625 "$target_file" | head -n 221750 > /de-en-baseline/data/dev.en
tail -n 110875 "$source_file" > /de-en-baseline/data/test.de
tail -n 110875 "$target_file" > /de-en-baseline/data/test.en

wc -lw /de-en-baseline/data/train.* \
        /de-en-baseline/data/dev.* \
        /de-en-baseline/data/test.*

python3 - <<'EOF'
#declare environment variable 
os.environ["dataset"]="./de-en-baseline/data"

# One of the huge boosts in NMT performance was to use a different method of tokenizing. 
# Usually, NMT would tokenize by words. However, using a method called BPE gave amazing boosts to performance

# Do subword NMT
from os import path
os.environ["src"] = source_language # Sets them in bash as well, since we often use bash scripts
os.environ["tgt"] = target_language

# Learn BPEs on the training data.
os.environ["data_path"] = path.join("joeynmt", "data", source_language + target_language) # Herman! 
EOF

subword-nmt learn-joint-bpe-and-vocab --input $dataset/train.$src $dataset/train.$tgt -s 4000 \
                                -o $dataset/bpe.codes.4000 --write-vocabulary $dataset/vocab.$src $dataset/vocab.$tgt

# Apply BPE splits to the development and test data.
subword-nmt apply-bpe -c $dataset/bpe.codes.4000 --vocabulary $dataset/vocab.$src < $dataset/train.$src > $dataset/train.bpe.$src
subword-nmt apply-bpe -c $dataset/bpe.codes.4000 --vocabulary $dataset/vocab.$tgt < $dataset/train.$tgt > $dataset/train.bpe.$tgt

subword-nmt apply-bpe -c $dataset/bpe.codes.4000 --vocabulary $dataset/vocab.$src < $dataset/dev.$src > $dataset/dev.bpe.$src
subword-nmt apply-bpe -c $dataset/bpe.codes.4000 --vocabulary $dataset/vocab.$tgt < $dataset/dev.$tgt > $dataset/dev.bpe.$tgt
subword-nmt apply-bpe -c $dataset/bpe.codes.4000 --vocabulary $dataset/vocab.$src < $dataset/test.$src > $dataset/test.bpe.$src
subword-nmt apply-bpe -c $dataset/bpe.codes.4000 --vocabulary $dataset/vocab.$tgt < $dataset/test.$tgt > $dataset/test.bpe.$tgt

# Create directory, move everyone we care about to the correct location
mkdir -p "$data_path"
cp $dataset/train.* "$data_path"
cp $dataset/test.* "$data_path"
cp $dataset/dev.* "$data_path"
cp $dataset/bpe.codes.4000 "$data_path"
ls "$data_path"

# Also move everything we care about to a mounted location in google drive (relevant if running in colab) at gdrive_path
cp $dataset/train.* "$ex_path"
cp $dataset/test.* "$ex_path"
cp $dataset/dev.* "$ex_path"
cp $dataset/bpe.codes.4000 "$ex_path"
ls "$ex_path"

# Create that vocab using build_vocab
sudo chmod +x joeynmt/scripts/build_vocab.py
joeynmt/scripts/build_vocab.py $data_path/train.bpe.$src $data_path/train.bpe.$tgt --output_path $data_path/vocab.txt

# Some output
echo "BPE Test language Sentences"
tail -n 5 $dataset/test.bpe.$tgt
echo "Combined BPE Vocab"
tail -n 10 joeynmt/data/$src$tgt/vocab.txt  # Herman


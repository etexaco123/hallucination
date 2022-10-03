# Corpus-level BLEU score with arguments
# Run this file from CMD/Terminal
# Example Command: python3 corpus-bleu.py reference_file_name.txt mt_file_name.txt


import sys
import sacrebleu
from sacremoses import MosesDetokenizer
md = MosesDetokenizer(lang='en')

target_test = sys.argv[1]  # Test file argument
target_pred = sys.argv[2]  # MT predictions file argument

# reference human translation file
#detokenize the references
refs = []

with open(target_test) as test:
    for line in test: 
        line = line.strip().split() 
        line = md.detokenize(line) 
        refs.append(line)
    
#print("Reference 1st sentence:", refs[0])

refs = [refs]  # Yes, it is a list of list(s) of the references


# Open the predictions by the NMT model 
# detokenize the predictions
preds = []

with open(target_pred) as pred:  
    for line in pred: 
        line = line.strip().split() 
        line = md.detokenize(line) 
        preds.append(line)

#print("MTed 1st sentence:", preds[0])    


# Calculate and print the BLEU score
bleu = sacrebleu.corpus_bleu(preds, refs)
print("The Corpus level BLEU score is : ", bleu.score)
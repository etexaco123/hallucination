# BLEU for sentence level with arguments
# Run this file from CMD/Terminal
# Example Command: python3 sentence_bleu.py reference_file_name.txt mt_file_name.txt

import sys
import sacrebleu
from sacremoses import MosesDetokenizer
md = MosesDetokenizer(lang='en')

target_test = sys.argv[1]  # Test file argument
target_pred = sys.argv[2]  # MTed file argument

# Opens the reference file and detokenize
refs = []

with open(target_test) as test:
    for line in test: 
        line = line.strip().split() 
        line = md.detokenize(line) 
        refs.append(line)
    
#print("Reference 1st sentence:", refs[0]) #stop the printing of bleu score

# Opens the predictions by the NMT model and detokenize
preds = []

with open(target_pred) as pred:  
    for line in pred: 
        line = line.strip().split() 
        line = md.detokenize(line) 
        preds.append(line)

# Compute BLEU score for sentence by sentence and save the result to a file
with open("bleu-" + target_pred + ".txt", "w+") as output:
    for line in zip(refs,preds):
        test = line[0]
        pred = line[1]
        # print(test, "\t--->\t", pred) #stop the printing
        bleu = sacrebleu.sentence_bleu(pred, [test], smooth_method='exp')
        print(bleu.score, "\n")
        output.write(str(bleu.score) + "\n")


#press ctrl + K or ctrl +Q to toggle comments if using notepad ++

# with open("bleu-"+tgt_preds+".txt", "r+") as stats:
    # stats_info= stats.readlines()
    # stats_history = collections.Counter(stats_info)
    # #print(stats_history)
    # #{k: v for k, v in sorted(stats_history.items(), key=lambda item: item[1])}
    # #stats_keys =['{:.2f}'.format(float(key)) for key in stats_history.keys()]
    # plt.bar(['{:.2f}'.format(float(key)) for key in stats_history.keys()], stats_history.values())
    # plt.xticks(rotation=90, horizontalalignment="center")
    # plt.title("Distibution of Similarity")
    # plt.xlabel("BLEU scores")
    # plt.ylabel("No of Sentences")
    # plt.show()
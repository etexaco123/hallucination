#counting the number of hallucinations 
# to run in CMD/Terminal:
#python3 hallucination_counter.py source_file reference_file predictions_file

import sys
from pathlib import Path


source = sys.argv[1]   # source file
references = sys.argv[2] # reference translated file
predictions = sys.argv[3] # MT translated file
#bleu_scores = sys.argv[4]

#with open(file, ) as stack:
source_stack = Path(source).read_text(encoding="UTF-8").splitlines()
reference_stack = Path(references).read_text(encoding="UTF-8").splitlines()
prediction_stack = Path(predictions).read_text(encoding="UTF-8").splitlines()
#score_stack = Path(bleu_scores).read_text(encoding="UTF-8").splitlines()

hallucinations_count = 0
hallucinations = [] # contains the list of index where hallucinations occur in the the 
non_hallucinations_count = 0
non_hallucinations = []


#indices = [index for index, element in enumerate(a_list) if element == 1]
with open('bleu-'+predictions+'.txt', 'r' ) as score_stack:
    scores = score_stack.readlines()
    for i, score in enumerate(scores):
        if float(score) <= 1.0: #0.06, 0.09 
            hallucinations_count+=1
            hallucinations.append(i)
            
        else:
            non_hallucinations.append(i)
            non_hallucinations_count+=1
        
        
print("-----------The test corpus statistics---------")
print("number of hallucinations : %d" %(hallucinations_count))
print("number of non_hallucinations : %d" %(non_hallucinations_count))
print("\n")


for _,hallucination in enumerate(hallucinations):
    print(source_stack[hallucination] + '\n')
    print(reference_stack[hallucination] + '\n')
    print(prediction_stack[hallucination] + '\n')
    print(hallucination)
    print(" ***************************************")
    
    
        
    
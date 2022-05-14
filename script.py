import re
import string
import logging as l

# alphabet to number
ANS_CHAR = dict(zip(range(1, 27), string.ascii_uppercase)) 

# open file
FILE = open("/home/huy/Projects/k12/extracted.html", "r")
TEXT = FILE.read()


ALL_ANS_REGEX = re.compile(r'''
value="
([1234]+)
"
''', re.X)

ALL_CORRECT_ANS_REGEX = re.compile(r'''
"answerCode":
([1234]+)
,"point":"1",
''', re.X)

l.basicConfig(filename="answer.log",level=l.DEBUG)

# Input params 
print("Input total question:")
total_question = int(input())
print("Input number of answers per question:")
ans_per_question = int(input())

# Vars initialization
all_ans = re.findall(ALL_ANS_REGEX, TEXT)
all_correct_ans = re.findall(ALL_CORRECT_ANS_REGEX, TEXT)
ans_val = [None] * ans_per_question

# Logics
for i in range(0, total_question *  ans_per_question, ans_per_question):
    current_question_index = int(i / ans_per_question)
    current_correct_ans = int(all_correct_ans[current_question_index])

    for j in range(0, ans_per_question):
        current_ans_index = i + j
        ans_val[j] = int(all_ans[current_ans_index])

    for j in range(0, ans_per_question):
        current_ans = ans_val[j]
        if current_ans == current_correct_ans:
            print(f'{current_question_index + 1}: {ANS_CHAR[j + 1]}')
            break

FILE.close()
import re
import string

# Value to char
ANS_CHAR = dict(zip(range(1, 27), string.ascii_uppercase)) 

# Open file
FILE = open("/home/huy/Projects/k12/input.txt", "r")
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

# Input params 
print("Input total question:")
total_question = int(input())
print("Input number of answers per question:")
ans_per_question = int(input())

# Vars initialization
ANS = re.findall(ALL_ANS_REGEX, TEXT)
CORRECT_ANS = re.findall(ALL_CORRECT_ANS_REGEX, TEXT)

# Logics
for i in range(0, total_question *  ans_per_question, ans_per_question):
    current_question_index = int(i / ans_per_question)
    current_correct_ans = int(CORRECT_ANS[current_question_index])

    for j in range(0, ans_per_question):
        current_ans_index = i + j
        current_ans = int(ANS[current_ans_index])
        if current_ans == current_correct_ans:
            print(f'{current_question_index + 1}: {ANS_CHAR[j + 1]}')

FILE.close()
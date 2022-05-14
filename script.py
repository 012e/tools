import re
import string

# Value to char
ANS_CHAR = dict(zip(range(1, 27), string.ascii_uppercase)) 

# Open file
FILE = open("/home/huy/Projects/k12/bruh.txt", "r")
TEXT = FILE.read()

ALL_ANS_REGEX = re.compile(r'''
value="
([1234.]+)
"
''', re.X)

ALL_CORRECT_ANS_REGEX = re.compile(r'''
"answerCode":
([""\w\d.]+)
,"point":"1",
''', re.X)

# Input params 
print("Input total question:")
total_question = int(input())
print("Input number of answers per question:")
ans_per_question = int(input())

# total_question = 25
# ans_per_question = 4


# Vars initialization

# form: type="<this-code>"
ans = re.findall(ALL_ANS_REGEX, TEXT)
# remove all non-number characters
ans = [int(re.sub("[^0-9]", "", s)) for s in ans]
# split into smaller chunks by question
ans = [ans[i:i + ans_per_question] for i in range(0, len(ans), ans_per_question)]

# correct ans is taken from text
# form: "answerCode": <this-code>, "point": "1"
correct_ans = re.findall(ALL_CORRECT_ANS_REGEX, TEXT)
# remove all non-number characters
correct_ans = [int(re.sub("[^0-9]", "", s)) for s in correct_ans]

for i in range(0, total_question):
    curr_ans = ANS_CHAR[ans[i].index(correct_ans[i]) + 1]
    print(f"{i + 1}. {curr_ans}")
FILE.close()

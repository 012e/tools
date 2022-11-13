import re
import os
import string

"""
Value to char:
ANS_CHAR = {
    1: 'A',
    2: 'B',
    3: 'C',
    ...
}
"""
ANS_CHAR = dict(zip(range(1, 27), string.ascii_uppercase))

ALL_ANS_REGEX = re.compile(
    r"""
value="
([1234.]+)
"
""",
    re.X,
)


def get_corrent_ans(text: str) -> list[int]:
    ALL_CORRECT_ANS_REGEX = re.compile(
        r'''{"answerCode":"?([\w\d.]+)"?[^}]*?"point":"1"''',
        re.X,
    )

    # Exact only part with VHV.load at the beginning
    # otherwise it won't work (will get some random extrated answers)
    temp = ""
    for line in text.splitlines():
        if line.startswith("VHV.load("):
            temp += line
    text = temp

    # form: "answerCode": <this-code>, "point": "1"
    correct_ans = re.findall(ALL_CORRECT_ANS_REGEX, text)
    # remove non-number chars + convert to number
    correct_ans = [int(re.sub("[^0-9]", "", s)) for s in correct_ans]
    return correct_ans


def get_all_ans(text: str, total_question: int, ans_per_question) -> list[list[int]]:
    # form: type="<this-code>"
    ans = re.findall(ALL_ANS_REGEX, text)
    # remove all non-number characters
    ans = [int(re.sub("[^0-9]", "", s)) for s in ans]
    # split into smaller chunks by question
    ans = [ans[i : i + ans_per_question] for i in range(0, len(ans), ans_per_question)]
    return ans


def get_relative_ans(total_question: int, ans_per_question: int) -> list[int]:
    for i in range(0, total_question):
        curr_ans = ans[i].index(correct_ans[i])


def parse(text: str, total_question, ans_per_question) -> list[int]:
    ans = get_all_ans(text, total_question, ans_per_question)
    correct_ans = get_corrent_ans(text)
    res = []
    for i in range(0, total_question):
        res.append(ans[i].index(correct_ans[i]))
    return res


if __name__ == "__main__":

    total_question = int(input("how much questions are there: "))
    ans_per_question = 4

    # Open file (<current dir>/bruh.txt)
    FILE = open(os.getcwd() + "/bruh.txt", "r")
    TEXT = FILE.read()

    ans = get_all_ans(TEXT, total_question, ans_per_question)
    correct_ans = get_corrent_ans(TEXT)

    for i in range(0, total_question):
        curr_ans = ANS_CHAR[ans[i].index(correct_ans[i]) + 1]
        print(f"{i + 1}. {curr_ans}")
    FILE.close()

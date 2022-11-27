import os
import string
import json


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


class QuestionSuite:
    correct_choice: int
    relative_correct_choice: int
    total_choice: int
    choice_arrangement: list[int]

    def __init__(self, correct_choice: int, choice_arrangement: list[int]):
        self.correct_choice = correct_choice
        self.choice_arrangement = choice_arrangement
        self.total_choice = len(choice_arrangement)
        self.relative_correct_choice = choice_arrangement.index(correct_choice)


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)


def parse(text: str) -> list[QuestionSuite]:
    ques_and_ans = []
    for line in text.splitlines():
        if line.startswith("VHV.load("):
            ques_and_ans.append(line)

    question_suites = []
    for obj in ques_and_ans:
        obj = obj[findnth(obj, "{", 1) :]
        obj = obj[: obj.rfind("}")]
        obj = obj[: obj.rfind("}") + 1]
        obj = json.loads(obj)
        for choice in obj["choices"]:
            if choice["point"] == "1":
                correct_choice = int(choice["answerCode"]) - 1
                break

        question_suites.append(
            QuestionSuite(
                correct_choice=correct_choice,
                choice_arrangement=[int(val) for val in obj["pos"]],
            )
        )
    return question_suites


if __name__ == "__main__":

    # Open file (<current dir>/bruh.txt)
    FILE = open(os.getcwd() + "/response-decoded.txt", "r")
    TEXT = FILE.read()
    question_suites = parse(TEXT)
    for i, question_suite in enumerate(question_suites):
        correct_choice = question_suite.correct_choice
        relative_correct_choice = question_suite.choice_arrangement.index(
            correct_choice
        )
        print(f"{i+1}. {ANS_CHAR[relative_correct_choice+1]}")

    FILE.close()

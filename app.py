import json
import sys
import random
import os
from colorama import init, Fore, Back, Style


""" Colorama colors
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
"""

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def render_question(question: dict, answered = False, selected_answer = -1):
    cls()
    
    print(Fore.CYAN + question["question"] + Style.RESET_ALL)
    if not answered:
        for answer in question["answers"]:
                print(answer)
    else:
        correct = question["correct"]
        for i in range(len(question["answers"])):
            if correct != selected_answer and i == selected_answer:
                print(Fore.RED + question["answers"][i] + Fore.RESET)
                continue
            if i == correct:
                print(Fore.GREEN + question["answers"][i] + Fore.RESET)
                continue
            print(question["answers"][i])

def renderall(questions: list, answers: list, selected_answers: list):
    cls()
    for i in range(len(questions)):
        print("\n")
        if answers[i]:
            print(Back.WHITE + Fore.GREEN + questions[i]["question"] + Style.RESET_ALL)
        else:
            print(Back.WHITE + Fore.RED + questions[i]["question"] + Style.RESET_ALL)
        
        correct = questions[i]["correct"]
        for j in range(len(questions[i]["answers"])):
            if correct != selected_answers[i] and j == selected_answers[i]:
                print(Fore.RED + questions[i]["answers"][j] + Fore.RESET)
                continue
            if j == correct:
                print(Fore.GREEN + questions[i]["answers"][j] + Fore.RESET)
                continue
            print(questions[i]["answers"][j])
            
def test(questions: list, sim = False):

    answers = []
    selected_answers = []
    for i in range(len(questions)):
        answers += [False]

        render_question(questions[i])
        
        selected_answer = str(input(Fore.YELLOW + "\nAnswer: " + Fore.RESET))
        while selected_answer not in ('a', 'b', 'c'):
            render_question(questions[i])
            selected_answer = str(input(Fore.YELLOW + "\nAnswer: " + Fore.RESET))
        
        selected_answer = ord(selected_answer) - 97
        selected_answers += [selected_answer]
        if selected_answer == questions[i]["correct"]:
            answers[i] = True
        if not sim:
            render_question(questions[i], answered=True, selected_answer=selected_answer)
            input(Fore.YELLOW + "\nPress any key to continue..." + Fore.RESET)
    
    cls()
    
    fails = 0
    for answer in answers:
        if not answer:
            fails += 1
                
    if sim:
        
        print(Fore.CYAN + "Test simulation result: " + Fore.RESET)
        
        
        if fails > 2:
            print(Fore.RED + "FAIL" + Fore.RESET)
        else:
            print(Fore.GREEN + "SUCCESS" + Fore.RESET)
        print(Fore.CYAN + "Correct answers: " + Fore.RESET + f"{20-fails}/20")
    else:
        print(Fore.CYAN + "Correct answers: " + Fore.RESET + f"{20-fails}/20")
        
    input(Fore.YELLOW + "\nPress any key to see your answers... " + Fore.RESET)    
    renderall(questions, answers, selected_answers)

def show_help():
    print("Help")
    
def sim(seed, data: dict):

    random.seed(a=seed, version=2)
    
    questions = []
    
    for i in range(20):
        questions += [random.choice(data[str(random.randint(1, 7))]["questions"])]
    test(questions, True)
    
    


def Chapter_Test(Chapter: int, data: dict):
    questions = data[str(Chapter)]["questions"]
    test(questions, False)


if __name__ == "__main__":

    init()
   
    with open('data.json', encoding="utf8") as json_file:
        data = json.load(json_file)

    #print(data)
    arguments = sys.argv
    
    digits = []
    for x in range(1, 10):
        digits += [str(x)]

    
    if len(arguments) == 1:
        print("Invalid number of arguments passed.")
        show_help()
    elif arguments[1].lower() == "help":
        show_help()
    elif arguments[1].lower() == "sim":
        if len(arguments) > 2:
            seed = arguments[2]
            sim(seed, data)
        else:
            sim(None, data)
    elif arguments[1] in digits:
        Chapter_Test(int(arguments[1]), data)
    else:
        print("Invalid arguments passed.")
        show_help()
    exit()

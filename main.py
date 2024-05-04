from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
import random
import json
import html

#https://opentdb.com/api.php?amount=50&type=multiple
def read_file(filename:str):
    with open(filename) as my_file:
        return str(my_file.read())

def write_file(filename:str,filecontent:str):
    with open(filename,'w') as my_file:
       my_file.write(filecontent)
def pop_up(self,title,text=''):
    dialog = MDDialog(title=title,text=text,size_hint=(0.8, 0.3))
    dialog.open()



def count_question():
    s = json.loads(read_file('triviascores.text').replace("'", '"'))
    s['questions'] += 1
    write_file('triviascores.text', str(s))
def questions():

    q = json.loads(read_file('trivia.text'))
    q = random.choice(q)
    q = random.choice(q['results'])
    question = html.unescape(q['question'])
    correct_answer = html.unescape(q['correct_answer'])
    choices = q['incorrect_answers']
    choices.append(correct_answer)
    random.shuffle(choices)
    c = []
    for i in choices:
        c.append(html.unescape(i))
    choices = c
    count_question()
    q['category'] = html.unescape(q['category'])
    global data
    data = [question,correct_answer,choices,q['category'],q['difficulty'].upper()]
    return [question,correct_answer,choices,q['category'],q['difficulty'].upper()]

data = questions()


def score(add=False):
    s = json.loads(read_file('triviascores.text').replace("'",'"'))
    if add:
        s['score'] += 1
        write_file('triviascores.text', str(s))
    return str(s['score'])



def change_all(self,data):
    self.root.ids.question.text = data[0]
    self.root.ids.choice1.text = data[2][0]
    self.root.ids.choice2.text = data[2][1]
    self.root.ids.choice3.text = data[2][2]
    self.root.ids.choice4.text = data[2][3]
    self.root.ids.category.text = data[3]
    self.root.ids.difficulty.text = data[4]
    self.root.ids.score.text = score()
    s = json.loads(read_file('triviascores.text').replace("'", '"'))
    self.root.ids.total_questions.text = "Total Trivia Questions Asked: " + str(s['questions'])

class Main(MDApp):
    def build(self):
        self.title='Trivia'
        self.theme_cls.theme_style = "Light"
        self.icon = 'trivia.png'
        change_all(self,data)


    def card_pressed(self,button,action):
        if 'choice' in action:
            for i in self.root.ids:
                if str(i) == action:
                    x = str(eval(f"self.root.ids.{i}.text"))
                    if x == data[1]:
                        pop_up(self,title="CORRECT!",text=data[0] + "\n" + "Correct Answer: " + data[1] + "\n+1 Score!")
                        score(True)

                        change_all(self,questions())
                        return

            pop_up(self,title="Incorrect!",text="X")
        if action == 'new_question':
            s = json.loads(read_file('triviascores.text').replace("'", '"'))
            s['questions'] -= 1
            write_file('triviascores.text', str(s))
            change_all(self,questions())
            pop_up(self,title="CHANGED THE QUESTION!",text="Goodluck!")

        if action == 'reset_score':
            s = json.loads(read_file('triviascores.text').replace("'", '"'))
            s['questions'] = 0
            s['score'] = 0
            write_file('triviascores.text', str(s))
            change_all(self, questions())
            pop_up(self,"Score Resetted!")



    def show_popup_help(self):
        pop_up(self,
        title="Greetings!",
        text="What is this?\nThis is a TRIVIA APP!\nTest your knowledge to a random questions!!\nSubmitted to Sir Wilz for the Finals Project\nSource Code: \nContact Me: tabigne.johnanthony.mcc@gmail.com\nDakoa akong grado sir huhuhu\nCredits to: Open Trivia DB \nThe trivia questions are from them!\nhttps://opentdb.com/\nhttps://opentdb.com/api.php?amount=50&type=multiple"
               )


if __name__ == "__main__":
    Main().run()
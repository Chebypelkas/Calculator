from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class CalculatorApp(App):
    def __init__(self):
        super().__init__()
        self.label = Label(pos_hint={'center_x': 0.5, 'center_y': 0.7}, size_hint=(0.25, 0.25), text='',
                           font_size=30)
        self.can_point = True

    def build(self):
        sc_manager = ScreenManager()
        screen = Screen()


        #  основной код
        #text_input = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.7}, size_hint=(0.2, 0.2))
        buttons = []
        button_size = 0.195
        text2 = ''
        for i in range(4):
            for j in range(4):
                if j == 3:
                    if i == 0:
                        text2 = '+'
                    elif i == 1:
                        text2 = '-'
                    elif i == 2:
                        text2 = '*'
                    elif i == 3:
                        text2 = '/'
                elif i == 3:
                    if j == 0:
                        text2 = '0'
                    elif j == 1:
                        text2 = '('
                    elif j == 2:
                        text2 = ')'
                else:
                    text2 = f'{j + 1 + 3 * i}'
                b = Button(pos_hint={'x': 0.11 + button_size * j, 'center_y': 0.4 - button_size/2.5 * i},
                           size_hint=(button_size, button_size/2.5), text=text2,
                           background_normal='button2.png')
                b.bind(on_press=self.button_down)
                buttons.append(b)

        b = Button(pos_hint={'x': 0.5 + button_size, 'center_y': 0.17 - button_size / 2.5},
                   size_hint=(button_size, button_size / 2.5), text='=',
                   background_normal='button2.png')
        b1 = Button(pos_hint={'x': 0.11 + 2*button_size, 'center_y': 0.17 - button_size / 2.5},
                   size_hint=(button_size, button_size / 2.5), text='c',
                   background_normal='button2.png')
        b2 = Button(pos_hint={'x': 0.11 + button_size, 'center_y': 0.17 - button_size / 2.5},
                    size_hint=(button_size, button_size / 2.5), text='cc',
                    background_normal='button2.png')
        b3 = Button(pos_hint={'x': 0.11, 'center_y': 0.17 - button_size / 2.5},
                    size_hint=(button_size, button_size / 2.5), text='.',
                    background_normal='button2.png')
        b.bind(on_press=self.calculate)
        b1.bind(on_press=self.del_char)
        b2.bind(on_press=self.del_all)
        b3.bind(on_press=self.button_down)
        buttons.append(b)
        buttons.append(b1)
        buttons.append(b2)
        buttons.append(b3)
        #screen.add_widget(text_input)
        for button in buttons:
            screen.add_widget(button)
        screen.add_widget(self.label)


        sc_manager.add_widget(screen)
        return sc_manager

    def button_down(self, *args):
        current = args[0]
        # проверка на пустую строку
        if len(self.label.text) == 0:
            # можно ставить - и цифры
            if current.text.isdigit() or current.text == '-' or current.text == '(':
                self.label.text += current.text
        #  можем ли ставить знаки после цифры
        elif self.label.text[-1].isdigit() and current.text != '(':
            self.after_digit(current)
        #  если последний символ не циферка
        elif not self.label.text[-1].isdigit():
            self.not_after_digit(current)

    def after_digit(self, current):
        if current.text == ')':
            if self.label.text.count('(') > self.label.text.count(')'):
                self.add_char(current)
        elif current.text == '.' and self.can_point:
            self.can_point = False
            self.add_char(current)
        elif current.text != '.':
            self.add_char(current)
            self.can_point = True

    def not_after_digit(self, current):
        #  если последний символ ( и кнопка -
        if self.label.text[-1] == '(' and current.text == '-':
            self.add_char(current)
        #  если кнопка цифра и последний символ не )
        elif current.text.isdigit() and self.label.text[-1] != ')':
            self.add_char(current)
        #  если последний символ ) и кнопка не () и не цифра
        elif self.label.text[-1] == ')' and current.text not in '().' and not current.text.isdigit():
            self.add_char(current)
        #  если кнопка ( и если последний символ не )
        elif current.text == '(' and self.label.text[-1] != ')':
            self.add_char(current)
        elif self.label.text[-1] == ')' and current.text == ')' and self.label.text.count('(') > self.label.text.count(')'):
            self.add_char(current)

    def add_char(self, current):
        if len(self.label.text.replace('\n', '')) % 20 == 0:
            self.label.text += '\n'
        self.label.text += current.text

    def del_char(self, *args):
        self.label.text = self.label.text[:-1]

    def del_all(self, *args):
        self.label.text = ''

    def calculate(self, *args):
        if self.label.text.count('(') == self.label.text.count(')') and self.label.text[-1] not in '-+*/':
            list_ = self.get_list()
            # if '(' in list_:
            #     if ')' in list_:
            #         number1 = list_.index('(') + 1
            #         number2 = list_.index(')')
            #         print(list_[int(number1):int(number2)])
            print(list_)
            solve = self.solve(list_)
            if int(solve) == solve:  # solve % 1 == 0
                self.label.text = str(int(solve))
            else:
                self.label.text = str(solve)

    @staticmethod
    def solve(list_: list) -> float:
        while len(list_) != 1:
            if '*' in list_:
                CalculatorApp.mul(list_)
            elif '/' in list_:
                CalculatorApp.div(list_)
            elif '-' in list_:
                CalculatorApp.minus(list_)
            elif '+' in list_:
                CalculatorApp.plus(list_)
        if type(list_[0]) is list:
            list_[0] = CalculatorApp.solve(list_[0])
        return list_[0]  # возвращает результат

    @staticmethod
    def action(list_: list, action: str):
        number1 = list_[list_.index(action) - 1]
        if type(number1) is list:
            number1 = CalculatorApp.solve(number1)
        number2 = list_[list_.index(action) + 1]
        if type(number2) is list:
            number2 = CalculatorApp.solve(number2)
        match action:
            case '+':
                list_[list_.index(action)] = number1 + number2
            case '-':
                list_[list_.index(action)] = number1 - number2
            case '*':
                list_[list_.index(action)] = number1 * number2
            case '/':
                list_[list_.index(action)] = number1 / number2
        list_[list_.index(action) - 1] = number1
        list_[list_.index(action) + 1] = number2

    @staticmethod
    def mul(list_: list):
        number1 = list_[list_.index('*') - 1]
        if type(number1) is list:
            number1 = CalculatorApp.solve(number1)
        number2 = list_[list_.index('*') + 1]
        if type(number2) is list:
            number2 = CalculatorApp.solve(number2)
        list_.remove(list_[list_.index('*') - 1])
        list_.remove(list_[list_.index('*') + 1])
        list_[list_.index('*')] = number1 * number2

    @staticmethod
    def div(list_: list):
        number1 = list_[list_.index('/') - 1]
        if type(number1) is list:
            number1 = CalculatorApp.solve(number1)
        number2 = list_[list_.index('/') + 1]
        if type(number2) is list:
            number2 = CalculatorApp.solve(number2)
        list_.remove(list_[list_.index('/') - 1])
        list_.remove(list_[list_.index('/') + 1])
        list_[list_.index('/')] = number1 / number2

    @staticmethod
    def minus(list_: list):
        number1 = list_[list_.index('-') - 1]
        if type(number1) is list:
            number1 = CalculatorApp.solve(number1)
        number2 = list_[list_.index('-') + 1]
        if type(number2) is list:
            number2 = CalculatorApp.solve(number2)
        list_.remove(list_[list_.index('-') - 1])
        list_.remove(list_[list_.index('-') + 1])
        list_[list_.index('-')] = number1 - number2

    @staticmethod
    def plus(list_: list):
        number1 = list_[list_.index('+') - 1]
        if type(number1) is list:
            number1 = CalculatorApp.solve(number1)
        number2 = list_[list_.index('+') + 1]
        if type(number2) is list:
            number2 = CalculatorApp.solve(number2)
        list_.remove(list_[list_.index('+') - 1])
        list_.remove(list_[list_.index('+') + 1])
        list_[list_.index('+')] = number1 + number2

    def get_list(self) -> list:
        list_ = []
        number = ''
        stack = [list_]
        for char in self.label.text:
            print(f'label.text: {self.label.text}')
            print(f'char: {char}')
            print(f'stack: {stack}')
            print(f'number: {number}')
            print(f'list: {list_}')
            print('-------------')
            if char.isdigit():
                number += char
            else:
                if char == '(':
                    stack.append(list())  # добавляем новый список в стек
                elif char == ')':
                    if number != '':
                        stack[-1].append(float(number))
                        number = ''
                    new_list = stack.pop()  # вырезал список
                    stack[-1].append(new_list)  # вставляю список
                elif char == '.':
                    number += '.'
                else:  # если знак не скобка
                    if len(stack[-1]) == 0 or type(stack[-1][-1]) is not list:
                        if number == '':
                            stack[-1].append(0)
                        else:
                            stack[-1].append(float(number))
                    stack[-1].append(char)
                    number = ''
        else:
            if number != '':
                stack[-1].append(float(number))
        print(list_)
        return list_


if __name__ == '__main__':
    calculator = CalculatorApp()
    calculator.run()


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window             # to change the color of app window
import operator


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)      #



Builder.load_file(resource_path("my.kv"))
# set app size
Window.size = (400,600) #(500, 700)

# refer python to the kv file


class MyLayout(Widget):

    def calculation(self):
        """will split the expression by the operator, will store operator in digit var and
         using operator lib will  the match operation, returns result, needs import operator"""
        expression = self.ids.calc_input.text   # assign the input, this will include both numbers
        operators_ = {"+": operator.add,
                      "-": operator.sub,
                      "x": operator.mul,
                      "/": operator.truediv,     # '%': operator.mod
                      }
        if "." in expression:
            for digit in expression:
                if digit in operators_:
                    try:
                        num1, num2 = expression.split(digit)
                        result = operators_[digit](float(num1), float(num2))
                        return result

                    except ValueError:
                        pass
        else:
            for digit in expression:
                if digit in operators_:
                    try:
                        num1, num2 = expression.split(digit)
                        result = operators_[digit](int(num1), int(num2))
                        return result

                    except ValueError:
                        pass

    def math_operation(self, operator_):

        oper_list = ["x", "-", "/", "+"]
        count_operators = []     # here we collect the operators to count them
        previous_value = self.ids.calc_input.text   # the number before operator is asigned
        for char in previous_value:
            if char in oper_list:
                count_operators.append(char)   # if char is an operator added to the list to count

        if len(count_operators) > 0:           # if we have more than one operator, print just number
            result = self.calculation()
            self.ids.calc_input.text = f'{result}{operator_}'


        elif len(count_operators) == 0:        # if there are no operators, print number and operator
            self.ids.calc_input.text = f'{previous_value}{operator_}'

        #elif len(count_operators) == 1:
            #result = self.calculation()
            #self.ids.calc_input.text = f'{result}'
    def equals(self):
        result = self.calculation()
        self.ids.calc_input.text = f'{result}'

    def clear(self):
        """ display  0 in the calc screen when CE is pressed """
        self.ids.calc_input.text = "0"
        self.ids.display_entered.text = "0"

        """ displays the corresponding number in the calc screen, when number is 
         pressed if value is 0 exchange to number, else add new number at end """

    def number_pressed(self, number):
        previous_value = self.ids.calc_input.text

        if previous_value == "0":                            # if input screen =0
            self.ids.calc_input.text = ""
            self.ids.calc_input.text = f"{number}"          # prints to input screen
            # self.ids.display_entered.text = f'{number}'    # prints to small screen the value of number we pressed

        else:                               # else add the number at the end of the string
            self.ids.calc_input.text = f'{previous_value}{number}'
            self.ids.display_entered.text = f'{previous_value}{number}'

    def decimal_dot(self):
        previous_value = self.ids.calc_input.text
        ope = ["x", "-", "/", "+", "%"]
        dot_num = False
        dot_num1 = False
        dot_num2 = False
        operator_sign = False
        sing = ""

        for element in ope:
            if element in previous_value:
                sing += element
                operator_sign = True

        if operator_sign is True:             # there are 2 numbers
            num1, num2 = previous_value.split(sing)

            if "." in num1:
                dot_num1 = True
            if "." in num2:
                dot_num2 = True
        else:   # if there is only one number
            if "." in previous_value:
                dot_num = True

        if dot_num is True:      # there is no sign, only one number that has a dot
            self.ids.calc_input.text = f'{previous_value}'
        else:               #elif dot_num is False:
            self.ids.calc_input.text = f'{previous_value}.'
        if dot_num1 is True and dot_num2 is False:       # there is a sign and the first number has a dot
            self.ids.calc_input.text = f'{previous_value}.'
        elif dot_num1 is True and dot_num2 is True:
            self.ids.calc_input.text = f'{previous_value}'

    """
            self.ids.calc_input.text = f'{previous_value}'
        elif dot_num1 is False:
            self.ids.calc_input.text = f'{previous_value}.'
        elif dot_num2 is True:       # there is a sign and the first number has a dot
            self.ids.calc_input.text = f'{previous_value}'
        elif dot_num2 is False:
            self.ids.calc_input.text = f'{previous_value}.'
    """

    def back_space(self):
        previous_value = self.ids.calc_input.text
        numbers = previous_value
        self.ids.calc_input.text = f'{numbers[:-1]}'

    def plus_minus(self):
        previous_value = self.ids.calc_input.text

        if "-" in previous_value:
            self.ids.calc_input.text = f'{previous_value.replace("-"," ")}'
        else:
            self.ids.calc_input.text = f'-{previous_value}'

    def percent(self):
        previous_value = self.ids.calc_input.text
        operator_sign = False
        sign = ""
        ope = ["x", "-", "/", "+"]

        for element in ope:
            if element in previous_value:   # is there an operation?
                sign += element
                operator_sign = True  # there are 2 numbers

        if operator_sign is True:  # if there are 2 numbers split them
            num1, num2 = previous_value.split(sign)
            num2 = float(num2) / 100
            self.ids.calc_input.text = f'{num1}{sign}{num2}'

        else:        # there is no operation
            #if "." in previous_value:
            num1 = float(previous_value) / 100
            self.ids.calc_input.text = f'{num1}'





class CalculatorApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1)
        return MyLayout()


if __name__ == "__main__":
    CalculatorApp().run()
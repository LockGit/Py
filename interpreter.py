# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-12-18 15:21:43
# @Last Modified by:   lock
# @Last Modified time: 2017-12-18 15:40:25

class Interpreter:
    def __init__(self):
        self.stack = []

    def load_value(self, number):
        self.stack.append(number)

    def print_answer(self):
        answer = self.stack.pop()
        print(answer)

    def add_two_values(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def run_code(self, what_to_execute):
            instructions = what_to_execute["instructions"]
            numbers = what_to_execute["numbers"]
            for each_step in instructions:
                instruction, argument = each_step 
                if instruction == "load_value":
                    number = numbers[argument]
                    self.load_value(number)
                elif instruction == "add_two_values":
                    self.add_two_values()
                elif instruction == "print_answer":
                    self.print_answer()

interpreter = Interpreter()
what_to_execute = {
    "instructions": [("load_value", 0),
                     ("load_value", 1),
                     ("add_two_values", None),
                     ("print_answer", None)],
    "numbers": [7, 5] }
interpreter.run_code(what_to_execute)                    
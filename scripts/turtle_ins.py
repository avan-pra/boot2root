#!/usr/bin/python3

import turtle
import time

s = turtle.getscreen()
t = turtle.Turtle()

def forward(instruction):
    t.forward(int(instruction.split(' ')[1]))

def backward(instruction):
    t.backward(int(instruction.split(' ')[1]))

def rotate(instruction):
    direction = instruction.split(' ')[1]
    if direction == 'gauche':
        t.left(int(instruction.split(' ')[3]))
    if direction == 'droite':
        t.right(int(instruction.split(' ')[3]))


def main():
    with open('turtle', 'r') as fd:
        for instruction in fd:
            if instruction != '':
                if 'Avance' in instruction.split(' ')[0]:
                    forward(instruction)
                elif 'Recule' in instruction.split(' ')[0]:
                    backward(instruction)
                elif 'Tourne' in instruction.split(' ')[0]:
                    rotate(instruction)
                else:
                    print('pause 5')
                    time.sleep(5)
                    t.clear()
            else:
                print('pause 10')
                time.sleep(10)
    print('end')
    time.sleep(10)

if __name__ == '__main__':
    main()



import re

word = 'Keyboard.readInt("HOW MANY NUMBERS?'


words = [s for s in re.split(r"(\W)", word) if s != '']


print(words)
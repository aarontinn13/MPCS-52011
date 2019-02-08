text = ['52', 'hello']

for i in text:
    try:
        x = int(i)
        print(x)
    except ValueError:
        print('cannot turn into integer')



x = '165'
y = 'hello'
print(x.isalpha())
print(y.isalpha())
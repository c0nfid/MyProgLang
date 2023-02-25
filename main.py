import Lex
import math

text = '''for (i = 03; i < n; i != 35)'''
print(Lex.lexAnalys(text))


def vectorr(a):
    return abs(a ** 2 - 1 - 51 * a ** 3) ** 3
def main(lst):
    def vector(a):
        return abs(a ** 2 - 1 - 51 * a ** 3) ** 3

    res = 0
    for i in range(1, len(lst) +1):
        res += vector(lst[len(lst) - 1 - math.ceil(i//3)])
        print(len(lst) -1 - math.ceil(i//3))

    print(res)
    return res

main([0.87, -0.54, 0.18, 0.65])
print(vectorr())

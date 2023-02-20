import Lex


text = '''for (i = 1; i < n; i += 5) {
    if (i > 5) a+=1;
    else a-=1;
}
l = 4534534536.234564563453453453453453'''
t = (Lex.run(text))
for i in t:
    a = []
    for g in i:
        a.append(str(g))
    print(a)
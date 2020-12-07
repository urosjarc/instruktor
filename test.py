# 10.3
seznam = ['Pravo', 'Racunalnistvo', 'Programiranje', 'Sociologija', 'Psihologija']
print(seznam[1])
seznam.insert(2, "Informatika")
seznam.append("Statistika")
seznam.remove("Pravo")
print(seznam[-1])
seznam[seznam.index("Statistika")] = 'Matematika'
print(seznam)
print(sorted(seznam))
nov_seznam = seznam.copy()
seznam.pop(len(seznam)-1)
print(seznam[1:-1])
seznam.clear()
print(seznam)
del seznam

# 10.4
for st_zvezdic in [5, 2, 5, 2, 2]:
    print('*'*st_zvezdic)

# 10.5
import random
seznam = []
for i in range(100):
    seznam.append(random.randint(1, 999))
print(seznam)
for i in range(len(seznam)):
    st = seznam[i]
    if st % 2 != 0:
        print(st, end=', ')

# 10.5
cene = []
while True:
    st = float(input("Vnesi ceno izdelka: "))
    if st < 0:
        break

    cene.append(st)

print(max(cene), sum(cene))

# 10.7
seznam = [ "korenje", "jabolka", "rdeca pesa", "koleraba", "zelje", "zelena solata", "mango", "hrušk"]
nov_seznam = []
for ele in seznam:
    if 'L' in ele:
        nov_seznam.append(ele)
print(nov_seznam)

# 10.8
casi = []
while True:
    cas = float(input("Vnesi cas tekaca: "))
    if cas < 0:
        break

    casi.append(cas)
casi.sort()
print("Prvo mesto:", casi[0])
print("Drugo mesto:", casi[1])
print("Tretje mesto:", casi[2])



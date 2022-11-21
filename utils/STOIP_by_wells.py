#Automaticaly recalculate=true
#Single model=false
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/voronov.txt") as voron:
    stroka=0
    for line in voron:
        stroka+=1
#рассчитаем сколько пластов в файле через максимум в fipnum
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/fipnum.txt") as fip:
    maxfip=0
    for i in range(stroka):
        s=fip.readline()
        s=s.split()
        s=int(float(s[3]))
        if s>maxfip:
            maxfip=s
    maxfip+=1
#найдем количество регионов воронова через значение max
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/voronov.txt") as voron:
    maximum=0
    for i in range(stroka):
        s=voron.readline()
        s=s.split()
        s=int(float(s[3]))
        if s>maximum:
            maximum=s
    maximum+=1 #прибавим 1 что бы при использовании range число было maximum
    
zap=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas.txt")#открытие файла 1.тхт как объект zap
fip=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/fipnum.txt")#открытие файла 2.тхт как объект fip
voron=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/voronov.txt") #открытие файла

spisok=[0]*maximum #создаем пустой список по количеству кругов воронова
#создаем двумерный список
for i in range(maximum):
    spisok[i]=[0]*maxfip# по коичеству фипнамов
#читаем по строчке файлы и заполн¤ем массив
for i in range(stroka):
    fiplin=fip.readline()#читает по строчкам объект fip
    zaplin=zap.readline()#читает по строчкам объект zap
    voronlin=voron.readline()
    lisf=fiplin.split() #создает список из строчки флине
    lisz=zaplin.split()
    lisv=voronlin.split()
    #суммирование запасов по ¤чейкам
    spisok[int(float(lisv[3]))][int(float(lisf[3]))]+=float(lisz[3])

#определим какие скважины относ¤тс¤ к каждому кругу воронова
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/Well.txt","r", encoding="utf-8") as well:
    s=well.readlines()
    well_voron=[""]*len(s)
    for i in range(1, len(s)):
        well_voron[int(float(s[i].split()[4]))]+=s[i].split()[0]
    
#выводим и записываем в файл rezult
rezult=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/rezultat.txt", "w") #дл¤ записи результата
for i in range(maximum):
    f=" "
    for j in range(maxfip):
        f=f+"\t"+ str(round(spisok[i][j],1))
    d="\n"+str(well_voron[i])+"\t"+f
    rezult.write(d)
zap.close()
fip.close()
voron.close()
rezult.close()
print("готово")

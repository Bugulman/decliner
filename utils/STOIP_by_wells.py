#Automaticaly recalculate=true
#Single model=false
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/voronov.txt") as voron:
    stroka=0
    for line in voron:
        stroka+=1
#���������� ������� ������� � ����� ����� �������� � fipnum
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/fipnum.txt") as fip:
    maxfip=0
    for i in range(stroka):
        s=fip.readline()
        s=s.split()
        s=int(float(s[3]))
        if s>maxfip:
            maxfip=s
    maxfip+=1
#������ ���������� �������� �������� ����� �������� max
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/voronov.txt") as voron:
    maximum=0
    for i in range(stroka):
        s=voron.readline()
        s=s.split()
        s=int(float(s[3]))
        if s>maximum:
            maximum=s
    maximum+=1 #�������� 1 ��� �� ��� ������������� range ����� ���� maximum
    
zap=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas.txt")#�������� ����� 1.��� ��� ������ zap
fip=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/fipnum.txt")#�������� ����� 2.��� ��� ������ fip
voron=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/voronov.txt") #�������� �����

spisok=[0]*maximum #������� ������ ������ �� ���������� ������ ��������
#������� ��������� ������
for i in range(maximum):
    spisok[i]=[0]*maxfip# �� ��������� ��������
#������ �� ������� ����� � �������� ������
for i in range(stroka):
    fiplin=fip.readline()#������ �� �������� ������ fip
    zaplin=zap.readline()#������ �� �������� ������ zap
    voronlin=voron.readline()
    lisf=fiplin.split() #������� ������ �� ������� �����
    lisz=zaplin.split()
    lisv=voronlin.split()
    #������������ ������� �� �������
    spisok[int(float(lisv[3]))][int(float(lisf[3]))]+=float(lisz[3])

#��������� ����� �������� ������� � ������� ����� ��������
with open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/Well.txt","r", encoding="utf-8") as well:
    s=well.readlines()
    well_voron=[""]*len(s)
    for i in range(1, len(s)):
        well_voron[int(float(s[i].split()[4]))]+=s[i].split()[0]
    
#������� � ���������� � ���� rezult
rezult=open("D:/project/Minnib_project/SCHED_PATTERNS/zapas/rezultat.txt", "w") #�� ������ ����������
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
print("������")

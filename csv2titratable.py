#!/usr/bin/python3

import csv


atom1 = [] 
atom2 = [] 
charge1 = []
totcharge1 = 0
charge2 = []
totcharge2 = 0
protcnt = [2,3]
#pka = 9.5

residue = "CP4"

csv.register_dialect('myDialect',
delimiter = ',',
skipinitialspace=True)
line = 0

with open('CP4.csv', 'r') as csvFile:
    reader = csv.reader(csvFile, dialect='myDialect')
    for row in reader:
#       print (len(row))
        if (line==0):
             pka = (float)(row[0])
        if (line==1):
             for col in range(0,len(row)):
                if (row[col]=="Charge"):
                     col1=col
#                    print (col1)
        elif (line>1):
#            print (row)
             temp=row[0]
             atom1.append(temp.strip()) 
             charge1.append((float)(row[2])) 
             temp=row[3]
             atom2.append(temp.strip()) 
             charge2.append((float)(row[5])) 
        line = line + 1

print ("")
print ("# {:3s}".format(residue))
print ("refene1 = _ReferenceEnergy(igb1=0, igb2=0, igb5=0, igb7=0, igb8=0)")
print ("refene1.solvent_energies(igb1=0, igb2=0, igb5=0, igb7=0, igb8=0)")
print ("refene1.dielc2_energies(igb1=0, igb2=0, igb5=0, igb7=0, igb8=0)")
print ("refene1.dielc2.solvent_energies(igb1=0, igb2=0, igb5=0, igb7=0, igb8=0)")
print ("refene2 = _ReferenceEnergy(igb2=1.0, igb5=0, igb7=0, igb8=0) # Implicit ")
print ("refene2.solvent_energies(igb2=1.0, igb5=0, igb7=0, igb8=0) # Explicit ")
print ("refene2.dielc2_energies()")
print ("refene2.dielc2.solvent_energies()")
print ("# Copying the reference energy to be printted on the old CPIN format") 
print ("refene1_old = _ReferenceEnergy(igb2=-1.0, igb5=0, igb8=0)") 
print ("refene1_old.solvent_energies(igb2=-1.0, igb5=0)")
print ("refene1_old.dielc2_energies(igb2=-1.0, igb5=0)") 
print ("refene1_old.dielc2.solvent_energies()")
print ("refene1_old.set_pKa({:.2f}, deprotonated=False)".format(pka))
print ("")

#PRN = TitratableResidue('PRN',
#                        ['CA', 'HA1', 'HA2', 'CB', 'HB1', 'HB2', 'CG',
#                        'O1', 'O2', 'H11', 'H12', 'H21', 'H22'], pka=4.85, typ="ph")


print ("{:3s} = TitratableResidue('{:3s}',[".format(residue, residue), end=''),
for i in range(0,len(charge1)):
    if((i+1)%5):
        print("'{:s}'".format(atom1[i]), end=''), 
    else:
        print("'{:s}',".format(atom1[i])), 

    if ((i<len(charge1)-1) and ((i+1)%5)):
        print (",", end='') 
print ("]", end='')
print (", pka={:.2f}, typ=\"ph\")".format(pka))

print ("")

print ("{:3s}".format(residue),end=''),
print (".add_state(protcnt={:d}, refene=refene2, refene_old=refene2, pka_corr=0.0, # deprotonated".format(protcnt[0]))

print ("charges=[", end=''),

for i in range(0,len(charge1)):
    if((i+1)%5):
        print("{:.4f}".format(charge1[i]), end=''), 
    else:
        print("{:.4f},".format(charge1[i])), 

    totcharge1 = totcharge1 + charge1[i]
    if ((i<len(charge1)-1) and ((i+1)%5)):
        print (",", end='') 
print ("])")

print ("")

print ("{:3s}".format(residue),end=''),
print (".add_state(protcnt={:d}, refene=refene1, refene_old=refene1_old, pka_corr={:.2f}, # protonated".format(protcnt[1],pka))

print ("charges=[", end=''),

for i in range(0,len(charge2)):
    if((i+1)%5):
        print("{:.4f}".format(charge2[i]), end=''), 
    else:
        print("{:.4f},".format(charge2[i])), 

    totcharge2 = totcharge2 + charge2[i]
    if ((i<len(charge2)-1) and ((i+1)%5)):
        print (",", end='') 
print ("])")

print ("")

#PRN.add_state(protcnt=0, refene=refene1, refene_old=refene1, pka_corr=0.0, # deprotonated
#              charges=[-0.0508, -0.0173,
#              -0.0173, 0.0026, -0.0425, -0.0425, 0.8054, -0.8188, -0.8188, 0.0,
#              0.0, 0.0, 0.0])

print ("{:3s}.check()".format(residue)),
print ("")

print ("Totcharge1 = {:f}".format(totcharge1))
print ("Totcharge2 = {:f}".format(totcharge2))

csvFile.close()


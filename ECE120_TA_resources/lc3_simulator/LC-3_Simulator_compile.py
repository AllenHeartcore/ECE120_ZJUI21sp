# -*- coding: utf-8 -*-

def hex2bin(hexstr):
    binstr=bin(int(hexstr[1:],16))[2:]
    return '0'*(16-len(binstr))+binstr

def verify(command):
    if len(command)==16 and command.count('0')+command.count('1')==16:
        return command,True
    elif len(command)==5 and command[0]=='x':
        try:
            command=hex2bin(command)
        except:
            return '',False
        else:
            return command,True
    else:
        return '',False

sourceFile=open('lab11.txt')
sourceCode=sourceFile.readlines()
sourceFile.close()
compilable=True
for lineNum in range(len(sourceCode)):
    line=sourceCode[lineNum]
    line=line.split(';')[0].replace(' ','')
    command,valid=verify(line)
    if valid==True or line=='':
        sourceCode[lineNum]=command
    else:
        compilable=False
        break
    
if compilable==True:
    objectFile=open('lab11_compiled.bin','w')
    for line in sourceCode:
        if line!='':objectFile.write(line+'\n')
    objectFile.close()
    print('Compilation succeed.')
else:
    print('Compilation failed.')

# -*- coding: utf-8 -*-

"""
    <LC-3 Simulator>
    By Chen, Ziyuan
        Electrical and Computer Engineering, ZJUI Institute, 
        International Campus, Zhejiang University. 
    Copyright 2021 Chen, Ziyuan. All rights reserved. 
    For academic use only. Any form of commercial use is prohibited. 
    
    Version history: 
        Created  on Tue Feb 16 12:15:00 2021 (Version 1.0)
        Modified on Tue Feb 16 20:30:00 2021 (Version 1.1)
        Updated  on Sat Feb 20 19:20:00 2021 (Version 2.0)
        Modified on Sun Feb 21 11:10:00 2021 (Version 2.1)
        Updated  on Tue Apr 20 16:00:00 2021 (Version 3.0)
        Modified on Wed Apr 21 16:30:00 2021 (Version 3.1)
"""

import numpy

opcodes=['BR', 'ADD','LD', 'ST',
         'JSR','AND','LDR','STR',
         'RTI','NOT','LDI','STI',
         'JMP','RES','LEA','TRAP']
Register=['0000000000000000','0111111111111111',
          '0000000000000000','0000000000000000',
          '0000000000000000','0000000000000000',
          '0000000000000000','0000010010010000']
Memory={}
PC ='0000010010010100'
IR ='1011000110101110'
PSR='0000010000000000'
N=0;Z=1;P=0;
command_count=1
operating=True
subroutine=False

def SEXT(binstr):
    return binstr[0]*(16-len(binstr))+binstr

def bin2hex(binstr):
    hexstr=hex(int(SEXT(binstr),2))[2:].upper()
    return 'x'+'0'*(4-len(hexstr))+hexstr

def hex2bin(hexstr):
    binstr=bin(int(hexstr[1:],16))[2:]
    return '0'*(16-len(binstr))+binstr

def ALU_ADDer(operand1,operand2):
    operand=numpy.zeros([16,3])
    result0=numpy.zeros(16)
    for i in range(16):
        operand[i,1]=operand1[i]
        operand[i,2]=operand2[i]
    for i in range(15,-1,-1):
        calc=sum(operand[i])
        result0[i]=calc%2
        if i!=0:
            operand[i-1,0]=calc//2
    result=''
    for i in range(16):
        result+=str(int(result0[i]))
    return result

def ALU_ANDer(operand1,operand2):
    result=''
    for i in range(16):
        result+='1' if operand1[i]=='1' and operand2[i]=='1' else '0'
    return result

def increment(varName):
    return ALU_ADDer(varName,'0000000000000001')

def getMemory(addr):
    if addr in Memory.keys():
        return Memory[addr]
    else:
        return '0000000000000000'

def evalNZP(result):
    def setNZP(tN,tZ,tP):
        globals()['N']=tN
        globals()['Z']=tZ
        globals()['P']=tP
        return None
    if result[0]=='1':
        setNZP(1,0,0)
    else:
        if result[1:]=='000000000000000':
            setNZP(0,1,0)
        else:
            setNZP(0,0,1)
    return None

def syntaxError(message):
    globals()['command_count']-=1
    print(message)
    return None

def ADD(instr):
    DR=int(instr[0:3],2)
    SR1=int(instr[3:6],2)
    if instr[6]=='0':
        if instr[7:9]=='00':
            SR2=int(instr[9:12],2)
            result=ALU_ADDer(Register[SR1],Register[SR2])
            Register[DR]=result
            evalNZP(result)
            print('   ADD : R%d <- R%d+R%d'%(DR,SR1,SR2))
        else:
            syntaxError('   ADD : Syntax 0001DDDSSS000SSS error.')
    else:
        SR2=instr[7:12]
        result=ALU_ADDer(Register[SR1],SEXT(SR2))
        Register[DR]=result
        evalNZP(result)
        print('   ADD : R%d <- R%d+%d'%(DR,SR1,int(SR2,2)))
    return None

def AND(instr):
    DR=int(instr[0:3],2)
    SR1=int(instr[3:6],2)
    if instr[6]=='0':
        if instr[7:9]=='00':
            SR2=int(instr[9:12],2)
            result=ALU_ANDer(Register[SR1],Register[SR2])
            Register[DR]=result
            evalNZP(result)
            print('   AND : R%d <- R%d&R%d'%(DR,SR1,SR2))
        else:
            syntaxError('   AND : Syntax 0101DDDSSS000SSS error.')
    else:
        SR2=instr[7:12]
        result=ALU_ANDer(Register[SR1],SEXT(SR2))
        Register[DR]=result
        evalNZP(result)
        print('   AND : R%d <- R%d&(%s)'%(DR,SR1,bin2hex(instr[7:12])))
    return None

def NOT(instr):
    if instr[6:12]=='111111':
        DR=int(instr[0:3],2)
        SR=int(instr[3:6],2)
        result=''
        for i in range(16):
            result+='1' if Register[SR][i]=='0' else '0'
        Register[DR]=result
        evalNZP(result)
        print('   NOT : R%d <- ~R%d'%(DR,SR))
    else:
        syntaxError('   NOT : Syntax 1001DDDSSS111111 error.')
    return None

def LD(instr):
    DR=int(instr[:3],2)
    PCoffset9=instr[3:]
    Addr=ALU_ADDer(PC,SEXT(PCoffset9))
    result=getMemory(Addr)
    Register[DR]=result
    evalNZP(result)
    print('   LD  : R%d <- M[PC+%s=%s]'\
          %(DR,bin2hex(PCoffset9),bin2hex(Addr)))
    return None

def LDR(instr):
    DR=int(instr[:3],2)
    BaseR=int(instr[3:6],2)
    offset6=instr[6:]
    Addr=ALU_ADDer(Register[BaseR],SEXT(offset6))
    result=getMemory(Addr)
    Register[DR]=result
    evalNZP(result)
    print('   LDR : R%d <- M[R%d+%s=%s]'\
          %(DR,BaseR,bin2hex(offset6),bin2hex(Addr)))
    return None

def LDI(instr):
    DR=int(instr[:3],2)
    PCoffset9=instr[3:]
    Addr=ALU_ADDer(PC,SEXT(PCoffset9))
    result=getMemory(getMemory(Addr))
    Register[DR]=result
    evalNZP(result)
    print('   LDI : R%d <- M[M[PC+%s=%s]]'\
          %(DR,bin2hex(PCoffset9),bin2hex(Addr)))
    return None

def LEA(instr):
    DR=int(instr[:3],2)
    PCoffset9=instr[3:]
    Addr=ALU_ADDer(PC,SEXT(PCoffset9))
    result=Addr
    Register[DR]=result
    evalNZP(result)
    print('   LEA : R%d <- PC+%s=%s'\
          %(DR,bin2hex(PCoffset9),bin2hex(Addr)))
    return None

def ST(instr):
    SR=int(instr[:3],2)
    PCoffset9=instr[3:]
    Addr=ALU_ADDer(PC,SEXT(PCoffset9))
    Memory[Addr]=Register[SR]
    print('   ST  : M[PC+%s=%s] <- R%d'\
          %(bin2hex(PCoffset9),bin2hex(Addr),SR))
    return None

def STR(instr):
    SR=int(instr[:3],2)
    BaseR=int(instr[3:6],2)
    offset6=instr[6:]
    Addr=ALU_ADDer(Register[BaseR],SEXT(offset6))
    Memory[Addr]=Register[SR]
    print('   STR : M[R%d+%s=%s] <- R%d'\
          %(BaseR,bin2hex(offset6),bin2hex(Addr),SR))
    return None

def STI(instr):
    SR=int(instr[:3],2)
    PCoffset9=instr[3:]
    Addr=ALU_ADDer(PC,SEXT(PCoffset9))
    Memory[Memory[Addr]]=Register[SR]
    print('   STI : M[M[PC+%s=%s]] <- R%d'\
          %(bin2hex(PCoffset9),bin2hex(Addr),SR))
    return None

def BR(instr):
    execute=False
    if instr[0]=='1' and globals()['N']==1:execute=True
    if instr[1]=='1' and globals()['Z']==1:execute=True
    if instr[2]=='1' and globals()['P']==1:execute=True
    if execute==True:
        PCoffset9=instr[3:]
        globals()['PC']=ALU_ADDer(globals()['PC'],SEXT(PCoffset9))
        print('   BR  : PC <- PC+%s'%bin2hex(PCoffset9))
    else:
        conditions=['','p','z','zp','n','np','nz','nzp']
        print('   BR  : Condition BR%s unsatisfied.'\
              %conditions[int(instr[:2],2)])
    return None

def JMP(instr):
    if instr[:3]=='000' and instr[6:]=='000000':
        BaseR=int(instr[3:6],2)
        globals()['PC']=Register[BaseR]
        if BaseR!=7:
            print('   JMP : PC <- R%d'%BaseR)
        else:
            if globals()['subroutine']==True:
                globals()['subroutine']=False
                print('   RET : PC <- R7 (subroutine %s)'\
                      %bin2hex(Register[7]))
            else:
                print('   RET : Currently not in subroutine. Skipped.')
    else:
        syntaxError('   JMP : Syntax 1100000RRR000000 error.')
    return None

def TRAP(instr):
    def SEXT8(binstr):
        return '0'*(8-len(binstr))+binstr
    trapVect=instr[4:]
    if instr[:4]=='0000':
        if trapVect=='00100000':
            print('   TRAP: Trap Vector x20 (GETC)',end='')
            char=input('   ')
            Register[0]='00000000'+SEXT8(bin(ord(char[0]))[2:])
        elif trapVect=='00100001':
            print('   TRAP: Trap Vector x21 (OUT)')
            print('   %c'%chr(int(Register[0][8:],2)))
        elif trapVect=='00100010':
            print('   TRAP: Trap Vector x22 (PUTS)')
            print('   Printing a string, starting from M[%s].\n   '\
                  %bin2hex(Register[0]),end='')
            pointer=Register[0]
            while True:
                data=getMemory(pointer)
                if data!='0000000000000000':
                    print('%c'%chr(int(data[8:],2)),end='')
                else:
                    break
                pointer=increment(pointer)
            print()
        elif trapVect=='00100011':
            print('   TRAP: Trap Vector x23 (IN)',end='')
            char=''
            while len(char)!=1:
                char=input('   Please input 1 character: ')
            print("   The inputted character is '%c'."%char)
            Register[0]='00000000'+SEXT8(bin(ord(char))[2:])
        elif trapVect=='00100100':
            print('   TRAP: Trap Vector x24 (PUTSP)')
            print('   Printing a string, starting from M[%s].\n   '\
                  %bin2hex(Register[0]),end='')
            pointer=Register[0]
            while True:
                data=getMemory(pointer)
                if data[8:]!='00000000':
                    print('%c'%chr(int(data[8:],2)),end='')
                else:
                    break
                if data[:8]!='00000000':
                    print('%c'%chr(int(data[:8],2)),end='')
                else:
                    break
                pointer=increment(pointer)
            print()
        elif trapVect=='00100101':
            print('   TRAP: Trap Vector x25 (HALT)')
            globals()['operating']=False
        else:
            hexstr=hex(int(trapVect,2))[2:].upper()
            hexstr='x'+'0'*(2-len(hexstr))+hexstr
            syntaxError('   TRAP: Trap Vector %s undefined.'%hexstr)
    else:
        syntaxError('   TRAP: Syntax 11110000TRAPVECT error.')
    return None

def JSR(instr):
    if globals()['subroutine']==False:
        globals()['subroutine']=True
        Register[7]=globals()['PC']
        if instr[0]=='1':
            PCoffset11=instr[1:]
            globals()['PC']=ALU_ADDer(globals()['PC'],SEXT(PCoffset11))
            print('   JSR : R7 <- PC, PC <- PC+%s=%s'\
                  %(bin2hex(PCoffset11),bin2hex(globals()['PC'])))
        else:
            if instr[1:3]=='00' and instr[6:]=='000000':
                BaseR=int(instr[3:6],2)
                globals()['PC']=Register[BaseR]
                print('   JSRR: R7 <- PC, PC <- R%d (subroutine %s)'\
                      %(BaseR,bin2hex(Register[7])))
            else:
                syntaxError('   JSRR: Syntax 0100000RRR000000 error.')
    else:
        if instr[0]=='1':
            print('   JSR : Already in subroutine. Skipped.')
        else:
            print('   JSRR: Already in subroutine. Skipped.')
    return None

'''
def RTI(instr):
    if instr=='000000000000':
        # Placeholder, pp. 549
    else:
        syntaxError('   RTI : Syntax 1000000000000000 error.')
    return None
'''

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

def compileFile(file,name):
    try:
        sourceCode=file.readlines()
        file.close()
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
            objectFile=open(name+'.lc3_script','w')
            for line in sourceCode:
                if line!='':objectFile.write(line+'\n')
            objectFile.close()
            print('   Compilation succeed. ',end='')
            print('Script file name is "%s.lc3_script".'%name)
        else:
            print('   Compilation failed.')
    except:
        print('   Unsupported file format.')
    return None

def loadMemory(file):
    commands=file.readlines()
    file.close()
    pointer=commands[0][:-1]
    for command in commands[1:]:
        Memory[pointer]=command[:-1]
        pointer=increment(pointer)
    globals()['PC']=commands[0][:-1]
    printStatus()
    return None

def execute(stepwise):
    globals()['N']=0
    globals()['Z']=1
    globals()['P']=0
    globals()['command_count']=1
    globals()['operating']=True
    globals()['subroutine']=False
    while True:
        command=getMemory(globals()['PC'])
        globals()['IR']=command
        print('\n   Command #%03d is %s (%s).'\
                  %(command_count,bin2hex(command),command))
        if command=='0000000000000000':
            print('   NOP : Skipped.')
        else:
            globals()[opcodes[int(command[:4],2)]](command[4:])
            if operating==False:
                print('   Execution halted.')
                break
        globals()['PC']=increment(globals()['PC'])
        globals()['command_count']+=1
        if stepwise==True:
            printStatus()
            input('>>Press "Enter" to continue.')
    return None

def printStatus():
    print('\n   <System Variables>')
    print('      PC:    %s (%s)'%(bin2hex(PC),PC))
    print('      IR:    %s (%s)'%(bin2hex(IR),IR))
    #print('      PSR:   %s (%s)'%(bin2hex(PSR),PSR))
    NZPcode=str(N)+str(Z)+str(P)
    if NZPcode=='100':print('      CC:    NEGATIVE')
    if NZPcode=='010':print('      CC:    ZERO')
    if NZPcode=='001':print('      CC:    POSITIVE')
    print('   <Register File>')
    for i in range(8):
        print('      R%d:    %s (%s)'\
              %(i,bin2hex(Register[i]),Register[i]),end='')
        if i!=7:
            print()
        else:
            if globals()['subroutine']==True:
                print(' [Subroutine]')
            else:
                print()
    print('   <Memory>')
    empty=True
    for addr in sorted(Memory,key=lambda x:x[0]):
        val=Memory[addr]
        if val!='0000000000000000':
            empty=False
            print('      %s: %s (%s)'%(bin2hex(addr),bin2hex(val),val))
    if empty==True:
        print('                /* EMPTY */')
    return None

print('\n\n************* LC-3 Simulator **************')
print('********** Author: Chen, Ziyuan ***********')
print('*** ZJUI Institute, Zhejiang University ***')
print('\n<Type "quit" at any time to quit simulation.>')
printStatus()

while True:
    fileName=input('>>Source or script (.lc3_script) file name:  ').strip()
    if fileName!='quit':
        try:
            file=open(fileName)
        except FileNotFoundError:
            print('   File not found.')
        else:
            if fileName[-11:]=='.lc3_script':
                loadMemory(file)
                print('\n>>Memory initialization complete.\n  ',end='')
                while True:
                    print('Type "continue" to execute program, ',end='')
                    action=input('  or "step" to execute step by step:  ')
                    if action=='continue':
                        execute(False)
                        printStatus()
                        break
                    elif action=='step':
                        execute(True)
                        break
                    elif action=='quit':
                        break
                    else:
                        print('   Undefined command.\n\n>>',end='')
            else:
                compileFile(file,fileName[:-4])
    else:
        print('   Simulation terminated.')
        break


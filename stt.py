
print('importieren...')

from time import sleep
import speech_recognition as sr
import threading as th
import pyttsx3
import datetime
import pywhatkit
import os
import wikipedia
from pynput.keyboard import Key, Controller

print('define...')

NAME = 'robo'.lower()

keyboard = Controller()
pycomm = ['variable','definition','klasse','class','klass','importiere','import','wenn','ansonsten','if','else']
wikipedia.set_lang("de")
module = {'python':True}
p = False
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
pyfile = ''
buffer = ''

def take_command2(x=0):
    i = input(">>> ")
    sleep(1)
    return i

def talk2(text):
    print(text)



def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command(x=0):
    global p, t
    command = ''
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            if not p and not x:
                t = th.Thread(target=run)
                t.start()
            if not p:
                command = listener.recognize_google(voice,language='de_DE')
    except Exception as e:
        print(e)
    return command


def run():
    global p, t
    if p:
        return
    command = take_command()
    print(command)
    if 'stopp' == command.lower():
        for i in module.keys():
            module[i] = False
        talk('gestoppt')
        p = True
    if NAME in command.lower():
        command = command.lower()
        command = command.replace(NAME+' ', '')
        print(command)
        if 'play' in command.lower() or 'spiel' in command.lower():
            command = command.replace('spiel','')
            song = command.replace('play', '')
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'google ' in command:
            command = command.replace('google ','')
            pywhatkit.search(command)
        elif 'time' in command.lower() or 'zeit' in command.lower():
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        elif 'deaktiviere ' in command:
            command = command.replace('deaktiviere ','')
            if command in module.keys():
                print(command+' inaktiv')
                module[command] = False
        elif 'aktiviere ' in command:
            command = command.replace('aktiviere ','')
            if command in module.keys():
                print(command+' aktiv')
                module[command] = True
        elif 'was ist ' in command or 'wer ist ' in command or 'was bedeutet ' in command:
            command = command.replace('was ist ','')
            command = command.replace('wer ist ','')
            command = command.replace('was bedeutet ','')
            try:
                info = wikipedia.summary(command, 1)
                print(info)
                talk(info)
            except:
                talk('kenn ich nicht')
        
    else:
        for i in module.keys():
            if module[i]:
                print(i+"('"+command+"')")
                exec(i+"('"+command+"')")

def python(x):
    global buffer, pyfile, pycomm
    
    if pyfile == '':
        x = x.lower()
        if 'neu ' in x:
            x = x.replace('neu ','')
            pyfile = x+'.py'
            if os.path.isfile(pyfile):
                talk('do you want to overwrite the existing file?')
                command=take_command(1)
                if 'yes' in command.lower():
                    e = open(pyfile,'w')
                    e.close()
                    os.startfile(pyfile, r'editwithidle\shell\edit37')
                else:
                    os.startfile(pyfile, r'editwithidle\shell\edit37')
            else:
                e = open(pyfile,'w')
                e.close()
                os.startfile(pyfile, r'editwithidle\shell\edit37')
        elif 'lade ' in x:
            x = x.replace('lade ','')
            pyfile = x+'.py'
            if os.path.isfile(pyfile):
                os.startfile(pyfile, r'editwithidle\shell\edit37')
            else:
                talk('diese datai existiert nicht')
    else:
        inx = []
        werte = []
        x_c = x
        x = x.lower()
        x = x.split(' ')
        data = saveandget()
        zeile = 0
        for i in pycomm:
            if i in x:
                inx.append(i)
        if inx != []:
            
            text = get_text(pyfile)
            if 'in der zeile ' in x_c.lower():
                zeile = int(x[x.index('zeile')+1])
            if len(inx) == 1:
                name = x[x.index(inx[0]) + 1]
                if ' mit den ' in x_c.lower():
                    werte = x[x.index('den')+2:]
                elif ' mit dem ' in x_c.lower():
                    werte = [x[x.index('dem')+2]]
                elif ' mit der ' in x_c.lower():
                    werte = [x[x.index('mit')+3]]
                if 'und' in werte:
                    werte.remove('und')
                print('neue ' + inx[0] +' '+ name+' mit dem/den wert/werten '+ str(werte))
                if inx[0] == 'variable':
                    if len(werte) == 0:
                        type_it(zeile,0,name+ ' = 0\r')
                    if len(werte) == 1:
                        type_it(zeile,0,name+ ' = '+werte[0]+'\r')
                    elif len(werte)>1:
                        type_it(zeile,0,name+ ' = '+str(werte)+'\r')
                if inx[0] == 'definition':
                    type_it(zeile,0,'def '+name+ '('+str(werte).replace('[','').replace(']','')+'):\r')
                if inx[0] == 'klasse':
                    w = ''
                    for i in werte:
                        w += ', '+i
                    w2 = ''
                    for i in werte:
                        w2+='self.'+i+' = '+i+'\r'
                    type_it(zeile,0,'class '+name+ ':\rdef __init__(self'+w+'):\r'+w2)
            elif len(inx) == 2:
                name1 = x[x.index(inx[0]) + 1]
                name2 = x[x.index(inx[1]) + 1]
                print(inx)
                if ' mit den ' in x_c.lower():
                    werte = x[x.index('den')+2:]
                elif ' mit dem ' in x_c.lower():
                    werte = [x[x.index('dem')+2]]
                elif ' mit der ' in x_c.lower():
                    werte = [x[x.index('mit')+3]]
                if 'und' in werte:
                    werte.remove('und')
                if 'klasse' in inx and 'definition' in inx:
                    name1 = x[x.index('klasse') + 1]
                    name2 = x[x.index('definition') + 1]
                    try:
                        w = data.split('class '+name1+':\n')[1]
                    except:
                        talk('nicht gefunden')
                        return
                    w = w.split('\n')
                    f = False
                    if zeile == 0:
                        f = True
                    for i in w:
                        if '    ' in i or i.replace(' ','') == '':
                            pass
                        elif f:
                            f = False
                            zeile = i
                    
                    if f:
                        zeile = len(data.split('\n'))
                    else:
                        w = data.split('\n')
                        zeile = w.index(zeile)+1
                    

                    w = ''
                    for i in werte:
                        w += ', '+i
                        
                    w2 = ''
                    for i in werte:
                        w2+='self.'+i+' = '+i+'\r'
                    type_it(zeile,0,'\tdef '+name2+'(self'+w+'):\r'+w2)
                        
                
            elif len(inx) > 2:
                namen = []
                for i in inx:
                    namen.append(x[x.index(i) + 1])
                


def saveandget():
    keyboard.press(Key.ctrl.value)
    keyboard.press('s')
    keyboard.release('s')
    keyboard.release(Key.ctrl.value)
    return get_text(pyfile)

def type_it(zeile,spalte,text):
    go_to(zeile,spalte)
    keyboard.type(text)

def go_to(zeile,spalte):
    keyboard.press(Key.ctrl.value)
    keyboard.press(Key.home.value)
    keyboard.release(Key.home.value)
    keyboard.release(Key.ctrl.value)
    for i in range(zeile-1):
        keyboard.press(Key.down.value)
        keyboard.release(Key.down.value)
    for i in range(spalte):
        keyboard.press(Key.right.value)
        keyboard.release(Key.right.value)

def delete_all(text=''):
    keyboard.press(Key.ctrl.value)
    keyboard.press('a')
    keyboard.release('a')
    keyboard.release(Key.ctrl.value)
    keyboard.press(Key.backspace.value)
    keyboard.release(Key.backspace.value)
    keyboard.type(text)

def delete(x,forward=True):
    if forward:
        for i in range(x):
            keyboard.press(Key.delete.value)
            keyboard.release(Key.delete.value)
    else:
        for i in range(x):
            keyboard.press(Key.backspace.value)
            keyboard.release(Key.backspace.value)
    
def get_text(path):
    e = open(path,'r')
    output = e.read()
    e.close()
    return output

print('finisched')

run()


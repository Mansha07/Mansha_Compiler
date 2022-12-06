from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as box
from xml.sax import _create_parser

fileptr = [False, 0]

class MainWIndow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background='#eed')
        self.parent = parent
        self.initUI()
        self.initQuitButton()
        self.initInputText()
        self.initOutputText()
        self.initLabels()
        self.initGenerateButton()
        self.initInfoLabel()
        
    def initUI(self):        
        self.parent.title('SynCom')
        self.pack(fill=BOTH, expand=1)
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        self.parent.geometry('500x500+%d+%d' % ((sw - 500)/2, (sh - 500)/2))
        
    def initQuitButton(self):
        quitButton = Button(self, text = "Quit", command = self.quit)
        quitButton.place(relx = 0.8, rely = 0.93, relwidth = 0.1)
        
    def initGenerateButton(self):
        genButton = Button(self, text = "Generate table", command = self.invokeParser)
        genButton.place(relx = 0.32, rely = 0.93, relwidth = 0.2)
        
    def initInputText(self, textParam=''):
        self.inputText = Text(self)
        self.inputText.place(relx = 0.08, rely = 0.07, relwidth = 0.7, relheight = 0.25)
        self.inputText.insert(index = INSERT, chars = textParam)
                
    def initLabels(self):
        l1 = Label(self, text = "Input Grammar", background='#eed')
        l2 = Label(self, text = "Output Parsing Table", background='#eed')        
        l1.place(relx = 0.2, rely = 0.02, relwidth = 0.3)
        l2.place(relx = 0.2, rely = 0.35, relwidth = 0.3)
                
    def initInfoLabel(self, textParam = "Information: ", flag = 1):
        if flag == 1:
            l3 = Label(self, text = textParam, background='#3f3')
        else:
            l3 = Label(self, text = textParam, background='#a77')
        l3.place(relx = 0.79, rely = 0.1, relwidth = 0.2)    
        
    def initOutputText(self, textParam=''):
        self.outputText = Text(self)
        self.outputText.place(relx = 0.08, rely = 0.4, relwidth = 0.7, relheight = 0.50)
        self.outputText.insert(index = INSERT, chars = textParam)
        
    def invokeParser(self):
        #call to generateparser code module

        parsingtable = _create_parser(self.inputText.get( '0.0', END)) 
        
        outputText = ''
        
        #print("---"*40)
        outputText +="---"*35
        for i in parsingtable:
            outputText +="\n "
            for j in parsingtable[i]:
                for k in parsingtable[i][j]:
                
                    outputText += "[ "+i+ ","+j+ " ]" "::" +k+ ' '
            outputText +="\n " 
            outputText +="---"*35               
        print('outputText:', outputText)
        self.initOutputText(outputText)
        infoString = 'Success!\nThe parsing\ntable has been\nsuccessfully\ncreated' 
        self.initInfoLabel(infoString, flag = 1)
                    
    
def main():
    root = Tk()
    app = MainWIndow(root)
    root.mainloop()

#First Follow
firstset={}
followset={}
parsingtable={}

class FirstFollow:
    def __init__(self,gram,ter,nonter,start):#need to pass the grammar here..
        self.gram=gram
        self.term=ter
        self.nonterm=nonter
        self.start=start
 
    def first(self,ip):
        fir=[]
        ctr=0
        length=0
        if(ip in self.term):
            fir.extend(ip)
        else:
            for i in self.gram[ip]:
                # print('1')
                #print(i[0],":",i,"::")
                if(i[0] in self.term):
                    #print('2')
                    #print(i[0])
                    #print(ctr)
                    fir.extend(i[0])
                else:
                    #print('3')
                    length=len(i)
                    while(ctr<length):
                        #print('4')
                        if('n' in self.gram[i[ctr]]):   # 'n' is for null symbol
                                #print('5')
                                #print(ctr)
                                fir.extend(self.first(i[ctr]))
                                #print(fir)
                                ctr+=1
                                #print(ctr)
                        else:
                                #print('6')
                                
                                fir.extend(self.first(i[ctr]))
                                #print(fir)
                                #print(ctr)
                                break
        firstset[ip]=fir
        return fir

    def follow(self,ip):
        foll=[]
        if(ip==self.start):
            foll.extend('$')
        for key in self.gram.keys():#iterating thorugh the keys of the grammar
            vals=self.gram[key]
            #print('1')
            #print('key',key)
            #print('vals',vals)
            for each in vals:
                #print('2')
                #print('each',each)
                ctr=0
                length=len(each)
                #print('len',length)
                for j in each:
                    #print('3')
                    #print('j',j)
                    if(j==ip):
                        #print('4')
                        if(ctr<length-1):
                            #print('5')
                            if((ip != key)and('n'in self.first(each[ctr+1]))):
                                #print('6')
                                for x in self.first(each[ctr+1]):
                                    if((x not in foll)and(x!='n')):
                                        foll.extend(x)
                                for x in self.follow(key):
                                    if((x not in foll)and(x!='n')):
                                        foll.extend(x)
                                #print('foll',foll)
                            else:
                                #print('7')
                                for x in self.first(each[ctr+1]):
                                    if((x not in foll)and(x!='n')):
                                        foll.extend(x)
                                #print('foll',foll)
                        if((ip != key)and(ctr==length-1)):
                            #print('8')
                            for x in self.follow(key):
                                if((x not in foll)and(x!='n')):
                                    foll.extend(x)
                            #print('foll',foll)
                    ctr+=1
                ctr=0
        followset[ip]=foll
        return foll
      
    def parsingtable(self,ip):
        #print(self.gram)
        
        for i in self.gram[ip]:
            #print("+++",i)
            #print(i[0],":",i,"::",ip)   
            if ip not in parsingtable: 
                parsingtable[ip]={}
                
            elif i[0] in self.term and i[0]!='n':
                
                if i[0] not in parsingtable[ip]:
                    parsingtable[ip][i[0]]=[]
                parsingtable[ip][i[0]].append(str(ip +" -> "+ i))
            elif i == 'n':
                
                for k in followset[ip]:
                    if k not in parsingtable[ip]: 
                        parsingtable[ip][k]=[]
                    parsingtable[ip][k].append(str(ip +" -> "+ i))
            else:
                
                for k in firstset[ip]:
                    if k not in parsingtable[ip]: 
                        parsingtable[ip][k]=[]
                    parsingtable[ip][k].append(str(ip + " -> "+i))
        
        for i in self.term :
            
            if i not in parsingtable[ip] and i!="n":
                parsingtable[ip][i]=[]
                parsingtable[ip][i].append("Error")
                      
    def printparser(self):
        print("---"*40)
        for i in self.nonterm:
            for j in self.term:
                if j!='n':
                    for k in parsingtable[i][j]:
                
                        print("[",i, ",",j, "]",":",k,end=" ")
            print("")
            print("---"*30)
       
def createparser(text):
    text = text.split('\n')

    t=text[0]
    t =t.split(",,")
    dict={}
    for i in t:
        print(i[0])
        dict[i[0]]=[i[3:-1]]
        k=i[3:-1].split(",")
        dict[i[0]]=k

    terminals=list(text[1].split(","))
    nonterminals=list(text[2].split(","))
    start=text[3]
    print(terminals,nonterminals,start)
    a=FirstFollow(dict,terminals,nonterminals,start)
    #a.findset()
    nont=nonterminals
    # print('FOLLOW :',"e " ,a.first('E'))
    for i in nont:
        fi=a.first(i)
        fo=a.follow(i)
        firstset[i]=fi
        followset[i]=fo
        
    
    print(firstset)
    print(followset)
    for i in nont:
        a.parsingtable(i)
    
    a.printparser()
    return parsingtable


try:
    main()

except Exception as e:
    print(e)
finally:
    print("Parsing table successfully created")



from tkinter import*
import re 
root = Tk()

count = 0
def oneLineLexer(string):
    print(string)
    # if the string contains words or A-Z characters then print(identifier)
    if(re.findall(r'[A-Z|a-z]+\d?', string)):
        identifier = re.findall(r'[A-Z|a-z]+\d?', string)
        for iD in identifier:
            output_window.insert(END, "{identifier,%s}\n" % iD)

    # if the string contains operators: =, +, or >, then print(operator)
    if(re.findall(r'(=|\+|>|<|-)', string)):
        operator = re.findall(r'(=|\+|>|<|-)', string)
        for op in operator:
            output_window.insert(END, "{operator,%s}\n" % op)
    # if the string contains literals: numbers, then print(literals)
    if(re.findall(r'[^A-Z|a-z|>|\s][0-9]+', string)):
        literal = re.findall(r'[^A-Z|a-z|>|\s][0-9]+', string)
        for lit in literal:
            if lit[0] == "=":
                output_window.insert(END, "{identifier,%s}\n" % lit[1:])
            else:
                output_window.insert(END, "{literal,%s}\n" % lit)

    # if the string contains separators: (),:, "", then print(separators)
    if(re.findall(r'(:|\(|\)|\"|\")', string)):
        separator = re.findall(r'(:|\(|\)|\"|\")', string)
        for sep in separator:
            output_window.insert(END, "{sep,%s}\n" % sep)
    return

def copyInput():
    global count
    count += 1

    temp = input_window.get("1.0", END)
    textStr = temp
    textList = textStr.split("\n")
    # pass count and textList to outputText:

    outputText(count, textList)
    return
    

#Purpose: Prints the output source onto the output window.
def outputText(count, textList): 
    if count < len(textList):
       # output_window.insert(END, str(textList[count - 1])) + "\n")
        oneLineLexer(str(textList[count - 1]))
        counterLabel.config(text = count)
        #analyzeInput(textList)
    return

# Purpuse: Quits the window
def quitWindow():
    root.destroy()



# center window:
root.title("LexCom: Lexical Analyzer")
root.update_idletasks()
width = 500
height = 500
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry("{}x{}+{}+{}".format(width, height, x, y))
    
# Input Label:
inputLabel = Label(root, text = "Input Source Code:", font=("Arial", 15), fg = "black")
inputLabel.grid(row = 0, column = 0, sticky = W)

# Input Window:
input_window = Text(root, height = 10, width = 28, bg = "white", highlightbackground = "black" )
input_window.grid(row = 1, column = 0, sticky = W)


# Next Line button:    
nextButton = Button(root, text = "Compute", command = copyInput, font=("Arial", 15), relief=RAISED, bg="blue", fg="white")
nextButton.grid(row = 2, pady=5, column = 1, sticky = W)


# Current Line Label:
lineLabel = Label(root, text = "Current Line Tokenized:", font=("Arial", 15), fg = "black")
lineLabel.grid(row = 3, column = 0, pady=10, sticky = W)

# Counter Label:
counterLabel = Label(root, font=("Arial", 15), fg = "red")
counterLabel.grid(row = 3, column = 1,   sticky = W)

# Output Label:
outputLabel = Label(root, text = "Output:",font=("Arial", 15), fg = "green")
outputLabel.grid(row = 0, column = 1, sticky = W)

# Output Window:
output_window = Text(root, height = 10, width = 30, bg = "white", highlightbackground = "black" )
output_window.grid(row = 1, column = 1, sticky = E)

# run main
root.mainloop()
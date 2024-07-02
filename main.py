
import platform
import webbrowser

version = "1.0.0 7-2-2024 (initial release)" # major.minor.build

# non-changing
numbers = "1234567890."
letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

# changing
debugmessages = False
userinput = ""
lexerdata = [] 
lexerdatatypes = []
parserdata = []
variablenames = ["input"]
variablevalues = [""]
args = []
argtypes = []

functions = ["log", "takeinput", "quit", "add", "join", "debug"]
keywords = ["var"]

def run(func):
    global args, argtypes, variablevalues, variablenames, takeinputvalue

    debugmessage("running function " + func)
    for i in range(0, len(args)):
        debugmessage("replacing substitute variables in args ")
        try:
            if argtypes[i] == "variable":
                for j in range(0, len(variablenames)):
                    if args[i] == variablenames[j]:
                        args[i] = variablevalues[j]
        except:
            argumenterror(args[i])

    try:
        debugmessage("executing function " + func)
        if func == "log":
            print(args[0], end="")
        elif func == "takeinput":
            variablevalues[0] = input()
        elif func == "add":
            print(numberprocessor(args[0])+numberprocessor(args[1]))
        elif func == "join":
            print(str(args[0])+str(args[1]))
        elif func == "debug":
            debugmessage("\x1b[0m\x1b[43m(USER)\x1b[0m\x1b[33m " + args[0])
    except:
        warning(func + " function doesn't have enough arguments!")

def debugmessage(message):
    if debugmessages == True:
        print("\x1b[33m⚠ debug: " + message + "\x1b[0m")

def lexer():
    global lexerdata, lexerdatatypes, userinput, variablenames

    debugmessage("lexer process begun")
    
    lexerdata = []
    lexerdatatypes = []
    letter = 0

    while letter+1 < len(userinput):
        processing = ""
        isstring = False
        termtype = "unknown"

        # read term
        while letter+1 < len(userinput) and ((userinput[letter] != " " and userinput[letter] != "\n") and isstring == False) or isstring == True:
            if userinput[letter] != "\"":
                processing = processing + userinput[letter]
            else:
                isstring = not isstring
                if isstring:
                    termtype = "string"
            letter += 1
            try:
                if userinput[letter] == ";" and isstring == False:
                    break
            except:
                parsingerror()
        if userinput[letter] != " " and userinput[letter] != ";" and userinput[letter] != "\n":
            processing = processing + userinput[letter]

        lexerdata.append(processing)
        debugmessage("lexer found term: " + processing)

        # classify type of term
        if termtype != "string":

            # is it a number?
            for i in range(0, len(numbers)):
                if numbers[i] in processing:
                    termtype = "number"

            # is it a word?
            for i in range(0, len(letters)):
                if letters[i] in processing:
                    termtype = "word"
        
            # is it a function?
            if processing in functions:
                termtype = "function"
        
            # is it a keyword?
            if processing in keywords:
                termtype = "keyword"
        
            # is it a terminator?
            if processing == ";":
                termtype = "terminator"

            # is it a variable?
            if processing in variablenames:
                termtype = "variable"
        
        lexerdatatypes.append(termtype)
        debugmessage("lexer categorized term \"" + processing + "\" as \"" + termtype + "\"")

        # skip spaces
        while (userinput[letter] == " " or userinput[letter] == "\n") and letter < len(userinput):
            letter += 1

def parser():
    global parserdata, lexerdatatypes, lexerdata

    parserdata = []

    debugmessage("parser process begun")

    for i in range(0, len(lexerdatatypes)):
        if lexerdatatypes[i] == "terminator":

            if lexerdata[i+1] == ";":
                parserdata.append("program end")
                break

            elif lexerdata[i+1] == "var":
                parserdata.append("variable")
            
            elif lexerdatatypes[i+1] == "function":
                parserdata.append("function")
            
            else:
                undefinederror(lexerdata[i+1])
            
            debugmessage("parser determined line")

def interpreter():
    global args, argtypes

    debugmessage("interpreter process begun")

    line = -1
    lineindex = 0
    args = []
    argtypes = []
    func = ""
    # print(parserdata)
    # print(lexerdata)
    # print(lexerdatatypes)

    # ❗❗❗ DON'T TOUCH THIS UNLESS YOU REALLY REALLY REALLY KNOW WHAT YOU'RE DOING!!!!!!!! IT WORKS OMG HOW DID I GET IT TO WORK!!!!!!!!!!
    # ❗❗❗ EXTREMELY FRAGILE!!!!!!!!!!! LIKE SERIOUSLY IT'S RIDICULOUS HOW FRAGILE THIS IS!!!!!!!!!!!!!
    for i in range(0, len(lexerdata)):
        if lexerdatatypes[i] == "terminator":
            if parserdata[line] == "function":
                if func == "quit":
                    exit()
                else:
                    run(func)
            line += 1
            lineindex = 0
            args = []
        else:
            if parserdata[line] == "function":
                if lineindex == 0:
                    func = lexerdata[i]
                else:
                    if lexerdatatypes[i] != "word":
                        args.append(lexerdata[i])
                        argtypes.append(lexerdatatypes[i])
                    else:
                        parsingerror()
            elif parserdata[line] == "variable":
                if lineindex == 1:
                    variablenames.append(lexerdata[i])
                    if lexerdatatypes[i+1] != "terminator":
                        variablevalues.append(lexerdata[i+1])
                    else:
                        variablevalues.append("")
            else:
                undefinederror(lexerdata[i])
            lineindex += 1

def numberprocessor(num):
    val = ""
    for i in range(0, len(str(num))):
        val = val + str(num[i])
    try:
        return int(val)
    except:
        return float(val)

def undefinederror(term):
    print("\x1b[31m\x1b[1mundefinederror: term \"" + term + "\x1b[31m\x1b[1m\" is not defined\x1b[0m")
    exit()

def argumenterror(term):
    print("\x1b[31m\x1b[1margumenterror: " + term + " is not recognized\x1b[0m")
    exit()

def parsingerror():
    print("\x1b[31m\x1b[1mparsingerror: i have zero idea what you're trying to say...\x1b[0m")
    exit()

def namingerror(term):
    print("\x1b[31m\x1b[1namingerror: name " + term + " is taken\x1b[0m")

def userintervene():
    print("\x1b[31m\x1b[1m\nuserintervene: the program has been interrupted by the user!\x1b[0m")
    exit()

def warning(message):
    print("\x1b[35m\x1b[1mwarning: \x1b[31m" + message + "\x1b[0m")

def main():
    global userinput

    print("\x1b[35m\x1b[1m" + platform.system().lower() + " " + platform.release().lower() + " \x1b[0mdetected. goodmorning ver. " + version + " created and developed by breakfast on git.gay. type \"about creator\" to learn more. type \"help\" to view the official documentation. hope you enjoy! :)")
    
    while True:
        userinput = "; " + input("\n// ") + " ;;"

        if userinput == "; about creator ;;":
            webbrowser.open("https://git.gay/breakfast")
        elif userinput == "; help ;;":
            webbrowser.open("https://docs.google.com/document/d/1o4tGeCqOlJM4l9pAHDwWVZelZXanA_auUJE4fLR4ujw/edit?usp=sharing")
        else:
            try:
                lexer()
                parser()
                interpreter()
            except IndexError:
                parsingerror()

try:
    main()
except KeyboardInterrupt:
    userintervene()
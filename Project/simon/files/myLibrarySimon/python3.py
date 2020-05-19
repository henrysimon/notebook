import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tkinter import *
import time
import socket
socekt_Global1 = socket.socket()

vNew_Line = '\n'
vTab = '\t'
def sLoop(vExec_Command, xTimes, oObject):
    """loop with the provided command, use newline for multiple syntax
    oObject = object / class to parse, set args.isFinished = True (untuk break)
    xTimes = -1 (unlimited)
    q.sLoop(vCmd, 4, args)
    Eval
    """
    
    #pake ini buat exec variable local = exec("old_string = new_string", globals(), _locals)
    _locals = locals()

    b"contoh loop pake index"
#     arrRow = q.sSplit(vText, q.vNew_Line)
#     for i in range(len(arrRow)):
#         print(str(i) + " = " + arrRow[i])

    class cArgs :
        isFinished = False
        o = None
    
    args = cArgs()
    args.o = oObject
    isUlang = True
    i = 1
    while isUlang :
        exec(vExec_Command)
        if(args.isFinished == True) : break
        if(xTimes != -1) :
            if(i > (xTimes-1)) : isUlang = False
        i+=1

def sArray_2_String(oArr, vDelimiter):
    vReturn = ""
    try:
        vReturn = vDelimiter.join(oArr)
    except : vReturn = ""
    return vReturn

def sArray_Get(oArr, iID, vDefault = ""):
    vReturn = vDefault
    try:
        vReturn = oArr[iID]
    except: vReturn = vDefault
    return vReturn

def sArray_Find(arrInput, vFind):
    """find in array (return true or false if found)
    """
    return (vFind in arrInput)

def sArray_Find_Loc(arrText, vFind, isExact_Match = True):
    """find in array the location start from 0
    """
    iLoc_Return = -1
    try:
        if(isExact_Match == False):
            iLoc = 0
            for vText in arrText :
                if(sString_Find(vText, vFind)) : 
                    iLoc_Return = iLoc
                    break
                iLoc +=1
        else :
            iLoc_Return = arrText.index(vFind)
    except : qwe = 123
    return iLoc_Return

def sArray_Length(arrInput):
    return len(arrInput)

def sApplication_Get_Directory_Python_Main():
    """ini maksudnya main path dari Python_Main yah
    """
    import os
    vPath = os.path.dirname(os.path.realpath(__file__))
    vPath = os.path.dirname(vPath) #go up directory
    return vPath

def sApplication_Get_Directory_List_Project():
    """maksudnya yg list Pupuk, Python_Main (jadi kalo mau pilih project yg lain gampang)
    """
    import os
    vPath_Lib = sApplication_Get_Directory_Python_Main()
    vPath_List_Project = os.path.dirname(vPath_Lib)
    return vPath_List_Project

def sApplication_Get_Args_By_No(iID = -1, vDefault = ""):
    """get arguments from command prompt, mulai dari 0
    """
    import sys
    vReturn = vDefault
    if(iID == -1):
        vReturn = sArray_2_String(sys.argv, " ")
    else :
        vReturn = sArray_Get(sys.argv, iID, vDefault)
    return vReturn

def sApplication_Get_Args_By_Name(vName, vDefault = ""):
    """get arguments from command prompt by name
    ex: b.bat id=1 nama=2
    """
    import sys
    vReturn = vDefault
    vCMD = sArray_2_String(sys.argv, " ")
    vValue = sString_Get_Parameter_Content(vCMD, vName, "=", " ")
    if(vValue != "") : vReturn = vValue
    return vReturn

def sApplication_Get_Machine_Name():
    import socket
    vName = socket.gethostname()
    return vName

def sConnection_Get(vType, vHost, vDB_Name, vUser, vPassword):
    """type = MSSQL
    """
    import sqlalchemy
    import pymysql
    #     mssql+pyodbc://server_name/database_name?driver=SQL Server?Trusted_Connection=yes
    #     dialect+driver://username:password@host:port/database

    if(vType == "MSSQL") : vURL = "mssql+pyodbc://#USER#:#PASSWORD#@#HOST#:1433/#DB#?DRIVER={SQL Server}"
    elif (vType == "MYSQL") : vURL = "mysql+pymysql://#USER#:#PASSWORD#@#HOST#/#DB#"
    
    vURL = sString_Replace(vURL, "#USER#", vUser)
    vURL = sString_Replace(vURL, "#PASSWORD#", vPassword)
    vURL = sString_Replace(vURL, "#HOST#", vHost)
    vURL = sString_Replace(vURL, "#DB#", vDB_Name)
    oCon = sqlalchemy.create_engine(vURL)
    return oCon

def sConfig_Read(vName, vPath=""):
    ""
    if(vPath == "") : vPath = sApplication_Get_Directory_List_Project() + r"\zConfig\CodingConfig.txt"
    vText = sFile_Read(vPath)
    vValue = sString_Get_Parameter_Content(vText, vName)
    return vValue

def sConnection_Execute(oCon, vSQL):
    "execute and commit, karena biasanya dia gak commit"
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=oCon)
    session = Session()
    session.execute(vSQL)
    session.commit()
    session.close()

def Exit():
    """exit program / stop
    """
    exit()

def sDataframe_2_Collection_Counter(df, vCol = "words", vCounter = "counter"):
    "convert from dataframe to hashtable words = jumlah counternya"
    import collections
    c=collections.Counter()
    for i, oRow in df.iterrows():
        vWords = str(oRow[vCol])
        iCounter = int(oRow[vCounter])
        c[vWords] = iCounter
    return c

def sDataframe_Find_Row(df, vList_Col, vList_Find, vDelimiter):
    "find value in dataframe, return the row index"
    iLoc = -1
    arrFind = sSplit(vList_Find, vDelimiter)
    iTemp = 0
    oFound = df.copy()
    
    try:
        oTemp = None
        for vCol in sSplit(vList_Col, vDelimiter) :
            if(iTemp==0) : oTemp = (df[vCol]==arrFind[iTemp])
            else : oTemp = oTemp & (df["Path"]=="2") 
            iTemp+=1
        iLoc = df.loc[oTemp].index[0]
    except : qwe =123
    return iLoc

def sDataframe_from_Hash(oHash):
    """convert hashtable to dataframe (masih bukan array hashtablenya)
    """
    import pandas as pd
    oDict = {}
    vList = ""
    for vCol_Name in oHash:
        oDict[vCol_Name] = [oHash[vCol_Name]]
    df = pd.DataFrame(oDict)
    return df

def sDataframe_from_String(vText, vDelimiter_Col = ",", vDelimiter_Line = ";"):
    "create data frame from string"
    from io import StringIO
    import pandas as pd
    vText = sString_Replace(vText, vDelimiter_Line, vNew_Line)
    df = pd.read_csv(StringIO(vText), sep=vDelimiter_Col)
    return df

def sDataframe_Get_Columns(df, vDelimiter = ","):
    vList_Col = sArray_2_String(df.columns.tolist(), vDelimiter)
    return vList_Col

def sDataframe_Get_Dummies(oDF, vList_Column, vDefault = 0):
    """get dummies, and create column if not exist
    """
    import pandas as pd
    df = pd.get_dummies(oDF.copy())
    arrCol = sSplit(vList_Column, ",")
    for vCol in arrCol :
        if(vCol not in df) : df[vCol] = vDefault
    return df

def sDataframe_Read_Excel(vPath, vSheet, vCols = None):
    """read from excel, will replace NaN with empty string, and remove rows where first column is NAN
    cols = A:F
    """
    import pandas as pd
    df = None
    df = pd.read_excel(vPath, usecols = vCols, sheet_name=vSheet, index=False)
    vFirst_Col = sSplit(sDataframe_Get_Columns(df, ","), ",")[0]
    df.dropna(subset=[vFirst_Col], inplace=True)
    df = df.fillna('')
    return df

def sDataframe_Print(df):
    "print dataframe, can remove index"
    vCSV = df.to_csv(sep="\t", line_terminator=vNew_Line, index=False)
    print(vCSV)

def sDataframe_Replace_Float(oDF, vCol_Name, vList_Find, vList_Replace = "", vDelimiter=","):
    """will replace based on order, start from 0 (kalao vList_Value gak keisi
    """
    df = oDF.copy() 
    arrFind = sSplit(vList_Find, vDelimiter)
    iNil = 0
    for vFind in arrFind:
        vReplace = sSplit_Get(vList_Replace, vDelimiter, iNil, "")
        iReplace = 0
        if(vReplace == "") : iReplace = float(iNil+1)
        else : iReplace = float(vReplace)
        try: df[vCol_Name].replace({vFind: iReplace}, inplace=True)
        except: qwe = 123
        iNil+=1
    return df

def sDataframe_Upsert(df, vList_ID, oHash):
    """insert or update dataframe if hashtable exists
    hash = {}, hash[ID]=1
    """
    vList_Val = ""
    iTemp = 0
    vDelimiter = "+++==="
    oDF_New = df.copy()
    for vID in sSplit(vList_ID, ",") :
        vList_Val = sVBCLRF_Max_Line(vList_Val, oHash[vID], vDelimiter)
        iTemp += 1 
    iLoc = sDataframe_Find_Row(oDF_New, vList_ID, vList_Val, vDelimiter)
    if(iLoc > -1):
        oDF_New.loc[iLoc] = oHash
    else :
        oDF_New = oDF_New.append(oHash, ignore_index=True)
    return oDF_New

def sDate_Format(oDate, vFormat):
    """return date with requested format as string
    ex: vFormat YYYY/MM/DD HH:mm:ss EEE EE E
    DDDD, DDD = weekdays
    """
    vReturn = ""
    vFormat = sString_Replace(vFormat, "YYYY", "%Y")
    vFormat = sString_Replace(vFormat, "MMMM", "%B")
    vFormat = sString_Replace(vFormat, "MMM", "%h")
    vFormat = sString_Replace(vFormat, "MM", "%m")
    vFormat = sString_Replace(vFormat, "DDDD", "%A")
    vFormat = sString_Replace(vFormat, "DDD", "%a")
    vFormat = sString_Replace(vFormat, "DD", "%d")
    vFormat = sString_Replace(vFormat, "HH", "%H")
    vFormat = sString_Replace(vFormat, "mm", "%M")
    vFormat = sString_Replace(vFormat, "ss", "%S")
    vFormat = sString_Replace(vFormat, "EEE", "%f")
    vFormat = sString_Replace(vFormat, "EE", "%f")
    vFormat = sString_Replace(vFormat, "E", "%f")
    vReturn = oDate.strftime(vFormat)
    return vReturn

def sDate_Now():
    from datetime import date
    return date.today()

def sDateTime_Now():
    from datetime import datetime
    return datetime.now()

def sDate_Add(oDate, iAdd, vType):
    """vType DD, HH, mm, ss
    ini belom bisa = MM, YYYY
    """
    from _datetime import timedelta
    import calendar
    oDelta = timedelta(days=0)
    if(vType == "ss") : oDelta = timedelta(seconds=iAdd) 
    if(vType == "mm") : oDelta = timedelta(minutes=iAdd)
    if(vType == "HH") : oDelta = timedelta(hours=iAdd)
    if(vType == "DD") : oDelta = timedelta(days=iAdd)
    oReturn = oDate + oDelta
    
    #kalo year dan bulan belum bisa, karena misal skrg tgl 29 feb, belom tentu taon depan ada tgl 29, ato bulan depan ada tgl 31
    if(vType == "YYYY") : oDelta = timedelta(years=iAdd)
    if(vType == "MM") : 
        iAdd_Abs = abs(iAdd)
        for i in range(0, iAdd_Abs):
            iDays_inMonth = calendar.monthrange(oDate.year, oDate.month)[1]
            oDate += timedelta(days=iDays_inMonth)
            print(iDays_inMonth)
#         oDelta = timedelta
    return oReturn

def sDateTime_Difference_in_Seconds(oDateTime2, oDateTime1):
    return (oDateTime2 - oDateTime1).total_seconds()

def sDateTime_Difference_in_Minutes(oDateTime2, oDateTime1):
    oDelta = sDateTime_Difference_in_Seconds(oDateTime2, oDateTime1)
    return (oDelta / 60)

def sDateTime_Difference_in_Hours(oDateTime2, oDateTime1):
    oDelta = sDateTime_Difference_in_Seconds(oDateTime2, oDateTime1)
    return (oDelta / 60 / 60)

def sDateTime_Difference_in_Days(oDateTime2, oDateTime1):
    oDelta = sDateTime_Difference_in_Seconds(oDateTime2, oDateTime1)
    return (oDelta / 60 / 60 / 24)

def sExecute_Shell(vCMD, vArgument = "", vTitle = "Command", isWait = True, iLimit_Error = 250):
    """return result
    result.returncode (0=ok,1=error)
    result.stderr (error messagenya)
    limit error textnya kalo terlalu panjang juga gak kebaca
    """
    class cReturn():
        returncode = 0
        
        stderr = ""
    import os
    if(isWait == True):
        "ini nunggu, tapi buat exe kayaknya"
        import subprocess
        result = subprocess.run([vCMD, vArgument], stderr=subprocess.PIPE)
        if(result.returncode > 0):
            result.stderr = sString_Replace(str(result.stderr), r"\r\n", vNew_Line)
            result.stderr = sString_Replace(str(result.stderr), r"\\\\", "\\")
            result.stderr = sString_Replace(str(result.stderr), "b\\", "")
            result.stderr = sString_Replace(str(result.stderr), r"\x1b", "")
            result.stderr = sString_Right(result.stderr, iLimit_Error)
        return result
    else :
        "ini bisa buat command"
        vFull_Command = sString_Create("start \"{0}\" \"{1}\" {2}", vTitle, vCMD, vArgument)
        os.system(vFull_Command)
        oResult = cReturn()
        return oResult
    return

def sExecute_Shell2(vCMD):
    "ini execute bat file bisa dan nungguin"
    import os
    os.system(vCMD)

def sExcel_Read(vExcel_Path, vSheet_Name):
    """read excel and return pandas
    untuk iterate for index, row in df.iterrows():
    print(row['TGL'])
    """
    import pandas
    df = pandas.read_excel(vExcel_Path, sheet_name=vSheet_Name)
    return df

def sExcel_Write_Panda(vPath, df, vSheet_Name, vStart_Col):
    """startcol = E
    """
    import pandas as pd
    from openpyxl import load_workbook
    book = load_workbook(vPath)
    writer = pd.ExcelWriter(vPath, engine="openpyxl")
    writer.book = book

    vCol_Num = sExcel_Get_Column_Number(vStart_Col)
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, vSheet_Name, startcol=vCol_Num, index=False)
    writer.save()

def sExcel_Get_Column_Number(vCol):
    """get column number a = 1, b=2
    """
    vCol_Start = vCol
    vNumber = sString_2_CharNumber(vCol_Start)
    if(vNumber > 96) : vNumber -= 97
    else : vNumber -= 65
    return vNumber

def sFile_Delete(vPath):
    try:
        import os
        os.remove(vSelenium_Link_Path)
    except:
        qwe = 123

def sFile_Directory_Create(vPath):
    import os
    import errno
    vPath = vPath + "/"
    if not os.path.exists(os.path.dirname(vPath)):
        try:
            os.makedirs(os.path.dirname(vPath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return

def sFile_Get_Directory(vPath = ""):
    import os
    if(vPath == "") : vPath = __file__
    vDir = os.path.dirname(os.path.abspath(vPath))
    return vDir

def sFile_isExist(vPath):
    import os.path
    isExist = False
    if os.path.isfile(vPath):
        isExist = True
    return isExist

def sFile_Read(vPath):
    """Read file
    """
    try:
        f = open(vPath, "r")
        vText = f.read()
        f.close()
    except: 
        vText = ""
    return(vText)

def sFile_Write(vPath, vText, isAppend = False, isAppend_AddLine = True):
    """write file
    """
    import os
    import errno
    isExist_File = True
    if not os.path.exists(os.path.dirname(vPath)):
        try:
            os.makedirs(os.path.dirname(vPath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if(sFile_isExist(vPath)==False): isExist_File = False
    vAttr = "w+"
    if(isAppend) :
        vAttr = "a"
        if(isAppend_AddLine and isExist_File) : 
            vText = vNew_Line + vText
        
    f = open(vPath, vAttr, encoding='utf8')
    f.write(vText)
    f.close()
    return()

def sFunction_Execute(oFunc, args=()):
    """execute function, lebih rapi dari kasih string doang
    ex= sFunction_Execute(print_time, (1, 3))
    """
    oReturn = None
    if(sString_Find(str(type(args)), "'tuple")):
        oReturn = oFunc(*args)
    else:
        oReturn = oFunc(args)
    return oReturn

def sGUI_Enter_Input(vQuestion):
    import tkinter.font as tkFont
    from tkinter.constants import RIGHT
    top = Tk()
    root = top
    windowWidth = top.winfo_reqwidth()
    windowHeight = top.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    
    fontStyle = tkFont.Font(family="Lucida Grande", size=20)
    L1 = Label(top, text = vQuestion, font=fontStyle)
    L1.pack()
    E1 = Entry(top, bd = 5, font=fontStyle)
    E1.pack()
    E1.focus()
    class cInput():
        vEntry = ""
    def stExit_App(vType):
        vEntry = str(E1.get())
        if(vType == "s") : cInput.vEntry = vEntry
        root.destroy()
    top.bind_all("<Alt-x>", lambda a=1: stExit_App("x"))
    top.bind_all("<Alt-s>", lambda a=1: stExit_App("s"))
    Button (root, text='e = Exit',command=lambda: stExit_App('e'),bg='white').pack(side = RIGHT)
    Button (root, text='s = Submit',command=lambda: stExit_App('s'), bg='white').pack(side = RIGHT)    
    top.mainloop()
    return cInput.vEntry

def sHTML_Get_NoScript(url):
    """Read html tapi gak jalanin javascript
    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return(text)

def sHTML_Get_WithScript(url, vPath_Driver = ""):
    if(vPath_Driver == ""): vPath_Driver = sConfig_Read("vChromeDriver")
    chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True
    
    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities, executable_path=vPath_Driver)
    driver.get(url)
    
    html = 'kosong'
    isFinish = 0
    while isFinish == 0 :
        status = driver.execute_script("return document.readyState")
        if status == 'complete' :
            isFinish = 1
        else :
            time.sleep(1)
    
    html = driver.find_element_by_tag_name("body").text
    driver.close()
    driver.quit()
    return html

def sHTML_Get_WithPyCurl(url):
    import pycurl
    from io import BytesIO
    c = pycurl.Curl()
    e = BytesIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, e.write)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.HTTPHEADER, ["Connection: keep-alive",
                                "Upgrade-Insecure-Requests: 1",
                                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
                                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                                "Sec-Fetch-Site: none",
                                "Sec-Fetch-Mode: navigate",
                                "Accept-Language: en-US,en;q=0.9,id;q=0.8"])
    c.perform()
    c.close()
    content = e.getvalue().decode('UTF-8')
        
    text = content
    text = text.replace(">", ">\n")
    text = sHTML_Extract_Text(text)
    return text

def sHTML_Extract_Text(vHTML, vDelimiter = vNew_Line):
    soup = BeautifulSoup(vHTML, features="lxml")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text(separator=vDelimiter)
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return(text)

def sInteger_Random_Generator(iStart, iStop):
    from random import randint
    iNum = randint(iStart, iStop)
    return iNum

def sJDBC_Load_Connection(vList_JDBC, vDriver, vURL):
    "load jdbc connection"
    import jaydebeapi as jdbc
    arrJDBC = sSplit(vList_JDBC, ",")
    oConn = jdbc.connect(jclassname=vDriver, url=vURL, jars=arrJDBC)
    return oConn

def sLabel_2_Int(vList_Label, arrLabel, vDelimiter = ",", isLabel = True):
    """return 2 variable array, label dan integernya
    arrLabel, arrInt = sLabel_2_Int(vList_Label, ",")
    """
    arrHash = {}
    iTemp = 0
    arrData = sSplit(vList_Label, vDelimiter)
    for vLabel in arrData:
        if(isLabel) : arrHash[vLabel] = iTemp
        else : arrHash[iTemp] = arrData[iTemp]
        iTemp+=1
        
    oReturn = None
    oReturn = [ arrHash[vName] for vName in arrLabel ]
    return oReturn

def sML_Model_Save(oModel, vPath):
    """func to save model of machine learning ex:LinearRegression
    """
    import pickle
    vPath_Model = vPath  
    with open(vPath_Model, 'wb') as file:  
        pickle.dump(oModel, file)

def sML_Model_Load(vPath):
    """func to model of machine learning ex:LinearRegression
    """
    import pickle
    oModel = None
    with open(vPath, 'rb') as file:  
        oModel = pickle.load(file)
    return oModel

def sML_Model_Train(oX, oY, vList_Model, vPath_Save):
    """func to check many model score, using default settings
    vList_Model_Regression = "skr.ARDRegression,skr.BayesianRidge,skr.ElasticNet,skr.ElasticNetCV,skr.Hinge,skr.Huber,skr.HuberRegressor,skr.Lars,skr.LarsCV,skr.Lasso,skr.LassoCV,skr.LassoLars,skr.LassoLarsCV,skr.LassoLarsIC,skr.LinearRegression,skr.Log,skr.LogisticRegression,skr.LogisticRegressionCV,skr.ModifiedHuber,skr.MultiTaskElasticNet,skr.MultiTaskElasticNetCV,skr.MultiTaskLasso,skr.MultiTaskLassoCV,skr.OrthogonalMatchingPursuit,skr.OrthogonalMatchingPursuitCV,skr.PassiveAggressiveClassifier,skr.PassiveAggressiveRegressor,skr.Perceptron,skr.RANSACRegressor,skr.Ridge,skr.RidgeCV,skr.RidgeClassifier,skr.RidgeClassifierCV,skr.SGDClassifier,skr.SGDRegressor,skr.SquaredLoss,skr.TheilSenRegressor,skr.__all__,skr.__builtins__,skr.__cached__,skr.__doc__,skr.__file__,skr.__loader__,skr.__name__,skr.__package__,skr.__path__,skr.__spec__,skr.base,skr.bayes,skr.cd_fast,skr.coordinate_descent,skr.enet_path,skr.huber,skr.lars_path,skr.lars_path_gram,skr.lasso_path,skr.least_angle,skr.logistic,skr.logistic_regression_path,skr.omp,skr.orthogonal_mp,skr.orthogonal_mp_gram,skr.passive_aggressive,skr.perceptron,skr.ransac,skr.ridge,skr.ridge_regression,skr.sag,skr.sag_fast,skr.sgd_fast,skr.stochastic_gradient,skr.theil_sen"
    vList_Model_Classification = "GradientBoostingClassifier,DecisionTreeClassifier,RandomForestClassifier,LinearDiscriminantAnalysis,LogisticRegression,KNeighborsClassifier,GaussianNB,ExtraTreesClassifier,BaggingClassifier"
    vPath_Save (kalau list model lebih dari satu, tidak disave, karena untuk percobaan biasanya)
    """
#     import sklearn.linear_model
    import sklearn.linear_model as skr 
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
    arrModel = sSplit(vList_Model, ",")
    for vModel in arrModel :
        try:
            _locals = locals()
            exec("oModel = " + vModel + "()", globals(), _locals)
            oModel = _locals['oModel']
    
            oXTrain, oXTest, oYTrain, oYTest = train_test_split(oX, oY, test_size=0.2, random_state=123)
            oModel.fit(X=oXTrain, y=oYTrain)
            oPred = oModel.predict(X=oXTest)
            oScores = r2_score(oYTest, oPred) * 100
            print(sString_Create("{0} Train Score = ", vModel) + str(oScores) + " %")
            if(len(arrModel) == 1) :
                vList_Col_Model = sDataframe_Get_Columns(oX)
                oPickle = oModel, vList_Col_Model
                sML_Model_Save(oPickle, vPath_Save)
                print("Model saved at " + vPath_Save)
        except Exception as e:
            print(sString_Create("{0} Train Failed : {1}", vModel, str(e)))

def sString_2_CharNumber(vChar):
    return ord(vChar)

def sString_2_Date(vText, vFormat):
    """return date with requested format as string
    ex: vFormat YYYY/MM/DD HH:mm:ss EEE EE E
    """
    from _datetime import datetime
    vFormat = sString_Replace(vFormat, "YYYY", "%Y")
    vFormat = sString_Replace(vFormat, "MMMM", "%B")
    vFormat = sString_Replace(vFormat, "MMM", "%h")
    vFormat = sString_Replace(vFormat, "MM", "%m")
    vFormat = sString_Replace(vFormat, "DD", "%d")
    vFormat = sString_Replace(vFormat, "HH", "%H")
    vFormat = sString_Replace(vFormat, "mm", "%M")
    vFormat = sString_Replace(vFormat, "ss", "%S")
    vFormat = sString_Replace(vFormat, "EEE", "%f")
    vFormat = sString_Replace(vFormat, "EE", "%f")
    vFormat = sString_Replace(vFormat, "E", "%f")
    vTanggal = datetime.strptime(vText, vFormat).date() 
    return vTanggal

def sString_2_Int(vText):
    iReturn = 0
    try:
        iReturn = int(vText)
    except: ""
    return iReturn

def sString_2_Float_IfCan(vVal):
    "will return float if can, else string"
    if(vVal.isnumeric()) : return float(vVal)
    else: return vVal

def sString_is_Number(vText):
    return vText.isnumeric()
    
def sString_Get_Last_Rows(vText, iNum_Rows):
    """Get last lines / rows from text
    """
    arrRows = sSplit(vText, vNew_Line)
    iAdder = 0
#     if(arrRows[len(arrRows)-1] == '') : iAdder = 1
    iStart = (iNum_Rows + iAdder) * -1
    
    arrNew = arrRows[iStart:]
    if(iAdder > 0) : arrNew = arrRows[iStart:(iAdder * -1)]
    vNew_Text = vNew_Line.join(arrNew)
    return vNew_Text

def sString_Get_Parameter_Content(vText, vParameter, vDelimiter_Equal = "=", vDelimiter_Line = vNew_Line, isRemove_Comment=False):
    """get content of parameter ex DB=SQL, User=SA (it will trim it's value)
    """
    vContent = ""
    vText += vDelimiter_Line
    try:
        iLoc1 = vText.find(vParameter + vDelimiter_Equal)
        iLoc2 = iLoc1 + vText[iLoc1:].find(vDelimiter_Line)
        if(iLoc1 >= 0) : vContent = vText[iLoc1 + len(vParameter) + len(vDelimiter_Equal) :iLoc2]     
    except:
        vContent = ""
    
    if(isRemove_Comment):
        iLoc1 = vContent.find("#")
        if(iLoc1 >= 0) : 
            vContent = vContent[:iLoc1]
            vContent = sString_Trim(vContent)
    return vContent

def sString_Get_Inside_Tag(vText, vTag_Open, vTag_Close, isWith_Tag = False):
    """this will get inside tag
    """
    vContent = ""
    iLoc1 = vText.find(vTag_Open)
    iLoc2 = iLoc1 + vText[iLoc1 + len(vTag_Open):].find(vTag_Close)
    if(iLoc1 > -1) : 
        vContent = vText[iLoc1 + len(vTag_Open) : iLoc2 + len(vTag_Open)]
        
    if(vContent != "" and isWith_Tag):
        vContent = sString_Create("{0}{1}{2}", vTag_Open, vContent, vTag_Close)     
    return vContent

def sString_Get_Inside_Tag_Arr(vText, vTag_Open, vTag_Close):
    isFinish = False
    vList = ""
    arrReturn = []
    while isFinish == False :
        vFound = sString_Get_Inside_Tag(vText, vTag_Open, vTag_Close, True)
        vClean = vFound.replace(vTag_Open, "").replace(vTag_Close, "")
        vText = sString_Replace(vText, vFound, "")
        if(vFound == "") : isFinish = True
        else :
            vList = sVBCLRF_Max_Line(vList, vClean, vNew_Line)
    if(vList != "") : arrReturn = sSplit(vList, vNew_Line)
    return arrReturn

def sString_Get_Inside_HTML_Tag(vText, vTag):
    """misal html content gitu isinya
    """
    vTag = str(vTag)
    return sString_Get_Inside_Tag(vText, sString_Create("<{0}>", vTag), sString_Create("</{0}>", vTag), False)

def sString_Encode_UTF8(vText):
    """encode ke string biasa (ini kalo html biasanya error karena ada huruf chinese misalnya)
    """
    vText = str(vText.encode("utf-8"))
    vText = sString_Replace(vText, r"\n", vNew_Line)
    return vText

def sString_Left(vText, iLeft):
    return(vText[0:iLeft])

def sString_Right(s, amount):
    return s[-amount:]

def sString_Replace(vText, vFind, vReplace):
    return vText.replace(vFind, vReplace)

def sString_Trim(vText):
    return vText.lstrip().rstrip()

def sUsername_Password_Get(vName, vPath = ""):
    if(vPath == "") : vPath = sConfig_Read("vEmail")
    vText = sFile_Read(vPath)
    vUserName_Password = sString_Get_Parameter_Content(vText, vName)
    class cUsernamePassword:
        UserName = ""
        Password = ""
    oUser = cUsernamePassword()
    oUser.UserName = sSplit_Get(vUserName_Password, ":", 0)
    oUser.Password = sSplit_Get(vUserName_Password, ":", 1)
    return oUser

def sString_Create(vText, *arrInput):
    """create string args (ex= {0} {0} {1})
    """
    i = 0
    for vValue_Temp in arrInput:
        vValue = str(vValue_Temp)
        vText = vText.replace("{" + str(i) + "}" , vValue)
        i = i + 1
    return vText

def sString_Create_HTML_Tag(vText, vTag):
    vTag = sString_Create("<{0}>{1}</{0}>", str(vTag), vText)
    return vTag

def sSplit(vText, vDelimiter):
    return vText.split(vDelimiter)

def sSplit_2_Integer(vText, vDelimiter):
    return list(map(int, vText.split(vDelimiter)))

def sSplit_2_2Dimension_forML(vList, vDelimiter_Col = ",", vDelimiter_Row = ";"):
    """ini musti angka yah, karena buat machine learning harus angka
    """
#     a = np.array([[float(j) for j in i.split(vDelimiter_Col)] for i in vList.split(vDelimiter_Row)])
    a = [[sString_2_Float_IfCan(j) for j in i.split(vDelimiter_Col)] for i in vList.split(vDelimiter_Row)]
    return a

def sSplit_Get(vText, vDelimiter, iGet, vDefault = ""):
    vReturn = vDefault
    try:
        vReturn = vText.split(vDelimiter)[iGet]
    except:
        qwe = 123
    return vReturn

def sSelenium_Attach_Session(iID = 1):
    """sample vlink = http://127.0.0.1:31245 = c80967b2441b3f5a3cd85e5ec1d900df
    """
    vTemp_Content = sFile_Read(vSelenium_Link_Path)
    vLink = sString_Get_Inside_HTML_Tag(vTemp_Content, iID)
    executor_url = sSplit_Get(vLink, " = ", 0)
    session_id = sSplit_Get(vLink, " = ", 1)
    iPort = sSplit_Get(executor_url, ":", 2)
    isPort_Open = sTelnet_Check_Open("localhost", iPort, 0.5)
    driver = None

    if(isPort_Open) :
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        original_execute = WebDriver.execute
        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return original_execute(self, command, params)
        # Patch the function before creating the driver object
        WebDriver.execute = new_command_execute
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.session_id = session_id

        # Replace the patched function with original function
        WebDriver.execute = original_execute
    else :
        vFind = sString_Get_Inside_Tag(vTemp_Content, sString_Create("<{0}>", str(iID)), sString_Create("</{0}>", str(iID)), True)
        if(vFind != ""):
            vTemp_Content = sString_Replace(vTemp_Content, vFind, "")
            sFile_Write(vSelenium_Link_Path, vTemp_Content)
    return driver

def sSelenium_Get_Driver(vBrowser = "chrome", iID = "1", vData_Dir = ""):
    b"""datadir = "NONE" (artinya gak pake), kosong ikut default
    """
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    if(str(iID) == "") : iID = "1"

    driver = None    
    if(vBrowser == "chrome"):
        driver = sSelenium_Attach_Session(iID)
        if(driver == None):
            vPath_Driver = sConfig_Read("vChromeDriver")
            chrome_options = webdriver.ChromeOptions()
            vHostname = sApplication_Get_Machine_Name()
            
            vData_Dir_Default = sConfig_Read("vChromeTempPathDefault")
            if(vHostname == "simon10home"):
                vData_Dir_Default = sConfig_Read("vChromeTempPath")
                vPath_DataDir_Default_Source = sConfig_Read("vChromePathDataDefault")
                vPath_DataDir_Default_Target = vData_Dir + "/Default"
                if(1==1):
                    'copy bookmark'
                    vPath_Bookmark_Source = vPath_DataDir_Default_Source + "/Bookmarks"
                    vPath_Bookmark_Target = vPath_DataDir_Default_Target + "/Bookmarks"
                    vBookmark_Source = sFile_Read(vPath_Bookmark_Source)
                    vBookmark_Target = sFile_Read(vPath_Bookmark_Target)
                    if(vBookmark_Source != vBookmark_Target):
                        sFile_Write(vPath_Bookmark_Target, vBookmark_Source)
                            
            if(vData_Dir == "") : vData_Dir = vData_Dir_Default
            chrome_options.add_argument("user-data-dir=" + vData_Dir)
            
            chrome_options.add_argument("disable-extensions");
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities['acceptSslCerts'] = True
            capabilities['acceptInsecureCerts'] = True

            driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities, executable_path=vPath_Driver)
            vLink = sString_Create_HTML_Tag(driver.command_executor._url + " = " + driver.session_id, iID)
            sFile_Write(vSelenium_Link_Path, vLink, True)
    elif(vBrowser == "firefox"):
        from selenium.webdriver.firefox import firefox_profile
        vPath_Driver = sConfig_Read("vFirefoxPathDriver")
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        oOptions = webdriver.FirefoxOptions()
        profile = FirefoxProfile(sConfig_Read("vFirefoxTempPath"))
        driver = webdriver.Firefox(firefox_profile=profile, options=oOptions, executable_path=vPath_Driver)
    return driver

def sSelenium_Check_Still_Open(driver):
    """check if web closed or not
    """
    isOpen = True
    try:
        driver.execute_script("console.clear()")
    except:
        isOpen = False
        from selenium.webdriver.remote.webdriver import WebDriver
        WebDriver.__exit__(driver)
    return isOpen

def sSelenium_Check_Closed_Exit(driver):
    """Check if browser is closed, it will quit program
    """
    iInterval = 1
    iInterval_Add_Wait = 2 #buat cek diff second
    oTemp_Selenium_Last_Check_Time = sDateTime_Now()
    iCounter = 0
    from selenium.webdriver.remote.webdriver import WebDriver
    while True:
        sWait(iInterval)
        try:
            "skip add function"
            oClass = driver.execute_script(sString_Create("return document.getElementsByClassName('{0}')", "ytp-ad-skip-button-container"))
            if(len(oClass) > 0) :
                driver.execute_script(sString_Create("document.getElementsByClassName('{0}')[0].click()", "ytp-ad-skip-button ytp-button"))
        except: qwe = 123
        
        if(sString_Find(str(driver.get_log('driver')), "disconnected")) : 
            oDiff_Seconds = sDateTime_Difference_in_Seconds(sDateTime_Now(), oTemp_Selenium_Last_Check_Time)
            if(oDiff_Seconds > (iInterval + iInterval_Add_Wait)) :
                #kalo beda time lebih dari x, mungkin abis restart, clear log
                try:
                    driver.execute_script("console.clear()")
                except:
                    print("Exiting karena browser closed")
                    WebDriver.__exit__(driver)
                    exit()
                iCounter = 0
            else:
                iCounter +=1
                if(iCounter > 2) :
                    print("Exiting karena log ada disconnected, tapi durationnya gak masuk") 
                    try: WebDriver.__exit__(driver)
                    except:""
                    exit()

        oTemp_Selenium_Last_Check_Time = sDateTime_Now()
    return


def sSelenium_Close_PopUp_Browser(driver):
    try:
        for i in range(1, len(driver.window_handles)):
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
    except:
        tmp = 123;
    driver.switch_to.window(driver.window_handles[0])
    return

def sSelenium_Execute_Script(driver, vScript, *args):
    vScript = sString_Create(vScript, *args)
    return driver.execute_script(vScript)

def sSelenium_Execute_Script_Print(driver, vScript, *args):
    vScript = "return " + sString_Create(vScript, *args)
    print(driver.execute_script(vScript))

def sSelenium_Execute_Until_No_Error(driver, vElement, iTimeout_Seconds):
    for i in range(iTimeout_Seconds):
        try:
            driver.execute_script(vElement)
            break    
        except: 
            sWait(1)
    return

def sSelenium_Hit_Enter(driver, vID):
    from selenium.webdriver.common.keys import Keys
    driver.find_element_by_id(vID).send_keys(Keys.ENTER)

def sSelenium_Open_Chrome(iID = 1, vTitle = "CMD_Chrome", vData_Dir = ""):
    """open browser chrome if not exist, or reuse if exist
    """
    driver = None
    if(sWindow_Find_By_Title(vTitle) == None) :
        vCMD = sApplication_Get_Directory_Python_Main() + r"\zConsole_Command\browser_open.bat"
        sExecute_Shell(vCMD
                       , sString_Create(r"{0} {1}", iID, vData_Dir)
                       , vTitle, isWait = False)
        b"karena buka new window, dia musti looping buat ngecek udah keload belom"
        while True:
            sWait(1)
            driver = sSelenium_Attach_Session(iID)
            if(driver != None) :
                break
    else :
        driver = sSelenium_Attach_Session(iID)
    return driver

def sSelenium_Print(driver, vElement, *arrInput):
    ""
    vScript = sString_Create("return " + vElement, *arrInput)
    vText = sString_Encode_UTF8(sSelenium_Execute_Script(driver, vScript))
    print(vText)
    
def sSelenium_Set_By_ID(driver, vID, vValue):
    """set value by id
    """
#     print(driver.execute_script(q.sString_Create("return {0}.document.getElementsByName('{1}')[0].value", vFrame_Right, "value(submit)")))
    driver.execute_script(sString_Create("document.getElementById('{0}').value='{1}'", vID, vValue))
    return

def sSelenium_Stop_Close(driver):
    try:
        driver.close()
    except: 
        print("Quitting")
    driver.quit()
    exit()

def sString_Find(vText, *arrFind):
    vReturn = False
    vText = str(vText)
    if(str(type(arrFind[0])).find("'list'") > -1):
        arrFind = arrFind[0]
    for vFind in arrFind:
        if(vFind == "") : break
        if(vText.lower().find(vFind.lower()) > -1):
            vReturn = True
            break    
    return vReturn

def sPort_Open(iPort_Num, vHostName = "localhost"):
    host = socket.gethostname() # Get local machine name
    socekt_Global1.bind((vHostName, iPort_Num))
    socekt_Global1.listen()

def sPort_Close():
    socekt_Global1.close()

def sTelnet_Check_Open(vHost, iPort, iTimeout = 1):
    """check if port is open
    """
    isOpen = False
    import telnetlib
    try:
        tn = telnetlib.Telnet(vHost, iPort, iTimeout)
        isOpen = True
    except:
        isOpen = False
    return isOpen

arrThread_Func_Temp = []
def sThread_Run(oFunc, args=()):
    """sThread_Run(print_time, (1, 3))
    !!!inget pake kurung (cuma bisa 1 argumen, tapi dalemnya banyak
    """
    import threading
    class cThread (threading.Thread):
        def __init__(self, oFunc, args=()):
            threading.Thread.__init__(self)
            self.threadID = sInteger_Random_Generator(1, 1000000)
            self.oFunc = oFunc
            self.oArgs = args
        def run(self):
            ""
            sFunction_Execute(self.oFunc, self.oArgs)
    oT = cThread(oFunc, args)
    oT.daemon = True # kalo pake ini, kalo main thread selesai, dia akan kill semua anaknya
    oT.start()
    arrThread_Func_Temp.append(oT)

_vThread_Wait_Continue_Wait = True #kalo true dia akan nunggu sampe semua job selesai
def sThread_Wait():
    """wait for all global thread to finish
    """
    import threading
    while True:
        sWait(1)
        isAll_Close = True
        for oT in arrThread_Func_Temp:
            ""
            isAlive = threading.Thread.is_alive(oT)
            if(isAlive) : 
                isAll_Close = False
                break
        if(isAll_Close or _vThread_Wait_Continue_Wait == False) : break
            

def sThread_Kill():
    """set global var yg wait, kalo mau exit
    """
    global _vThread_Wait_Continue_Wait
    _vThread_Wait_Continue_Wait = False

_oList_Box_Tkinter = None
def _sTkinter_Loop(vList):
    global _oList_Box_Tkinter
    from tkinter import Tk
    from tkinter import Listbox
    from tkinter import font
    oTop = Tk()
    iSize_Font = 25
    appHighlightFont = font.Font(family='Helvetica', size=iSize_Font, weight='bold')
    oList = Listbox(oTop, font=appHighlightFont)
    
    arrVal = sSplit(vList, ",")
    for vVal in arrVal :
        oList.insert(1, vVal)
    oList.pack()
    _oList_Box_Tkinter = oList
    oList.select_set(0)
    oTop.mainloop()
        
def sTkinter_Listbox(vList, iSize_Font = 25):
    """ oListBox = q.sTkinter_Listbox("WatchLater,JustWatch")
    supaya gak exit, ex = oTop.mainloop()
    get value = value = str((Lb1.get(ACTIVE)))
    showing select box for option
    """
    oList = None
    sThread_Run(_sTkinter_Loop, vList)
    sWait(1)
    return _oList_Box_Tkinter

def sTkinter_Listbox_get_Value(oListBox):
    from tkinter.constants import ACTIVE
    value = str((oListBox.get(ACTIVE)))
    return value

def sTkinter_Listbox_Get_Index(oListBox):
    """get index
    """
    iIndex = 0
    try:
        iIndex = oListBox.curselection()[0]
    except: ""
    return  iIndex

def sTkinter_Listbox_Set_Value(oListBox, vValue):
    """set listbox by value
    """
    for i in range(oListBox.size()):
        if(str(oListBox.get(i)) == vValue):
            oListBox.select_set(i)
            break

def sTokenizer_Words(vText, iWords = 2, vList_Stopwords=""):
    b"""akan return oC, df (hashtable dan dataframe)
    dia akan menghitung occurance multi words, misal new york
    iWords = jumlah words (makin banyak makin berat, dia musti cek stiap word)
    """
    import collections
    import pandas as pd
    vText = vText.lower()
    arrText = sSplit(vText, vNew_Line)

    c=collections.Counter()
    def sLoop_On_IWords(iWords_Temp, c):
        ""
        for i in arrText:
            i = i.lstrip().rstrip()
            arrWord = i.split(" ")
            
            for iWord in range(len(arrWord)) :
                vWord = ""
                for iTemp1 in range(iWords_Temp):
                    try:
                        vWord = sVBCLRF_Max_Line(vWord, arrWord[iTemp1 + iWord], " ")
                    except: break
                
                if vWord == "new york" :
                        qwe = 123
                
                if(vWord != ""):
                    iLen_Words = len(sSplit(vWord, " "))
                    if(iLen_Words != iWords_Temp) : break
                    "ini kalo 1 words mengganggu, masukin stop word aja"
                    c.update( zip([vWord]) )
        if(iWords_Temp > 1):
            sLoop_On_IWords(iWords_Temp - 1, c)
        return c

    c = sLoop_On_IWords(iWords, c)

    stopwords = sSplit(vList_Stopwords, ",")
    cols = ['words', 'numwords', 'counter']
    rows = []
    for idx,i in enumerate(c): 
        vWord = ' '.join(i)
        iNumWords = len(sSplit(vWord, " "))
        row = [vWord, iNumWords, c[i]]
        if vWord not in stopwords:
            rows.append(row)
    
    df = pd.DataFrame(rows, columns = cols)

    def sLocal_Remove_Children_Same_Occurance(df):
        "remove kalo anaknya jumlah occurancenya sama, artinya udah dicover ama parentnya"
        c2=collections.Counter()
        df = df.sort_values(by=['numwords'], ascending=False)
        iMax = 0
        for index, oRow in df.iterrows():
            if (iMax == 0) : iMax = oRow['numwords']
            iNumWords = oRow['numwords']
            iCounter = int(oRow['counter'])
            if(iMax != iNumWords):
                vWords = str(oRow['words'])
                iNumwords = oRow['numwords']
                dfParent = df[df['words'].str.contains(vWords)]
                dfParent = dfParent[dfParent['numwords'] > iNumWords]
                dfParent = dfParent.sort_values(by=['counter'], ascending=False)
                iLen_Parent = len(dfParent)
                if(vWords == "rawa belong"):
                    qwe = 123 
                if(iLen_Parent > 0):
                    iParent_Counter = int(dfParent['counter'].iloc[0])
                    if(iParent_Counter >= iCounter) :
                        "delete"
                        df = df.drop(index)
        return df
    df = sLocal_Remove_Children_Same_Occurance(df)
    c = sDataframe_2_Collection_Counter(df)
    return c, df

def sVBCLRF_Max_Line(vText_VBCRLF, vValue, vDelimiter_Row = vNew_Line):
    if (vText_VBCRLF == None) : vText_VBCRLF = "";
    if (vDelimiter_Row == None) : vDelimiter_Row = vNew_Line;
    if (vText_VBCRLF != "") : vValue = vDelimiter_Row + vValue;

    vText_VBCRLF = vText_VBCRLF + vValue;
    return vText_VBCRLF

def sWait(iSeconds):
    time.sleep(iSeconds)
    return

def sWindow_Find_By_Title(vTitle, isDisplay = False):
    """list handle by title (like), use display true to debug
    """
    import win32gui
    import win32con
    vList_Handle = ""    
    def winEnumHandler( hwnd, hwnds ):
        if (win32gui.IsWindowVisible(hwnd)):
            vHandle = int(hwnd)
            vTitle_Source = win32gui.GetWindowText(hwnd)
            vTemp = str(vHandle) + ":" + vTitle
            if(sString_Find(vTitle_Source, vTitle)) :
                if(isDisplay) : print(vTemp)
                hwnds.append(vHandle)
    hwnds = []
    win32gui.EnumWindows( winEnumHandler, hwnds)
    oReturn = None
    if(len(hwnds) > 0) : oReturn = hwnds[0]
    return oReturn


def sWindow_Focus(oHandle, isMaximized = True):
    import win32gui
    import win32con
    try:
        if(isMaximized) : win32gui.ShowWindow(oHandle, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(oHandle)
    except:qwe=123

def sWindow_Kill(vTitle):
    import win32gui
    import win32con
    vTitle = str(vTitle)
    oHandle = None
    if(sString_is_Number(vTitle)):
        oHandle = sString_2_Int(vTitle)
    else:
        oHandle = sWindow_Find_By_Title(vTitle, True)
    win32gui.PostMessage(oHandle ,win32con.WM_CLOSE,0,0)
    return

def write2(vText):
    print(vText)
    return

def write(*arrText):
    print(arrText)
    return



def sReload(q):
    """to reload q module, jika jalanin dari command prompt, dan ada perubahan coding, dan ingin refresh tanpa quit
    sReload(q)
    """
    from importlib import reload
    q = reload(q)
    
    
    
vSelenium_Link_Path = sConfig_Read("vSelenium_Link_Path") #temp browser port
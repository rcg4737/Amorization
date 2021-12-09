import tkinter
from tkinter import messagebox, ttk  
from ttkthemes import ThemedTk
import pandas as pd
import numpy as np
import os
import fnmatch

def find(pattern, path):
        result = ''
        for root, dirs, files in os.walk(path):
                for name in files:
                        if fnmatch.fnmatch(name, pattern):
                                result = os.path.join(root, name)
        return str(result) if result!='' else None


def disc_process(dataFilePath):
    

    try:
        df1 = pd.read_csv('df1.txt', sep='|', dtype={'Loan Number': str})
        df2 = pd.read_csv('df1_2.txt', sep='|')
    except:
        tkinter.messagebox.showerror('File Reading Error','Please make sure the df1 data file are closed and not in use.')
        

    #   Principal/Interest Payment CHECK
    PI_Dict = {'Loan Number':[], 'P&I Payment':[], 'Calculated P&I':[]}
    for i, payment in enumerate(df1['Principal/Interest Payment']):
        PI_Payment = abs(round(np.pmt((df1['Annual Interest Rate'][i]/100)/(df1['Payment Period'][i]), (df1['Payment Period'][i])*(df1['Loan Term'][i]//12), df1['Current Principal Balance'][i]),2))
        if payment != PI_Payment:
            PI_Dict['Loan Number'].append(df1['Loan Number'][i])
            PI_Dict['P&I Payment'].append(payment)
            PI_Dict['Calculated P&I'].append(PI_Payment)
    PI_Discrepancies = pd.DataFrame.from_dict(PI_Dict)

    #   Due Date Check
    date_Dict = {'Loan Number':[], 'Current Due Date':[], 'First Due Date': []}
    for i, (currentDueDate, firstDueDate) in enumerate(zip(df1['Current Due Date'], df1['First Due Date'])):
        if currentDueDate != firstDueDate:
            date_Dict['Loan Number'].append(df1['Loan Number'][i])
            date_Dict['Current Due Date'].append(currentDueDate)
            date_Dict['First Due Date'].append(firstDueDate)
    date_Discrepancies = pd.DataFrame.from_dict(date_Dict)


    # CHECK UNPAID BALANCE
    bal_Dict = {'Loan Number':[], 'Current Principal Balance':[], 'Original Mortgage Amount': [], 'addl_principal': []}
    for i, (CurrPrinBal, OrigMortBal) in enumerate(zip(df1['Current Principal Balance'], df1['Original Mortgage Amount'])):
        if CurrPrinBal != OrigMortBal:
            bal_Dict['Loan Number'].append(df1['Loan Number'][i])
            bal_Dict['Current Principal Balance'].append(CurrPrinBal)
            bal_Dict['Original Mortgage Amount'].append(OrigMortBal)
            bal_Dict['addl_principal'].append(df2['Principal Reduction'][i])
    bal_Discrepancies = pd.DataFrame.from_dict(bal_Dict)


    finalFile = pd.ExcelWriter(dataFilePath + "/DISCREPANCIES.xlsx", engine='xlsxwriter')
    

    PI_Discrepancies.to_excel(finalFile, index=False, sheet_name='P&I Discrepancies')
    date_Discrepancies.to_excel(finalFile, index=False, sheet_name='Due Date Discrepancies')
    bal_Discrepancies.to_excel(finalFile, index=False, sheet_name='Unpaid Balance Discrepancies')

    try:
        finalFile.save()
    except:
        tkinter.messagebox.showerror('Open File Error','Please close the DISCREPANCIES.xlsx file and try again.')



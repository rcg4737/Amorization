import tkinter
from tkinter import messagebox, ttk, filedialog  
from ttkthemes import ThemedTk
import FGMC
import embrace


#   VARIABLES
servicers = ['embrace', 'fgmc']
scripts = [embrace.disc_process, FGMC.disc_process]



#   GUI DESIGN OUTLINE
root = ThemedTk(theme="breeze")
root.title('Discrepancy Report')
root.iconbitmap(r"icon path")



def clear_app():
    filePathEntry.delete(0,'end')
    submitButton["state"] = "enable"
    

def browse_cmd():
    """Opens file explorer browse dialogue box for user to search for files in GUI."""
    clear_app()
    root.filename = filedialog.askdirectory()
    filePathEntry.insert(0, root.filename)
    return None

def go_cmd():
    submitButton["state"] = "disable"
    dataFilePath = filePathEntry.get()

    if dataFilePath == '':
        tkinter.messagebox.showerror('Empty File Path',
        'Please enter the file path to FGMC final data folder.')
        submitButton["state"] = "enable"
        return

    if '003' not in dataFilePath:
        tkinter.messagebox.showerror('File Path Error','Please use the final data file path from the 003_Final Data folder.')
        clear_app()
        return

    print(dataFilePath)
    if 'embrace' in dataFilePath.lower():
        embrace.disc_process(dataFilePath)
    
    if 'fgmc' in dataFilePath.lower():
        FGMC.disc_process(dataFilePath)
    


#   GUI DESIGN LAYOUT
submitButton = ttk.Button(root, text="Submit", command=go_cmd)
filepathLabel = ttk.Label(root, text="Please provide the path to the FGMC fina data folder.")
filePathEntry = ttk.Entry(root,  width=50 )
browseButton = ttk.Button(root, text='Browse', command= browse_cmd)
browseButton.grid(row=1, column=1, pady=10, padx=10)
filepathLabel.grid(row=0, column=0, pady=10, padx=10)
filePathEntry.grid(row=1, column=0, pady=10, padx=10)
submitButton.grid(row=2, column=0, padx=10, pady=10)


root.mainloop()
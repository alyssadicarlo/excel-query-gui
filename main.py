import pandas as pd
import csv
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfile 
from fuzzy import levenshtein_ratio_and_distance

master = tk.Tk()

master.title("File Querying")

s = ttk.Style()
s.theme_use('clam')

header_font = tkFont.Font(size=20)
normal_font = tkFont.Font(size=15)

master_frame = ttk.Frame(master)
master_frame.pack()

top_frame = ttk.Frame(master_frame)
input_frame = ttk.Frame(master_frame)
results_frame = ttk.Frame(master_frame)

ttk.Label(top_frame, text="File Querying Tool", font=header_font).pack(pady=15)

ttk.Label(input_frame, text="Upload your file:", font=normal_font).grid(row=0,column=0, pady=10, padx=10)

file_path = None
def openFile():
    current_file = askopenfile(mode ='r', filetypes =[('Excel File', '*.xls'), ('Excel File', '*.xlsx'), ('CSV File', '*.csv')]) 
    global file_path
    file_path = current_file.name
    ttk.Label(input_frame, text=f"Upload your file:\nOpened: {file_path}", font=normal_font).grid(row=0,column=0, pady=10, padx=10)

file_button = ttk.Button(input_frame, text="Choose File", command=openFile)
file_button.grid(row=0,column=1,columnspan=2, pady=10, padx=10)

ttk.Label(input_frame, text="Enter the search word:", font=normal_font).grid(row=1,column=0, pady=10, padx=10)
search_input = ttk.Entry(input_frame)
search_input.grid(row=1,column=1,columnspan=2,pady=10, padx=15)

ttk.Label(input_frame, text="Check the file type:", font=normal_font).grid(row=2,column=0,padx=10,pady=10)

v = tk.IntVar()
v.set(0)

ttk.Radiobutton(input_frame, text=".csv", variable=v, value=0).grid(row=2,column=1,padx=10,pady=10)
ttk.Radiobutton(input_frame, text=".xlsx", variable=v, value=1).grid(row=2,column=2,padx=10,pady=10)

ttk.Label(input_frame, text="Enter the column you would like to search through:", font=normal_font).grid(row=3,column=0, pady=10, padx=10)
column_input = ttk.Entry(input_frame)
column_input.grid(row=3,column=1,columnspan=2,pady=10, padx=15)

def search():
    global file_path

    target_string = search_input.get()
    target_string  = target_string.upper()
    column_string = column_input.get()

    file_type = v.get()

    current_file = None
    if file_type == 0:
        current_file = getCSV(file_path)
    elif file_type == 1:
        current_file = getExcel(file_path)
    
    list_results = []

    for index in current_file.index:
        if target_string.upper() in current_file[column_string][index].upper():
            list_results.append(current_file.loc[index])

    for index in current_file.index:
        distance = levenshtein_ratio_and_distance(target_string, current_file[column_string][index], ratio_calc = True)
        print(distance)
        if distance > 0.6:
            list_results.append(current_file.loc[index])
    
    results = pd.DataFrame(list_results,columns=current_file.columns.values)
    results = results.drop_duplicates(subset=None, keep='first')

    column_pointer = 0
    for column in results.columns.values:
        ttk.Label(results_frame, text = column).grid(row=0, column=column_pointer, padx=10,pady=10)
        column_pointer += 1
    
    for i in range(0,len(results)):
        for j in range(0,len(results.columns.values)):
            ttk.Label(results_frame, text = results.iloc[i][j]).grid(row=i+1, column=j, padx=10,pady=10)


def getCSV(PATH):
    csv_file = pd.read_csv(PATH)
    return csv_file

def getExcel(PATH):
    excel_file = pd.read_excel(PATH)
    return excel_file

search_button = ttk.Button(input_frame, text="Submit", command=search)
search_button.grid(row=4,columnspan=3,pady=10,padx=10)

top_frame.pack()
input_frame.pack(padx=10)
results_frame.pack()

master.mainloop()
import csv
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


def badPart():
    print('ERROR')
    return


def search(filepath, boxResults):
    data = csv.reader(open(filepath, "r"), delimiter=",")

    searchVal = input('Scan next assembly: ')

    for row in data:
        if searchVal == row[2]:
            boxResults.append(row[0])
            boxResults.append(row[1])
            boxResults.append(row[2])
            boxResults.append(row[3])
            boxResults.append(row[4])
            boxResults.append(row[5])
            boxResults.append(row[6])

            if row[6] == 'PASS':
                return boxResults

            else:
                badPart()


def output():

    def close(event):
        window.destroy()
        root.quit()
        return

    window = tk.Tk()
    n = 0

    for i in range(6):
        window.grid_columnconfigure(i, weight=1)
        window.grid_rowconfigure(i, weight=1)
        for j in range(7):
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )

            frame.grid(row=i, column=j)

            if boxResults[n] == "FAIL" or boxResults[n] == " FAIL" or boxResults[n] == "CHECK" or boxResults[n] == " CHECK":
                label = tk.Label(master=frame, text=boxResults[n], foreground="red3", background="tomato2")
                label.grid(row=i, column=j, sticky="nsew")
                label.pack(expand=True)

            elif boxResults[n] == "PASS" or boxResults[n] == " PASS":
                label = tk.Label(master=frame, text=boxResults[n], foreground="dark green", background="PaleGreen2")
                label.grid(row=i, column=j, sticky="nsew")
                label.pack(expand=True)

            else:
                label = tk.Label(master=frame, text=boxResults[n], foreground="grey1", background="snow")
                label.grid(row=i, column=j, sticky="nsew")
                label.pack(expand=True)

            n += 1

    window.bind("<Key>", close)
    window.mainloop()
    return


filepath = filedialog.askopenfilename()

boxResults = ['Date', 'Time', 'Assembly Number', 'HSI', 'COC', 'OGP', 'Overall']

while True:
    assy = 0
    while assy < 5:
        search(filepath, boxResults)
        assy += 1

    print(boxResults)
    output()

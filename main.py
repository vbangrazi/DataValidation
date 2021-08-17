import csv
import tkinter as tk
from tkinter import filedialog
assy = 0

root = tk.Tk()
root.withdraw()


def badPart():
    print('ERROR')
    return


def search(data, boxResults):

    searchVal = input('Scan next assembly: ')

    for row in data:
        if searchVal == row[2]:
            print(row)
            if row[6] == 'PASS':
                boxResults.append(row[0])
                boxResults.append(row[1])
                boxResults.append(row[2])
                boxResults.append(row[3])
                boxResults.append(row[4])
                boxResults.append(row[5])
                boxResults.append(row[6])
                return boxResults
            else:
                badPart()


def output():

    def close(event):
        window.destroy()
        root.quit()
        return

    window = tk.Tk()

    for i in range(6):
        for j in range(7):
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )

            frame.grid(row=i, column=j)
            label = tk.Label(master=frame, text=f"Row {i} Column {j}")
            label.pack()

    window.bind("<Key>", close)
    window.mainloop()
    return


filepath = filedialog.askopenfilename()
data = csv.reader(open(filepath, "r"), delimiter=",")

while assy < 5:
    boxResults = ['Date', 'Time', 'Assembly Number', 'HSI', 'COC', 'OGP', 'Overall']
    data.seek(0)
    search(data, boxResults)
    assy += 1

print(boxResults)
output()

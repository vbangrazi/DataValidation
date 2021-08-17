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
                return row
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

while assy < 1:
    boxResuts = ['Date', 'Time', 'Assembly Number', 'HSI', 'COC', 'OGP', 'Overall')
    search(data, boxResuts)
    assy += 1

output()

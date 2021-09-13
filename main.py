import csv
import tkinter as tk
from tkinter import filedialog


# step down .csv looking for search, add to box_results
def search(filepath, box_results):
    # reopen .csv file to reset to top of file, reset variables
    data = csv.reader(open(filepath, "r"), delimiter=",")
    global bad_part
    found = False

    search_val = input('Scan next assembly: ')

    if search_val == "":
        search_val = " "

    # provide method for terminating program
    elif search_val == "exit":
        exit()

    else:
        # loop through data to find search value
        for row in data:
            if search_val == row[2]:

                # add row from .csv to list to be returned, verify that part was found
                box_results.append(row[0])
                box_results.append(row[1])
                box_results.append(row[2])
                box_results.append(row[3])
                box_results.append(row[4])
                box_results.append(row[5])
                box_results.append(row[6])
                found = True

                # check if part overall was good
                if row[6] == 'FAIL':
                    bad_part = True

    # record if part was not found in .csv
    if not found:
        box_results.append("Not Found")
        box_results.append("Not Found")
        box_results.append(search_val)
        box_results.append("Not Found")
        box_results.append("Not Found")
        box_results.append("Not Found")
        box_results.append("Not Found")
        bad_part = True

    return box_results


# check that all box parts are unique
def duplicate_check(box_results, scanned_good):
    # check if a part was scanned twice in current box
    global bad_part
    new_scanned_init = [box_results[9], box_results[16], box_results[23], box_results[30], box_results[37]]
    repeat_search_index = 13

    def advance_label():
        # TODO: add motor control
        return

    for part in new_scanned_init:
        if new_scanned_init.count(part) > 1:
            box_results[repeat_search_index] = "REPEAT"

        repeat_search_index += 7

    # check if newly scanned parts were scanned in a previous box
    new_scanned = {box_results[9], box_results[16], box_results[23], box_results[30], box_results[37]}
    no_repeat = new_scanned.isdisjoint(scanned_good)

    if len(new_scanned) < 5:
        bad_part = True

    if not no_repeat:
        bad_part = True

    # check overall results for all parts
    if not bad_part:
        # output label
        advance_label()

    # determine which part numbers are duplicates
    elif not no_repeat:
        repeat_parts = new_scanned.intersection(scanned_good)
        repeat_search_index = 0

        for current_repeat_search in box_results:
            if current_repeat_search in repeat_parts:
                box_results[(repeat_search_index + 4)] = "REPEAT"

            repeat_search_index += 1

    return box_results


# draw window
def output():
    # provide method to close window
    def close(event):
        window.destroy()
        root.quit()
        return

    # ser variables, provide linebreak between boxes
    window = tk.Tk()
    n = 0
    print("Press 'Enter' to exit box view")

    root.overrideredirect(True)
    window.attributes("-fullscreen", True)
    root.resizable(width=False, height=False)

    # define frames, place labels in frame
    for i in range(6):
        window.grid_columnconfigure(i, weight=1)
        window.grid_rowconfigure(i, weight=1)

        for j in range(7):
            frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=i, column=j)

            # define label in frame if box has a problem
            if (box_results[n] == "FAIL" or box_results[n] == " FAIL" or box_results[n] == "CHECK" or
                    box_results[n] == " CHECK" or box_results[n] == "Not Found"):

                pad_x = 100
                pad_y = 60
                label = tk.Label(master=frame, text=box_results[n], foreground="red3", background="tomato2")
                label.grid(row=i, column=j, sticky="nsew")
                label.pack(fill=tk.BOTH, expand=True, ipadx=pad_x, ipady=pad_y)

            # define label in frame if box is good
            elif box_results[n] == "PASS" or box_results[n] == " PASS":
                pad_x = 100
                pad_y = 60
                label = tk.Label(master=frame, text=box_results[n], foreground="dark green", background="PaleGreen2")
                label.grid(row=i, column=j, sticky="nsew")
                label.pack(fill=tk.BOTH, expand=True, ipadx=pad_x, ipady=pad_y)

            elif box_results[n] == "REPEAT":
                pad_x = 100
                pad_y = 60
                label = tk.Label(master=frame, text=box_results[n], foreground="gold4", background="gold2")
                label.grid(row=i, column=j, sticky="nsew")
                label.pack(fill=tk.BOTH, expand=True, ipadx=pad_x, ipady=pad_y)

            # define label in frame for titles
            else:
                if i == 0:
                    pad_y = 40

                else:
                    pad_y = 60

                if j < 3:
                    pad_x = 50

                else:
                    pad_y = 60

                label = tk.Label(master=frame, text=box_results[n], foreground="grey1", background="snow")
                label.grid(row=i, column=j, sticky="nsew")
                label.pack(fill=tk.BOTH, expand=True, ipadx=pad_x, ipady=pad_y)

            n += 1
    # handle window close

    # terminate window on keypress
    window.bind("<Key>", close)
    window.bind("")
    window.mainloop()
    return


# main

# call open file dialog
filepath = filedialog.askopenfilename()
scanned_good = {""}

# Initialize TKinter for drawing window
root = tk.Tk()
root.withdraw()

# loop through box cycles (termination is handled in the search method)
while True:
    # reset variables
    box_results = ['Date', 'Time', 'Assembly Number', 'HSI', 'COC', 'OGP', 'Overall']
    global bad_part
    bad_part = False
    assembly = 0

    # loop through 5 searches
    while assembly < 5:
        search(filepath, box_results)
        assembly += 1

    duplicate_check(box_results, scanned_good)

    # add good parts to scanned list
    if not bad_part:
        new_scanned_init = [box_results[9], box_results[16], box_results[23], box_results[30], box_results[37]]
        scanned_good.update(new_scanned_init)

    output()

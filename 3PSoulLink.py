from tkinter import Menu, Tk, ttk, messagebox, filedialog
import pickle

#Add Soul Link to the corresponding variables
#dictionary links for no route, arrays p1Team and p2Team include routes
def addMons(cnt):
    #Check if two nicknames are entered
    if p1Entry.get() != '' and p2Entry.get() != '' and p3Entry.get() != '':
        #Check if a route has been entered
        if routeEntry.get() != '':
            p1Team.append([p1Entry.get(), routeEntry.get()])
            p2Team.append([p2Entry.get(), routeEntry.get()])
            p3Team.append([p3Entry.get(), routeEntry.get()])
            p1Entry.delete(0, 'end')
            p2Entry.delete(0, 'end')
            p3Entry.delete(0, 'end')
            routeEntry.delete(0, 'end')
        else:
            # links[p1Entry.get()] = {p2Entry.get(), p3Entry.get()}
            links[cnt] = [p1Entry.get(), p2Entry.get(), p3Entry.get()]
            global count
            count += 1
            p1Entry.delete(0, 'end')
            p2Entry.delete(0, 'end')
            p3Entry.delete(0, 'end')
            routeEntry.delete(0, 'end')

#Create window to show all current links
def showAll():
    allMons = ''
    #If routes are being entered, show routes and linked mons
    if p1Team:
        for idx, mon in enumerate(p1Team, start=0):
            allMons += f'{p1Team[idx][1]}: {p1Team[idx][0]} ----- {p2Team[idx][0]} ----- {p3Team[idx][0]}\n'
        # for k, v in links.items():
        #     allMons += f'{k}\t<-->\t{v}\n'
        for i in links.keys():
            allMons += f'{links[i][0]} ----- {links[i][1]} ----- {links[i][2]}\n'
    #If routes are not being entered, only show linked mons
    else:
        # for k, v in links.items():
        #     allMons += f'{k}\t<-->\t{v}\n'
        for i in links.keys():
            allMons += f'{links[i][0]} ----- {links[i][1]} ----- {links[i][2]}\n'
    messagebox.showinfo('Current Soul Links', allMons)

#find the linked pokemon by entering a nickname
def findLink():
    if p1Entry.get() != '':
        p2Entry.delete(0, 'end')
        p3Entry.delete(0, 'end')
        routeEntry.delete(0, 'end')
        #If p1 nickname in links dictionary, show linked p2 nickname
        try:
            # if links[p1Entry.get()]:
            #     p2Entry.insert(0, links[p1Entry.get()][0])
            #     p3Entry.insert[0, links[p1Entry.get()][1]]
            for i in links.keys():
                if p1Entry.get() in links[i]:
                    p2Entry.insert(0, links[i][1])
                    p3Entry.insert(0, links[i][2])
                #If not in links dictionary, find p1 index and show p2 mon on that index and route
                else:
                    p2Entry.insert(0, p2Team[p1Team.index(p1Entry.get())][0])
                    p3Entry.insert(0, p3Team[p1Team.index(p1Entry.get())][0])
                    routeEntry.delete(0, 'end')
                    routeEntry.insert(0, p2Team[p1Team.index(p1Entry.get())][1])
        except KeyError:
            for i in range(len(p1Team)):
                if p1Entry.get() in p1Team[i]:
                    p2Entry.insert(0, p2Team[i][0])
                    p3Entry.insert(0, p3Team[i][0])
                    routeEntry.insert(0, p2Team[i][1])
                    break
            #p2Entry.insert(0, p2Team[p1Team.index(p1Entry.get())])
    #If p2 nickname entered
    elif p1Entry.get() == '' and p2Entry.get() != '' and p3Entry.get() == '':
        p1Entry.delete(0, 'end')
        p3Entry.delete(0, 'end')
        routeEntry.delete(0, 'end')
        #Invert dictionary to search for p1 mon
        # inv_links = {v: k for k,v in links.items()}
        #If p2 mon in dictionary, show linked p1 mon
        try:
            for i in links.keys():
                if p2Entry.get() in links[i]:
                    p1Entry.insert(0, links[i][0])
                    p3Entry.insert(0, links[i][2])
        except KeyError:
            for i in range(len(p2Team)):
                if p2Entry.get() in p2Team[i]:
                    p1Entry.insert(0, p1Team[i][0])
                    p3Entry.insert(0, p3Team[i][0])
                    routeEntry.insert(0, p1Team[i][1])
                    break
    elif p1Entry.get() == '' and p2Entry.get() == '' and p3Entry.get() != '':
        p1Entry.delete(0, 'end')
        p2Entry.delete(0, 'end')
        routeEntry.delete(0, 'end')
        #Invert dictionary to search for p1 mon
        # inv_links = {v: k for k,v in links.items()}
        #If p2 mon in dictionary, show linked p1 mon
        try:
            for i in links.keys():
                if p3Entry.get() in links[i]:
                    p1Entry.insert(0, links[i][0])
                    p2Entry.insert(0, links[i][1])
        except KeyError:
            for i in range(len(p3Team)):
                if p3Entry.get() in p3Team[i]:
                    p1Entry.insert(0, p1Team[i][0])
                    p2Entry.insert(0, p2Team[i][0])
                    routeEntry.insert(0, p1Team[i][1])
                    break

#menu entry to close program
def close():
    root.destroy()

#Save all links to json file
def saveFile():
    saveDict = {'p1Team': p1Team,
    'p2Team': p2Team,
    'links': links}
    #Open "save as" dialog and save the file in chosen path as chosen name
    fileName = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension='.json', filetypes=[('JSON Document', '*.json')])
    with open(fileName, 'wb') as file:
        pickle.dump(saveDict, file)

#Load all links from a previously saved file
def openFile():
    global p1Team, p2Team, links
    #Open file dialog to select a json file to load
    fileName = filedialog.askopenfilename(defaultextension='.json',filetypes=[('JSON Documents', '*.json')])
    #Open file and create tuples and dictionary to load json objects
    with open(fileName, 'rb') as fileReader:
        openDict = pickle.load(fileReader)
        try:
            p1Team = openDict['p1Team']
            p2Team = openDict['p2Team']
            links = openDict['links']
        #If file is not correct, show error window
        except KeyError as exc:
            messagebox.showerror('Cannot open file', exc.args)
            pass

#Create main window with title and make it not resizable
root = Tk()
root.title('Soul Link Helper')
root.resizable(False, False)
#Create variables to store links and routes
p1Team = []
p2Team = []
p3Team = []
links = {}
count = 0
#Create menubar for save/load functionality
menubar = Menu(root)
file = Menu(menubar, tearoff=0)
file.add_command(label='Load', command=openFile)
file.add_command(label='Save as...', command=saveFile)
file.add_command(label='Close', command=close)
menubar.add_cascade(label='File', menu=file)
root.config(menu=menubar)
#Create Route label
routeLabel = ttk.Label(root, text='Route :')
routeLabel.grid(row=0, column=0, padx=5, pady=5, sticky='w')
#Create text box for entering the route/place the mon was obtained at
routeEntry = ttk.Entry(root, width=40)
routeEntry.grid(row=0, column=1, columnspan=3)
#Create p1 label
p1Label = ttk.Label(root, text='Player 1')
p1Label.grid(row=1, column=1)
#Create p2 label
p2Label = ttk.Label(root, text='Player 2')
p2Label.grid(row=1, column=2)
#Create 3p label
p3Label = ttk.Label(root, text='Player 3')
p3Label.grid(row=1, column=3)
#Create nickname label
nickLabel = ttk.Label(root, text='Nickname :')
nickLabel.grid(row=2, column=0, padx=5)
#Create text boxes for p1 and p2 and p3 nickname to be entered
p1Entry = ttk.Entry(root, width=15)
p1Entry.grid(row=2, column=1, padx=5, pady=[5,0])
p2Entry = ttk.Entry(root, width=15)
p2Entry.grid(row=2, column=2, padx=5, pady=[5,0])
p3Entry = ttk.Entry(root, width=15)
p3Entry.grid(row=2, column=3, padx=5, pady=[5,0])
#Create button to find the linked mon
findButton = ttk.Button(root, text='find link', width=12, command=findLink)
findButton.grid(row=3, column=1, pady=5)
#Create button to add links to variables
addButton = ttk.Button(root, text='add new link', width=15, command=lambda: addMons(count))
addButton.grid(row=3, column=2, pady=5)
#Create button to show all currently loaded links
allButton = ttk.Button(root, text='show all links', width=15, command=showAll)
allButton.grid(row=3, column=3, pady=5)
#Direct flow to main window and keep it open
root.mainloop()
import Tkinter as tk
from Tkinter import StringVar, Label, Entry

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class AddProject:
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		label = tk.Label(self, text="ADD PROJECT DETAILS")
		label.pack(side="top", fill="both", expand=True)

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       #label = tk.Label(self, text="All Projects")
       #label.pack(side="top", fill="both", expand=True) 
       #b5 = tk.Button(buttonframe, text="Project One") 
       #b5.pack(side="top", fill="both", expand=True)

       #add = AddProject(self) 
       #add.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
       buttonframe = tk.Frame(self)
       container = tk.Frame(self)
       buttonframe.pack(side="top", fill="both", expand=False)
       container.pack(side="top", fill="both", expand=True)
       
       b5 = tk.Button(buttonframe, text="Project One") 
       b5.pack(side="top", fill="both", expand=True)

       b6 = tk.Button(buttonframe, text="Project Two") 
       b6.pack(side="top", fill="both", expand=True)

       b7 = tk.Button(buttonframe, text="Project Three") 
       b7.pack(side="top", fill="both", expand=True)

       b8 = tk.Button(buttonframe, text="Project Four") 
       b8.pack(side="top", fill="both", expand=True)

       b4 = tk.Button(buttonframe, text="Add Project", command=self.create_window)
       b4.pack(side="bottom") 

   def create_window(self):
   	t = tk.Toplevel(self)
   	t.wm_title("New Project")
   	l = tk.Label(t, text="NEW PROJECT")
   	l.pack(side="top", fill="both", expand=True) 


   	label = tk.Label(self, text="Project Name")
   	
   	# label_input = tk.Label(self, text="Search")
   	# e = tk.Entry(t)
   	# #e.insert(0, "a default value")
   	# e.pack(side="top", fill="both", padx=100)
   	# # e.grid(row=0, column=1)

   	labelText=StringVar()
	labelText.set("Project Title")
	labelDir=Label(t, textvariable=labelText, height=4)
	labelDir.pack(side="top", fill="both", expand=True)

	directory=StringVar(None)
	dirname=Entry(t,textvariable=directory,width=50)
	dirname.pack(side="top", fill="both", expand=True) 

	#namebox.insert(END, names + '\n')
	
	labelText=StringVar()
	labelText.set("Project Description")
	labelDir=Label(t, textvariable=labelText, height=4)
	labelDir.pack(side="top", fill="both", expand=True)

	directory=StringVar(None)
	dirname=Entry(t,textvariable=directory,width=50)
	dirname.pack(side="top", fill="both", expand=True)

	labelText=StringVar()
	labelText.set("Project Deadline")
	labelDir=Label(t, textvariable=labelText, height=4)
	labelDir.pack(side="top", fill="both", expand=True)

	directory=StringVar(None)
	dirname=Entry(t,textvariable=directory,width=50)
	dirname.pack(side="top", fill="both", expand=True)

	labelText=StringVar()
	labelText.set("Project Team Members")
	labelDir=Label(t, textvariable=labelText, height=4)
	labelDir.pack(side="top", fill="both", expand=True)

	directory=StringVar(None)
	dirname=Entry(t,textvariable=directory,width=50)
	dirname.pack(side="top", fill="both", expand=True) 

	#buttonframe = tk.Frame(self)
	#save = tk.Button(buttonframe, text="Save Project")
	#save.pack(side="left")

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)

class Page4(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 4")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self) 
        p4 = Page4(self) 
        

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1) 

        b1 = tk.Button(buttonframe, text="Projects", command=p1.lift)
        #b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        #b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)
        #b4 = tk.Button(buttonframe, text="Page 4", command=p4.lift) 
        

        b1.pack(side="left")
        #b2.pack(side="left")
        #b3.pack(side="left")
        

        #b4.pack(side="left") 
        

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
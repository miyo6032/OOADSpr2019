import tkinter as tk
from tkinter import StringVar, Label, Entry

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
       
       b5 = tk.Button(buttonframe, text="Project One", command=self.create_tasks_window) 
       b5.pack(side="top", fill="both", expand=True)

       b6 = tk.Button(buttonframe, text="Project Two") 
       b6.pack(side="top", fill="both", expand=True)

       b7 = tk.Button(buttonframe, text="Project Three") 
       b7.pack(side="top", fill="both", expand=True)

       b8 = tk.Button(buttonframe, text="Project Four") 
       b8.pack(side="top", fill="both", expand=True)

       b4 = tk.Button(buttonframe, text="Add Project", command=self.create_window)
       b4.pack(side="bottom")  


    def create_tasks_window(self):

      t = tk.Toplevel(self)
      t.wm_title("Project Details")
      
      nameFrame = tk.LabelFrame(t, pady = 0)  
      nameFrame.pack(side="top", fill="both")

      detailsFrame = tk.LabelFrame(t, pady = 0) 
      detailsFrame.pack(side="left", fill="both")
      
      tasksFrame = tk.LabelFrame(t, pady=0) 
      tasksFrame.pack(side="left", fill="both") 
      
      miniFrame = tk.LabelFrame(tasksFrame, pady=0) 
      miniFrame.pack(side="bottom", fill="both")

      l = tk.Label(detailsFrame, text="Project Details", bg="white", fg="black", borderwidth=5, relief="groove")
      l.pack(side="top", fill="both", expand=True)
      label = tk.Label(self, text="Project Name")

      projectTitle=StringVar()
      projectTitle.set("Project Title")
      labelDir=Label(nameFrame, textvariable=projectTitle, height=4, bg="white", fg="black", borderwidth=5, relief="groove")
      labelDir.pack(side="top", fill="both", expand=True)

      projDeadline=StringVar()
      projDeadline.set("Project Deadline")
      labelDir=Label(detailsFrame, textvariable=projDeadline, height=4, bg="white", fg="black", borderwidth=5, relief="groove")
      labelDir.pack(side="top", fill="both", expand=True)

      #projDeadlineField=StringVar(None)
      #dirname=Entry(t,textvariable=projDeadlineField,width=50)
      #dirname.pack(side="top", fill="both", expand=True) 

      projDeadline=StringVar()
      projDeadline.set("Active Team Members")
      labelDir=Label(detailsFrame, textvariable=projDeadline, height=4, bg="white", fg="black", borderwidth=5, relief="groove")
      labelDir.pack(side="top", fill="both", expand=True)

      #projDeadlineField=StringVar(None)
      #dirname=Entry(t,textvariable=projDeadlineField,width=50)
      #dirname.pack(side="top", fill="both", expand=True)   

      addTasks = tk.Button(miniFrame, text="Main Menu")
      addTasks.pack(side="left", fill="both")

      addTasks = tk.Button(miniFrame, text="Add Tasks", command=self.create_add_tasks_window)
      addTasks.pack(side="right", fill="both")

    def create_add_tasks_window(self): 
      t = tk.Toplevel(self)
      t.wm_title("Add Tasks Page") 

      headerFrame = tk.LabelFrame(t, pady = 0)  
      headerFrame.pack(side="top", fill="both")

      l = tk.Label(headerFrame, text="TASKS")
      l.pack(side="top", fill="both", expand=True) 
      label = tk.Label(self, text="Project Name") 

      taskTitle=StringVar()
      taskTitle.set("Task Title")
      labelDir=Label(t, textvariable=taskTitle, height=4)
      labelDir.pack(side="top", fill="both", expand=True)

      taskTitleField=StringVar(None)
      dirname=Entry(t,textvariable=taskTitleField,width=50)
      dirname.pack(side="top", fill="both", expand=True) 

      taskDescription=StringVar()
      taskDescription.set("Task Description")
      labelDir=Label(t, textvariable=taskDescription, height=4)
      labelDir.pack(side="top", fill="both", expand=True)

      taskDescriptionField=StringVar(None)
      dirname=Entry(t,textvariable=taskDescriptionField,width=50)
      dirname.pack(side="top", fill="both", expand=True)  

      taskDeadline=StringVar()
      taskDeadline.set("Task Deadline")
      labelDir=Label(t, textvariable=taskDeadline, height=4)
      labelDir.pack(side="top", fill="both", expand=True)

      taskDeadlineField=StringVar(None)
      dirname=Entry(t,textvariable=taskDeadlineField,width=50)
      dirname.pack(side="top", fill="both", expand=True)  

      taskMembers=StringVar()
      taskMembers.set("Members Associated to Task")
      labelDir=Label(t, textvariable=taskMembers, height=4)
      labelDir.pack(side="top", fill="both", expand=True)

      taskMembersField=StringVar(None)
      dirname=Entry(t,textvariable=taskMembersField,width=50)
      dirname.pack(side="top", fill="both", expand=True)  

      choicesFrame = tk.LabelFrame(t, pady = 0)  
      choicesFrame.pack(side="top", fill="both")

      confirmTask = tk.Button(choicesFrame, text="Confirm Task")
      confirmTask.pack(side="bottom", fill="both")

      cancel = tk.Button(choicesFrame, text="Cancel")
      cancel.pack(side="bottom", fill="both")


    
    def create_window(self):
        t = tk.Toplevel(self)
        t.wm_title("New Project")
        l = tk.Label(t, text="NEW PROJECT")
        l.pack(side="top", fill="both", expand=True) 


        label = tk.Label(self, text="Project Name")
        
        labelText=StringVar()
        labelText.set("Project Title")
        labelDir=Label(t, textvariable=labelText, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        directory=StringVar(None)
        dirname=Entry(t,textvariable=directory,width=50)
        dirname.pack(side="top", fill="both", expand=True) 
        
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

        b1.pack(side="left")
        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
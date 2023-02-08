import tkinter
import customtkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import docScanner as ds
import numpy as np
import cv2
import imageCrop as ic

class ImageObject():
    def __init__(self, id, imagePath, scan=False):
        self.id = id
        self.imagePath = imagePath
        self.scan = scan
        self.image = None

class DocMaker():
    imageList=[]
    selectedId=0

    def __init__(self):
        self.__window=tk.CTk()
        self.__window.title("DocMaker")
        # self.__window.state("zoomed")
        self.__window.geometry("860x700" + "+%d+%d" % (self.__window.winfo_screenwidth()/2-860/2, self.__window.winfo_screenheight()/2-700/2))

        # for i in range(0,10):
        #     self.imageList.append(ImageObject(i,"1.jpg"))
        #     self.imageList[i].image=Image.open(self.imageList[i].imagePath)

        self.docGUI()

    def docGUI(self):

        ########## ImageList Frame ##########
        self.__imageFrame=tk.CTkFrame(master=self.__window)
        self.__imageFrame.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

        self.__imageCanvas=tk.CTkCanvas(master=self.__imageFrame, bg="Black",width=200)
        self.__imageCanvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

        self.__imageScroll=tk.CTkScrollbar(master=self.__imageFrame,command=self.__imageCanvas.yview)
        self.__imageScroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)

        self.__imageCanvas.config(yscrollcommand=self.__imageScroll.set)
        self.__imageCanvas.bind('<Configure>',lambda event: self.__imageCanvas.configure(scrollregion=self.__imageCanvas.bbox("all")))

        self.__imageFrame2=tk.CTkFrame(master=self.__imageCanvas,fg_color="Black" ) #
        self.__imageCanvas.create_window((10,20),window=self.__imageFrame2,anchor="nw")

        self.__imageLabel=tk.CTkLabel(master=self.__imageFrame2,text="Image List")
        self.__imageLabel.grid(row=0,column=0,padx=5,pady=5,sticky="sw")

        self.__imageCanvas.config(height=1000)

        ########## Show Frame ##########
        self.__showFrame=tk.CTkFrame(master=self.__window)
        self.__showFrame.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)

        self.__moveEntry=tk.CTkEntry(master=self.__showFrame,width=50)
        self.__moveImage=tk.CTkButton(master=self.__showFrame,text="Move Image",command=lambda : self.moveImage(self.getID(),self.__moveEntry.get()),width=50)

        self.__moveImage.pack(side=tkinter.BOTTOM)
        self.__moveEntry.pack(side=tkinter.BOTTOM)

        self.__prevButton=tk.CTkButton(master=self.__showFrame,text="prev",command=lambda: self.prevImage(),width=50)
        self.__prevButton.pack(side=tkinter.LEFT)


        self.__showImage=tk.CTkLabel(master=self.__showFrame, width=350,height=480,fg_color="Black",bg_color="Black", text="")
        self.__showImage.pack(side=tkinter.LEFT,expand=True)

        self.__nextButton=tk.CTkButton(master=self.__showFrame,text="Next",command=lambda: self.nextImage(),width=50)
        self.__nextButton.pack(side=tkinter.RIGHT)



        ########## Button Frame ##########
        self.__buttonFrame=tk.CTkFrame(master=self.__window)
        self.__buttonFrame.pack(side=tkinter.BOTTOM,fill=tkinter.X,expand=True)

        self.__addImageStart=tk.CTkButton(master=self.__buttonFrame,text="Add Image Start",command=lambda: self.addImage(0))
        self.__addImageStart.grid(row=0,column=0,padx=5,pady=5,sticky="sw")

        self.__addImage=tk.CTkButton(master=self.__buttonFrame,text="Add Image",command=lambda: self.addImage(self.selectedId+1))
        self.__addImage.grid(row=0,column=1,padx=5,pady=5,sticky="sw")

        self.__addImageEnd=tk.CTkButton(master=self.__buttonFrame,text="Add Image End",command=lambda: self.addImage(len(self.imageList)))
        self.__addImageEnd.grid(row=0,column=2,padx=5,pady=5,sticky="sw")

        self.__removeImage=tk.CTkButton(master=self.__buttonFrame,text="Remove Image",command=lambda: self.removeImage(index=self.getID()))
        self.__removeImage.grid(row=0,column=3,padx=5,pady=5,sticky="sw")

        self.__scanImage=tk.CTkButton(master=self.__buttonFrame,text="Scan Image",command=lambda: self.scanImage(index=self.getID()))
        self.__scanImage.grid(row=1,column=1,padx=5,pady=5,sticky="sw")

        self.__saveDoc=tk.CTkButton(master=self.__buttonFrame,text="Save PDF",command=lambda: self.saveDoc())
        self.__saveDoc.grid(row=1,column=2,padx=5,pady=5,sticky="sw")

        self.__clearList=tk.CTkButton(master=self.__buttonFrame,text="Clear List",command=lambda: self.clearList())
        self.__clearList.grid(row=1,column=3,padx=5,pady=5,sticky="sw")

        self.__controlLabel=tk.CTkLabel(master=self.__buttonFrame,text="       Controls",font=("Arial", 17,))
        self.__controlLabel.grid(row=1,column=0,padx=5,pady=5,sticky="sw")


        self.__window.mainloop()

    def clearList(self):
        self.imageList.clear()
        self.displayImage()

    def addImage(self, index):
        try:               
            if len(self.imageList)==0:
                index=0
                                              #initialdir="/",   
            self.filename=filedialog.askopenfilenames(title="Select file",filetypes=(("jpeg files","*.jpg"),("jpeg files","*.jpeg"),("png files","*.png"),("all files","*.*")))
            for i,filename in enumerate(self.filename, start=index):
                self.imageList.insert(i,ImageObject(i,filename))

                for j in range(index,len(self.imageList)):
                    self.imageList[j].id=j

                orig=cv2.imread(filename)
                self.imageList[i].image=Image.fromarray(orig)
                
            self.displayImage()
                
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def displayImage(self):
        for widget in self.__imageFrame2.winfo_children():
            if "ctkbutton" in widget.winfo_name():
                widget.destroy()
         
        for image in self.imageList:
            img=tk.CTkImage(image.image, size=(100,200))
            imageButton=tk.CTkButton(master=self.__imageFrame2, text= image.id, command=lambda x=image.id: self.clickImage(x), border_width=5, fg_color="Black", image=img)
            imageButton.grid(row=image.id+1,column=1,padx=10,pady=10)

        height=self.__imageFrame2.winfo_height()*len(self.imageList)
        # print(height)
        self.__imageCanvas.config(height=height) 
        self.__imageCanvas.bind('<Configure>',lambda e: self.__imageCanvas.configure(scrollregion=self.__imageCanvas.bbox("all")))

    
    def removeImage(self, index):
        if len(self.imageList)==0:
            messagebox.showerror("Error","No Image to Remove")
            return
        self.imageList.pop(index)
        for i in range(index,len(self.imageList)):
            self.imageList[i].id=i
        self.displayImage()

        if self.getID()>=len(self.imageList):
            self.setID(len(self.imageList)-1)

    def clickImage(self, index):
        self.setID(index)
        self.__showImage.configure(image=tk.CTkImage(self.imageList[self.getID()].image, size=(350,480)))
        # Image.open(self.imageList[self.getID()].imagePath).show()

    
    def moveImage(self, index, newIndex):
        newIndex=int(newIndex)
        if newIndex<0:
            newIndex=0
        if newIndex>len(self.imageList)-1:
            newIndex=len(self.imageList)-1

        self.imageList.insert(newIndex,self.imageList.pop(index))
        for i in range(len(self.imageList)):
            self.imageList[i].id=i
        self.setID(value=newIndex)
        self.displayImage()

    def getID(self):
        return self.selectedId
    def setID(self, value):
        self.selectedId=value

    def prevImage(self):
        try:
            if self.getID()>0:
                self.setID(self.getID()-1)
            else:
                self.setID(0)
            self.__showImage.configure(image=tk.CTkImage(self.imageList[self.getID()].image, size=(350,480)))
        except:
            pass

    def nextImage(self):
        try:
            if self.getID()<len(self.imageList)-1:
                self.setID(self.getID()+1)
            else:
                self.setID(len(self.imageList)-1)
            self.__showImage.configure(image=tk.CTkImage(self.imageList[self.getID()].image, size=(350,480)))
        except:
            pass

    def scanImage(self, index):
        try: 
            scantype=messagebox.askquestion("Scan Image","Do you want to let AI scan it?")
            if scantype=="yes":
                wrap=ds.imageScanner(imagePath=self.imageList[index].imagePath)
                self.imageList[index].scan=True
                self.imageList[index].image=Image.fromarray(wrap)
            else:
                instructions=messagebox.showinfo("Control","Use mouse to select the area to scan \n press 'c' to crop the image \n press 'r' to reset the selection \n press 'q' to cancel the selection")

                imageCropper = ic.ImageCropper(self.imageList[index].imagePath)
                croppedImage = imageCropper.crop()
                
                if croppedImage is not None:
                    self.imageList[index].scan=True
                    self.imageList[index].image=Image.fromarray(croppedImage) 
            self.displayImage()
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def saveDoc(self):
        try:
            if len(self.imageList)==0:
                messagebox.showerror("Error","No Image to Save")
                return
            filename=filedialog.asksaveasfilename(title="Save file",filetypes=(("pdf files","*.pdf"),("all files","*.*")))
            if filename=="":
                return
            if ".pdf" not in filename:
                filename+=".pdf"

            append_images=[]
            for image in self.imageList:
                if image.scan:
                    append_images.append(image.image)
                else:
                    append_images.append(Image.open(image.imagePath))    
            append_images[0].save(filename,save_all=True, append_images=append_images[1:])
            messagebox.showinfo("Success","Document Saved Successfully")

        except Exception as e:
            messagebox.showerror("Error",str(e))

if __name__=="__main__":
    dm=DocMaker()





    

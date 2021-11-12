from __future__ import unicode_literals
from tkinter import ttk, filedialog, StringVar
from tkinter import *
import youtube_dl
import threading
import os


def download_source(link, option):
        """
        Function to download script

        Params:
        link: str, can be a list of links e.g. 'url1','url2'
        option: str, select mp3 or mp4
        """

        link = "{}".format(link)

        if option == 'mp3':
            ydl_opts = {
                'writethumbnail': True,
                'format': 'bestaudio/best',
                'outtmpl': os.getcwd() + '/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }, {'key': 'EmbedThumbnail'}, {'key': 'FFmpegMetadata'}], }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])   #options for youtube download
        if option == 'mp4':
            with youtube_dl.YoutubeDL({'format': 'bestvideo+bestaudio/best'}) as ydl:
                ydl.download([link]) - force - generic - extractor


def click():
    """
    Command for button once run button is clicked
    """
    download_source(link=textentry.get(), option=option_var.get())
    progress['value']=150

def threaded_click():
    """
    Run a threaded verison of click to prevent freezing.
    """
    progress['value']=20
    t=threading.Thread(target=click)
    t.start()
    progress['value']=60

def sel():
    """
    Selecting either mp3 or mp4
    """
    selection = "You selected the option " + str(option_var.get())
    print(selection)

def browse_button():
    """
    Allow user to select a directory and store it in global var call file path. Used to change
    save location.
    """
    global folder_path
    location = filedialog.askdirectory()
    folder_path.set(location)
    os.chdir(f'{location}')
    print('File will be saved at:'+os.getcwd())


# create root (initalise tkkitner window)
root = Tk()
root.title("Youtube download tool")
root.configure(background="lightgrey")
root.geometry("550x200")

# Link entry and run button
Label(root, text="Enter Link", bg="lightgrey", fg="black").grid(row=4, column=0)  #create label
textentry = Entry(root, width=20, bg="white")  #insert text box
textentry.grid(row=4, column=2, sticky="W")
Button(root, text="Run!", width=6, command=threaded_click)\
    .grid(row=8, column=2, sticky=W)   #run button with threaded click

# Radio buttons to select mp3/mp4
option_var = StringVar()
option_var.set('mp3')  #default option

R1 = Radiobutton(root, text="mp3", variable=option_var, value='mp3',
                 command=sel, bg='lightgrey')  #check mp3
R1.grid(column=2, row=2, sticky="W")

R2 = Radiobutton(root, text="mp4", variable=option_var, value='mp4',
                 command=sel, bg='lightgrey') #check mp4
R2.grid(column=2, row=3, sticky="W")
Label(root, text="File Type:", bg="lightgrey", fg="black").grid(row=1, column=0)


#progress bar
progress=ttk.Progressbar(root,orient=HORIZONTAL,length=150,mode='determinate')
progress.grid(column=7,row=8,pady=5)
Label(root, text="Progress", bg="lightgrey", fg="black").grid(row=7, column=7) #create progress bar


#directory change button
folder_path= StringVar()
folder_path.set(os.getcwd())  #set original cwd

lbl_cwd = Label(master=root,textvariable=folder_path) #show user current save location
lbl_cwd.grid(row=2, column=7)

buttonBrowse = Button(text="Browse save location", command=browse_button,height=2)
buttonBrowse.grid(row=3, column=7)   #button to browse and change save location

root.mainloop()

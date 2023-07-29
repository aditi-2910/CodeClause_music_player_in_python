import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

class Player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.pack()

        mixer.init()

        if(os.path.exists('song.pickle')):
            with open('song.pickle', 'rb') as f:
                self.playlist=pickle.load(f)
        else:
            self.playlist=[]

        self.currentSong=0
        self.paused=True
        self.played=False

        self.create_frames()
        self.track_widgets()
        self.tracklist_widgets()
        self.control_widgets()

    def create_frames(self):
        self.track=tk.LabelFrame(self,text='Currently Playing',font=('Comic Sans', 10, 'bold'),bg='black',fg='white',bd=5,relief=tk.GROOVE)
        self.track.configure(height=300, width=500, bg='black')
        self.track.grid(row=0, column=0)

        self.tracklist=tk.LabelFrame(self,text=f'Playlist - {len(self.playlist)}',font=('Comic Sans', 10, 'bold'),bg='black',fg='white',bd=5,relief=tk.GROOVE)
        self.tracklist.configure(height=404, width=250, bg='black')
        self.tracklist.grid(row=0, column=1, rowspan=2)

        self.controls=tk.LabelFrame(self,font=('Comic Sans', 10, 'bold'),bg='black',fg='white',bd=5,relief=tk.GROOVE)
        self.controls.configure(height=100, width=500, bg='black')
        self.controls.grid(row=1, column=0)
    
    def track_widgets(self):
        self.canvas=tk.Label(self.track, image=music, bg='#E6A9E4')
        self.canvas.configure(height=360, width=480)
        self.canvas.grid(row=0, column=0)

        self.label = tk.Label(self.track, bg='white')
        self.label['text']='MP3 player'
        self.label.configure(height=1, width=68)
        self.label.grid(row=1, column=0)


    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

        self.list=tk.Listbox(self.tracklist ,selectmode=tk.SINGLE, selectbackground='sky blue', yscrollcommand=self.scrollbar.set)
        self.addSongs()
        self.list.config(height=27, width=27)
        self.list.bind('<Double-1>', self.playSong)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)


    def control_widgets(self):
        self.loadSongs = tk.Button (self.controls, bg='green', fg='black', text='Load Songs', command=self.retrieveSongs, width= 15)
        self.loadSongs.grid(row=0, column=0, padx=25)

        self.previous = tk.Button (self.controls, image=previous, command=self.previousSong)
        self.previous.grid(row=0, column=1)

        self.pause = tk.Button (self.controls, image=play, command=self.pauseSong)
        self.pause.grid(row=0, column=2)

        self.next = tk.Button (self.controls,image=next, command=self.nextSong)
        self.next.grid(row=0, column=3)

        self.volume=tk.DoubleVar()
        self.slider=tk.Scale(self.controls, from_=0, to=10, variable=self.volume, orient=tk.HORIZONTAL, width=5, showvalue=0, sliderlength=10, length=150)
        self.slider.set(6)
        mixer.music.set_volume(0.6)
        self.slider['command']=self.changeVolume
        self.slider.grid(row=0, column=4, padx=25)

    def addSongs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def retrieveSongs(self):
        self.songlist=[]
        directory=filedialog.askdirectory()
        for root, dir, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1]=='.mp3':
                    path=(root + '/' + file).replace('\\', '/')
                    self.songlist.append(path)

        with open('song.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)
        
        self.playlist=self.songlist
        self.tracklist['text']=f'Playlist - {len(self.playlist)}'
        self.list.delete(0, tk.END)
        self.addSongs()

    
    def previousSong(self):
        if self.currentSong>0:
            self.list.itemconfigure(self.currentSong, bg='white')
            self.currentSong-=1
        else:
            self.currentSong=0
        self.playSong()

    def pauseSong(self):
        if not self.paused:
            mixer.music.pause()
            self.paused=True
            self.pause['image']=play
            self.played=True
        else:
            if self.played==False:
                self.playSong()
            mixer.music.unpause()
            self.paused=False
            self.pause['image']=pause


    def playSong(self, event=None):
        if event is not None:
            self.currentSong=self.list.curselection()[0]
            for i in range (len(self.playlist)):
                self.list.itemconfigure(i, bg='white')

        self.pause['image']=pause
        self.paused=False
        self.played=True
        mixer.music.load(self.playlist[self.currentSong])
        self.label['anchor']='w'
        self.label['text']=os.path.basename(self.playlist[self.currentSong])
        self.list.activate(self.currentSong)
        self.list.itemconfig(self.currentSong, bg='sky blue')
        mixer.music.play()

    def nextSong(self):
        if self.currentSong<len(self.playlist)-1:
            self.list.itemconfigure(self.currentSong, bg='white')
            self.currentSong+=1
        else:
            self.currentSong=len(self.playlist)-1
        self.playSong()

    def changeVolume(self, event=None):
        self.v=self.volume.get()
        mixer.music.set_volume(self.v/10)



root=tk.Tk()
root.geometry('710x470')
root.configure(bg='black')
root.wm_title('Music Player by Aditi')

music = PhotoImage(file='boombox.png')
previous = PhotoImage (file='previous.png')
pause = PhotoImage (file='pause.png')
next = PhotoImage (file='next.png')
play = PhotoImage(file='play.png')

app=Player(master=root)

root.mainloop()
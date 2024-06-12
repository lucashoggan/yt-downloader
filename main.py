from pytube import YouTube
import os, json, sys, math
from typing import List
from threading import Thread
from tkinter import *
from tkinter import filedialog

JSON_FILE_PATH = "url_list.json"
OUTPUT_FOLDER_PATH = "audio"
THREAD_COUNT = 5
AUDIO = True

def get_urls(filename:str):
    with open(filename, 'r') as f:
        return json.load(f)

def split(a, n): 
    chunk_size = math.floor(len(a)/n)
    return [a[i:i + chunk_size] for i in range(0, len(a), chunk_size)]

def start_download(urls, path):
    for url in urls:
        yt = YouTube(url)
        print(f'"{yt.title}" started downloading')
        
        
        
        if AUDIO:
            
            vid = yt.streams.filter(only_audio=True).first()
            out_file = vid.download(output_path=path)
            new_file = os.path.splitext(out_file)[0] + ".mp3"
            os.rename(out_file, new_file)
        else:
            vid = yt.streams.filter(only_audio=True).first()
            out_file = vid.download(output_path=path)
        print(f'"{yt.title}" Downloaded')
        

def start_threads():
    
    try:
        THREAD_COUNT = int(threadsV.get())
        print("Thread count:", THREAD_COUNT)
        print("Json file path", JSON_FILE_PATH)
        print("OUTPUT_FOLDER_PATH", OUTPUT_FOLDER_PATH)
        if JSON_FILE_PATH != "" and OUTPUT_FOLDER_PATH != "" and THREAD_COUNT != 0:
            app.destroy()
            urls = get_urls(JSON_FILE_PATH)
            sep_urls:List[List[str]]
            
            
            
            if len(urls) % THREAD_COUNT == 0:
                sep_urls = split(urls, THREAD_COUNT)
            else:
                
                sep_urls = split(urls[:(len(urls) - len(urls)%THREAD_COUNT)], THREAD_COUNT)
                excess = urls[(len(urls) - len(urls)%THREAD_COUNT):]

                for i in range(len(excess)):
                    sep_urls[i].append(excess[i])

            threads = [Thread(target=start_download, args=(u, OUTPUT_FOLDER_PATH)) for u in sep_urls]

            [t.start() for t in threads]
            [t.join() for t in threads]
        else:
            e = Tk()
            Label(e, text="INVALID INPUT", font=("sans-serif", 20)).pack()
            e.mainloop()
    except ValueError:
        e = Tk()
        Label(e, text="INVALID INPUT", font=("sans-serif", 20)).pack()
        e.mainloop()
    
    
    
    
    
    
    

    
    
   
    
def browseUrlFile():
    global JSON_FILE_PATH
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("JSON files", "*.json*"), ("all files", "*.*")))
    JSON_FILE_PATH = filename
    
    json_file_btn.config(text=f"File selected: {filename.split('/')[-1]}") 

def browseOutDir():
    global OUTPUT_FOLDER_PATH
    folder_path = filedialog.askdirectory(initialdir="/", title="Select a Folder")
    OUTPUT_FOLDER_PATH = folder_path
    
    out_dir_btn.config(text=f"Folder selected: {folder_path.split('/')[-1]}")


if __name__ == "__main__":
  
    app = Tk()
    app.title("YouTube Downloader")
    app.geometry("400x250")
    heading = Label(app, text="YouTube Downloader", font=('Times New Roman', 15))
    heading.grid(row=0, column=1)

    
    threadsV = StringVar(app, "5")
    

    

    fileChoiceFrame = Frame(app)

    json_file_btn = Button(fileChoiceFrame, text="Select a url list", command=browseUrlFile)
    json_file_btn.grid(row=0, column=0)
    
    out_dir_btn = Button(fileChoiceFrame, text="Select a output folder", command=browseOutDir)
    out_dir_btn.grid(row=1, column=0)

    fileChoiceFrame.grid(row=2, column=0)

    threads_lbl = Label(app, text="Threads:")
    threads_lbl.grid(row=3, column=0)

    threads_ent = Entry(app, textvariable=threadsV, width=10)
    threads_ent.grid(row=3, column=1)

    dl_btn = Button(app, text="Download", command=start_threads)
    dl_btn.grid(row=4, column=0, columnspan=2, pady=5)

    app.mainloop()

    
    

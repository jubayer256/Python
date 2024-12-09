import time
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Progressbar, Treeview
from youtube.script import YouTube
from scripts.calculate import *
from scripts.database import *
from scripts.fileinfo import *

PAUSE_BUTTON_CLICKED = False  # check if pause button is clicked or not
RESUME_BUTTON_CLICKED = False  # check if resume button is clicked or not


# add a link to the download process list
class AddToList:
    def __init__(self, u):
        self.url = u
        self.add()

    def add(self):
        if db.is_exists(self.url):
            messagebox.showinfo(message="Task exists")
            return
        else:
            if self._youtube_video():
                self._add_youtube_video()
            else:
                self._add_other_files()

    def _youtube_video(self):
        if "youtube.com" in self.url:
            return True
        else:
            return False

    def _add_youtube_video(self):
        self.youtube = YouTube(self.url)
        x = root.winfo_x() + 100
        y = root.winfo_y() + 100
        select_window = Toplevel(root)
        select_window.geometry("400x300+{}+{}".format(x, y))
        select_window.resizable(False, False)
        self._add_frames(select_window, self.youtube)
        show()
        ent.delete(0, "end")

    def _add_other_files(self):
        size = get_file_size(self.url)
        if size:
            filename = asksaveasfile(initialfile=get_file_name(self.url))
            if not filename:
                return
            db.insert_record("*", self.url, filename.name, size, self.url)
            show()
            ent.delete(0, "end")
        else:
            messagebox.showinfo(message="File can't be downloaded")

    def _add_frames(self, sw, yt):
        f1 = Frame(sw)
        f1.pack()
        Label(f1, text=yt.title).grid(row=0, column=0)

        f2 = Frame(sw)
        f2.pack()

        self.sub_tree = Treeview(f2)
        self.sub_tree.pack(pady=(10, 0))
        self.sub_tree["columns"] = ("Quality", "Size", "Type")
        self.sub_tree.column("#0", width=0, minwidth=0)
        self.sub_tree.column("Quality", width=70, anchor=CENTER)
        self.sub_tree.column("Size", width=70, anchor=CENTER)
        self.sub_tree.column("Type", width=70, anchor=CENTER)

        self.sub_tree.heading("#0", text="No")
        self.sub_tree.heading("Quality", text="Quality")
        self.sub_tree.heading("Size", text="Size")
        self.sub_tree.heading("Type", text="Type")

        self.sub_tree.bind("<Button-1>", self._set_selection)

        formats = yt.formats

        for i in range(len(formats)):
            if formats[i]["resolution"]:
                self.sub_tree.insert(parent="", index="end", iid=i, text="Parent", values=(
                formats[i]["resolution"], file_size_string(formats[i]["contentLength"]), "Video"))
            else:
                self.sub_tree.insert(parent="", index="end", iid=i, text="Parent",
                                     values=(formats[i]["abr"], file_size_string(formats[i]["contentLength"]), "Audio"))
        self.sub_tree.selection_set(0)

        f3 = Frame(sw)
        f3.pack()
        b = Button(f3, text="Download", command=self._add_youtube_video_to_list)
        b.grid(row=0, column=0)

    def _set_selection(self, event):
        item = self.sub_tree.identify("item", event.x, event.y)
        self.sub_tree.selection_remove(self.sub_tree.selection()[0])
        self.sub_tree.selection_set(item)

    def _add_youtube_video_to_list(self):
        record = {}
        rsl = self.sub_tree.item(self.sub_tree.selection()[0])["values"][0]
        for i in self.youtube.formats:
            if i["resolution"] == rsl or i["abr"] == rsl:
                record = i
                break
        filename = asksaveasfile(initialfile=self.youtube.title + ".mp4")
        db.insert_record(self.youtube.title + ".mp4", self.url, filename.name, record["contentLength"], record["url"])


class DownloadFile:
    def __init__(self, u):
        self.url = u
        db.update_status(self.url, "downloading")
        data = db.get_records(self.url)  # get the records of the file from database
        self.name = data[1]  # name of the file
        self.path = data[3]  # path to save file
        self.size = data[4]  # size of the file
        self.downloaded = data[5]  # downloaded size of the file, default 0
        self.status = data[6]  # status of the file
        self.table_row = self._table_row()

    def download_file(self):
        self._update_size_and_url()  # update url and filename to gui
        self._update_status()  # update status to gui, database and list
        self._update_progress()  # update progress bar to gui
        self._download_file()  # function to download file

    def _download_file(self):
        global PAUSE_BUTTON_CLICKED

        headers = {"Range": "bytes={}-{}".format(self.downloaded, self.size)}
        req = requests.get(self.url, headers=headers, stream=True)
        chunk_get, t = 0, time.time()

        for chunk in req.iter_content(chunk_size=102400):
            chunk_get += len(chunk)
            self.downloaded += len(chunk)
            self._update_downloaded()  # update downloaded size to gui & database
            self._write_file(chunk)  # write stream to file
            if time.time() - t > 0.25:
                self._update_speed(chunk_get, time.time() - t)  # update speed to gui
                self._update_progress()  # update progress to gui and tree-view
                chunk_get, t = 0, time.time()
            if PAUSE_BUTTON_CLICKED:
                db.update_record(self.downloaded, "paused", self.url)
                label_status.config(text="paused")
                show()
                PAUSE_BUTTON_CLICKED = False
                return
        self._complete()
        show()

    def _write_file(self, chunk):
        f = open(self.path, "ab")
        f.write(chunk)
        f.close()

    def _update_size_and_url(self):
        label_url.config(text=get_shorted_url(db.get_the_url(self.url)))
        label_size.config(text=file_size_string(self.size))

    def _update_status(self):
        label_status.config(text=self.status)
        db.update_record(self.downloaded, "downloading", self.url)
        show()

    def _update_downloaded(self):
        db.update_record(self.downloaded, self.status, self.url)  # update downloaded size to database
        label_downloaded.config(text=downloaded_size(self.downloaded, self.size))  # update downloaded size to gui

    def _update_progress(self):
        percent = (self.downloaded / self.size) * 100
        progress["value"] = percent
        print(self.table_row)
        tree.set(self.table_row, "#3", str(round(percent, 2)) + " %")

    @staticmethod
    def _update_speed(chunk_size, t):
        label_speed.config(text=download_speed(chunk_size, t))

    def _complete(self):
        db.update_record(self.downloaded, "completed", db.get_the_url(self.url))
        self._update_progress()
        label_speed.config(text="-")
        label_status.config(text="completed")

    def _table_row(self):
        items = tree.get_children()
        for item in items:
            data = tree.item(item)["values"]
            if data[4] == db.get_the_url(self.url):
                return item


def add_to_download():
    AddToList(url.get())


def show():
    tree.delete(*tree.get_children())
    data = list(db.all_records())
    data.reverse()
    i = 0
    while i < len(data):
        x = data[i]
        tree.insert(parent="", index="end", iid=i, text="Parent", values=(
        get_file_name(x[1]), file_size_string(x[4]), str(round((x[5] / x[4]) * 100, 2)) + " %", x[6], x[2]))
        i += 1


def double_click(event):
    x = root.winfo_x() + 100
    y = root.winfo_y() + 100
    info_window = Toplevel(root)
    info_window.geometry("400x300+{}+{}".format(x, y))
    info_window.title("Task information")


########################## END OF DOWNLOAD FUNCTIONS #######################
############################################################################


def pause_download(u):
    global PAUSE_BUTTON_CLICKED
    PAUSE_BUTTON_CLICKED = True
    db.update_status(u, "paused")


def resume_download(u):
    global PAUSE_BUTTON_CLICKED
    PAUSE_BUTTON_CLICKED = True
    db.update_to_pending()
    db.update_status(u, "downloading")
    PAUSE_BUTTON_CLICKED = False
    show()


def remove_download(u):
    con = messagebox.askyesno(message="Are you sure want to remove this item?")
    if con:
        db.remove_record(u)
    show()


def show_menu(e):
    item = tree.identify('item', e.x, e.y)
    if item:
        tree.selection_set(item)
        values = e.widget.item(item)["values"]
        menu.delete(0, END)
        if values[3] == "downloading":
            menu.add_command(label="Pause", command=lambda f=values[4]: pause_download(f))
            menu.add_command(label="Remove", command=lambda f=values[4]: remove_download(f))
        if values[3] == "pending":
            menu.add_command(label="Download", command=lambda f=values[4]: pause_download(f))
            menu.add_command(label="Remove", command=lambda f=values[4]: remove_download(f))
        if values[3] == "completed":
            menu.add_command(label="Remove", command=lambda f=values[4]: remove_download(f))
        if values[3] == "paused":
            menu.add_command(label="Resume", command=lambda f=values[4]: resume_download(f))
            menu.add_command(label="Remove", command=lambda f=values[4]: remove_download(f))
    menu.tk_popup(e.x_root, e.y_root)


def download_thread():
    while True:
        data = db.all_records()
        data.reverse()
        for i in data:
            if i[6] == "downloading":
                d = DownloadFile(i[-1])
                d.download_file()
        for i in data:
            if i[6] == "pending":
                d = DownloadFile(i[-1])
                d.download_file()
        time.sleep(5)


def start_download():
    th = Thread(target=download_thread)
    th.start()


############################################################################
################################ GUI PART ##################################
root = Tk()
root.geometry("600x500")
root.resizable(False, False)
root.title("Download Manager")

url = StringVar()

label_frame1 = LabelFrame(root, text="Download status")
label_frame1.pack(fill="both", expand="no", padx=10, pady=10)
label_frame2 = LabelFrame(root, text="Download list")
label_frame2.pack(fill="both", expand="yes", padx=10, pady=10)

##################################################################
################ label frame 1 ( download status ) ###############
##################################################################
frame1_label1 = Frame(label_frame1)
frame1_label1.pack(fill="x")
label_url = Label(frame1_label1, text="-")
label_url.grid(row=0, padx=5, pady=(5, 0), column=0, sticky=W)
###################################################################
frame2_label1 = Frame(label_frame1)
frame2_label1.pack(fill="x")
Label(frame2_label1, text="File size").grid(row=1, column=0, padx=5, sticky=W)
Label(frame2_label1, text="Downloaded").grid(row=2, column=0, padx=5, sticky=W)
Label(frame2_label1, text="Transfer rate").grid(row=3, column=0, padx=5, sticky=W)
Label(frame2_label1, text="Status").grid(row=4, column=0, padx=5, pady=(0, 5), sticky=W)

label_size = Label(frame2_label1, text="-")
label_size.grid(row=1, column=1, padx=(20, 0), sticky=W)
label_downloaded = Label(frame2_label1, text="-")
label_downloaded.grid(row=2, column=1, padx=(20, 0), sticky=W)
label_speed = Label(frame2_label1, text="-")
label_speed.grid(row=3, column=1, padx=(20, 0), sticky=W)
label_status = Label(frame2_label1, text="-", fg="blue")
label_status.grid(row=4, column=1, padx=(20, 0), pady=(0, 5), sticky=W)
label_value = Label(frame2_label1, text=None)
####################################################################
frame3_label1 = Frame(label_frame1)
frame3_label1.pack(fill="x")
progress = Progressbar(frame3_label1, orient=HORIZONTAL, length=565)
progress.grid(row=0, padx=(5, 0), pady=(0, 5))

###############################################################################
###########################  download list ####################################
###############################################################################
frame1_label2 = Frame(label_frame2)
frame1_label2.pack(fill="x")
frame2_label2 = Frame(label_frame2)
frame2_label2.pack(fill="x")
###############################################################################
ent = Entry(frame1_label2, textvariable=url, width=81)
ent.grid(row=0, column=0, padx=5, pady=10)
btn = Button(frame1_label2, text="Download", activebackground="#fff", command=add_to_download)
btn.grid(row=0, column=1, padx=5, pady=10)

#####################  ADD SCROLLBARS TO TABLE  ####################################
vertical_scrollbar = Scrollbar(frame2_label2)
vertical_scrollbar.pack(side=RIGHT, fill=Y)
horizontal_scrollbar = Scrollbar(frame2_label2, orient=HORIZONTAL)
horizontal_scrollbar.pack(side=BOTTOM, fill=X)

##########################  ADD MENU TO TABLE ################################
menu = Menu(frame2_label2, tearoff=False)

tree = Treeview(frame2_label2, xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)
vertical_scrollbar.config(command=tree.yview)
horizontal_scrollbar.config(command=tree.xview)

tree.pack(padx=(5, 0))
tree["columns"] = ("Name", "Size", "Process", "Status", "URL")
tree.bind("<Double-1>", double_click)
tree.bind("<Button-3>", show_menu)

tree.column("#0", width=0, minwidth=0)
tree.column("Name", width=250)
tree.column("Size", width=70, anchor=CENTER)
tree.column("Process", width=70, anchor=CENTER)
tree.column("Status", width=90, anchor=CENTER)
tree.column("URL", width=600)

tree.heading("#0", text="No")
tree.heading("Name", text="Name")
tree.heading("Size", text="Size", anchor=CENTER)
tree.heading("Process", text="Process", anchor=CENTER)
tree.heading("Status", text="Status")
tree.heading("URL", text="URL")
############################# END OF GUI PART ##############################
############################################################################


if __name__ == '__main__':
    db = DatabaseManagement()
    db.repair_download()
    show()
    start_download()
    root.mainloop()

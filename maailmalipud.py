import tkinter as tk # tkinter UI jaoks
import random # random
from PIL import Image, ImageTk # piltide jaoks vajalik pillow
from riigid import riigid # riikide nimekiri

root = tk.Tk() # aken
root.title('Maailma lipud') # akna nimi
root.geometry('700x500') # akna suurus

seaded_fr = tk.Frame(root) # seaded frame
mang_fr = tk.Frame(root) # mang frame
fakt_fr = tk.Frame(root) # fakt frame

seaded_fr.place(relwidth=1, relheight=1)
mang_fr.place(relwidth=1, relheight=1)
fakt_fr.place(relwidth=1, relheight=1)

# UUE PILDI LOOMINE
def show_frame(frame):
    frame.tkraise()

#----------
# SEADED_FR
#----------

# SEADED
raundid_var = tk.IntVar(value=5)
taimer_var = tk.IntVar(value=15)
piirkond_var = tk.StringVar(value='Maailm')

# PEALKIRI
pealkiri_label = tk.Label(seaded_fr, text='Seaded', font=('Arial', 25))
pealkiri_label.pack(pady=55)

# PIIRKOND
piirkond_frame = tk.Frame(seaded_fr)
piirkond_frame.pack(pady=10)

tk.Label(piirkond_frame, text='Piirkond:').pack(side='left', padx=5)

piirkond_menu = tk.OptionMenu(
    piirkond_frame,
    piirkond_var,
    'Maailm', 'Euroopa', 'Aasia', 'Aafrika', 'Põhja-Ameerika', 'Lõuna-Ameerika', 'Austraalia ja Okeaania'
)
piirkond_menu.pack(side='left')

# RAUNDID
raundid_frame = tk.Frame(seaded_fr)
raundid_frame.pack(pady=10)

tk.Label(raundid_frame, text='Raundide arv:').pack(side='left', padx=5)

raundid_menu = tk.OptionMenu(
    raundid_frame,
    raundid_var,
    5, 10
)
raundid_menu.pack(side='left')

# TAIMER
taimer_frame = tk.Frame(seaded_fr)
taimer_frame.pack(pady=10)

tk.Label(taimer_frame, text='Taimer (sekundit):').pack(side='left', padx=5)

taimer_menu = tk.OptionMenu(
    taimer_frame,
    taimer_var,
    5, 15, 30
)
taimer_menu.pack(side='left')

#-------------------------------
# FUNKTSIOONID RANDOM LIPU JAOKS
#-------------------------------

# LIPU VALIMINE
def random_riik():
    valitud_piirkond = piirkond_var.get()

    if valitud_piirkond == 'Maailm':
        sobivad_riigid = list(riigid.keys())
    else:
        sobivad_riigid = [
            riik
            for riik, andmed in riigid.items()
            if andmed['piirkond'] == valitud_piirkond
        ]

    return random.choice(sobivad_riigid)

# LIPU NAITAMINE
def naita_lipp(riik):
    lipp_file = riigid[riik]['lipp']

    img = Image.open(lipp_file)

    korgus = 180

    ratio = img.width / img.height
    laius = int(korgus * ratio)

    img = img.resize((laius, korgus), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    flag_label.config(image=photo)
    flag_label.image = photo

flag_label = tk.Label(mang_fr)
flag_label.pack(pady=40)

# ALUSTA
def alusta_mang():
    print('Piirkond:', piirkond_var.get())
    print('Raundid:', raundid_var.get())
    print('Taimer:', taimer_var.get())
    riik = random_riik()
    naita_lipp(riik)
    show_frame(mang_fr)

alusta_nupp = tk.Button(seaded_fr, text='Alusta', command=alusta_mang)
alusta_nupp.pack(pady=50)

root.bind('<Return>', lambda event: alusta_mang())

#--------
# MANG_FR
#--------

show_frame(seaded_fr)
root.mainloop()
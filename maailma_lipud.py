import tkinter as tk # tkinter UI jaoks
import random # random
from PIL import Image, ImageTk # piltide jaoks vajalik pillow
from riigid import riigid # riikide nimekiri

root = tk.Tk() # aken
root.title('Maailma lipud') # akna nimi
root.geometry('700x500') # akna suurus

# seaded, mang, fakt, lopp
seaded_fr = tk.Frame(root)
mang_fr = tk.Frame(root)
fakt_fr = tk.Frame(root)
lopp_fr = tk.Frame(root)

# frame suurused
seaded_fr.place(relwidth=1, relheight=1)
mang_fr.place(relwidth=1, relheight=1)
fakt_fr.place(relwidth=1, relheight=1)
lopp_fr.place(relwidth=1, relheight=1)

# UUE PILDI LOOMINE
def show_frame(frame):
    frame.tkraise()

#----------
# SEADED_FR
#----------

# SEADED
raundid_var = tk.IntVar(value=5)
piirkond_var = tk.StringVar(value='Maailm')

# PEALKIRI
pealkiri_label = tk.Label(seaded_fr, text='Seaded', font=('Arial', 20))
pealkiri_label.pack(pady=70)

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

praegune_raund = 0
max_raundid = 0
tulemus = 0

kasutamata_riigid = []

raundi_label = tk.Label(
    mang_fr,
    text='',
    font=('Arial', 12)
)
raundi_label.pack(pady=(10, 0))

# LIPU NAITAMINE

# ekraanile ilmub pillow abil lipp
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

# KONTROLLI VASTUS

# kontrollib kas vastus oli õige ning avab fakt_fr
def kontrolli_vastus(valik, oige):
    global tulemus
    
    if valik == oige:
        tulemus_label.config(
            text='Õige!',
            fg="#00A000"
        )
        oige_vastus_label.config(
            text=f'Vastus oli: {oige}'
        )
        tulemus += 1
    else:
        tulemus_label.config(
            text='Vale...',
            fg='#E00000'
        )

    fakt_pealkiri_label.config(
        text=f'Huvitav fakt riigi {oige} kohta:'
    )
    oige_vastus_label.config(
            text=f'Vastus oli: {oige}'
        )

    fakt_label.config(
        text=riigid[oige]['fakt']
    )

    show_frame(fakt_fr)

# ALUSTA MÄNG

# loob mängu alustamise funktsiooni ning sisaldab kõike vajalikku (raundide loendamine, mang_fr ilmumine, ...)
def alusta_mang():
    global praegune_raund, max_raundid, kasutamata_riigid

    if praegune_raund == 0:
        max_raundid = raundid_var.get()

        piirkond = piirkond_var.get()
        kasutamata_riigid = riigid_piirkonnas(piirkond)
        random.shuffle(kasutamata_riigid)

    if praegune_raund >= max_raundid:
        naita_lopp_ekraan()
        praegune_raund = 0
        return

    praegune_raund += 1

    raundi_label.config(
    text=f'Raund {praegune_raund} / {max_raundid}'
    )

    tulemus_label.config(text='')
    oige_vastus_label.config(text='')
    fakt_pealkiri_label.config(text='')
    fakt_label.config(text='')

    piirkond = piirkond_var.get()

    oige_riik = kasutamata_riigid.pop()
    naita_lipp(oige_riik)

    sobivad_riigid = riigid_piirkonnas(piirkond)
    sobivad_riigid.remove(oige_riik)

    valed_riigid = random.sample(sobivad_riigid, 2)

    vastused = [oige_riik] + valed_riigid
    random.shuffle(vastused)

    for btn, riik in zip(vastuse_nupud, vastused):
        btn.config(
            text=riik,
            command=lambda r=riik: kontrolli_vastus(r, oige_riik)
        )

    show_frame(mang_fr)

alusta_nupp = tk.Button(seaded_fr, text='Alusta', command=alusta_mang)
alusta_nupp.pack(pady=50)

#--------
# MANG_FR
#--------

vastuse_nupud = []

# ilmuvad 3 vastusevarianti nuppudena
for i in range(3):
    btn = tk.Button(
        mang_fr,
        text='',
        font=('Arial', 13),
        width=30
    )
    btn.pack(pady=5)
    vastuse_nupud.append(btn)

# vajalik selleks et kõik vastusevariandid oleks valitud maailmajaost
def riigid_piirkonnas(piirkond):
    if piirkond == 'Maailm':
        return list(riigid.keys())
    return [
        riik
        for riik, andmed in riigid.items()
        if andmed['piirkond'] == piirkond
    ]

#--------
# FAKT_FR
#--------

# kas oli õige või vale
tulemus_label = tk.Label(
    fakt_fr,
    text='',
    font=('Arial', 22, 'bold')
)
tulemus_label.pack(pady=(50, 0))

# õige vastus
oige_vastus_label = tk.Label(
    fakt_fr,
    text='',
    font=('Arial', 14)
)
oige_vastus_label.pack(pady=(50, 0))

# peale seda ilmub fakt
fakt_pealkiri_label = tk.Label(
    fakt_fr,
    text='',
    font=('Arial', 12),
    fg="#676767"
)
fakt_pealkiri_label.pack(pady=(50, 0))

# huvitav fakt riigi kohta
fakt_label = tk.Label(
    fakt_fr,
    text='',
    font=('Arial', 12),
    wraplength=500,
    justify='center'
)
fakt_label.pack(pady=(10, 20))

# nupp millele vajutades ilmub uus raund
jargmine_nupp = tk.Button(
    fakt_fr,
    text='Järgmine',
    font=('Arial', 14),
    command=lambda: alusta_mang()
)
jargmine_nupp.pack(pady=30)

#--------
# LOPP_FR
#--------

# pealkiri
lopp_pealkiri_label = tk.Label(
    lopp_fr,
    text='Mäng läbi!',
    font=('Arial', 24, 'bold')
)
lopp_pealkiri_label.pack(pady=(80, 20))

# tulemus
lopp_tulemus_label = tk.Label(
    lopp_fr,
    text='',
    font=('Arial', 18)
)
lopp_tulemus_label.pack(pady=20)

# nupud
nupud_frame = tk.Frame(lopp_fr)
nupud_frame.pack(pady=40)

mangi_uuesti_nupp = tk.Button(
    nupud_frame,
    text='Mängi uuesti',
    font=('Arial', 14),
    width=15,
    command=lambda: mangi_uuesti()
)
mangi_uuesti_nupp.pack(side='left', padx=10)

ava_seaded_nupp = tk.Button(
    nupud_frame,
    text='Ava seaded',
    font=('Arial', 14),
    width=15,
    command=lambda: seadetesse()
)
ava_seaded_nupp.pack(side='left', padx=10)

# funktsioonid lopu ekraani jaoks
def mangi_uuesti():
    global praegune_raund, tulemus
    
    praegune_raund = 0
    tulemus = 0
    alusta_mang()

def seadetesse():
    global praegune_raund, tulemus
    
    praegune_raund = 0
    tulemus = 0
    show_frame(seaded_fr)

def naita_lopp_ekraan():
    lopp_tulemus_label.config(
        text=f'Sinu tulemus: {tulemus}/{max_raundid}'
    )
    show_frame(lopp_fr)

# vajalik akna ilmumiseks
show_frame(seaded_fr)
root.mainloop()
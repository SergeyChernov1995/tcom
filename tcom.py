# ----------------------------------------------------------------------------
# The Colour of Money
# Based on the short-lived British game show
# Copyright © 2025 Sergey Chernov aka Gamer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from enum import Enum
from tkinter import messagebox as mb
from random import randint, uniform, randrange, shuffle
from heapq import nlargest
import codecs
root=tk.Tk()
root.geometry("1200x900")
root.resizable(width=False, height=False)
root.title('Добро пожаловать на игру "Цвет денег"!')
aim = 0
canvas = tk.Canvas(root, width=900, height=710, bg='#dfdfdf')
cash_machines = []
chosen_atm = 0


class stadija(Enum):
    pre_game = 0
    pre_choosing = 1
    bonggame = 2
    after_stop = 3
    bong = 4
    bankomat_chosen = 5

class bongstage(Enum):
    before = 0
    inprogress = 1
    stopped = 2
    finish = 3
    after = 4


bong = bongstage.before
etap = stadija.pre_game
b_g_thisvar = []
b_g_count = 0
def doSomething():
    if tk.messagebox.askyesno("Exit", "Do you want to quit the application?"):
        log.close()
        root.destroy()

def dummy():
    global spalvos
    bablo['text'] = '0'
    bongsum.place_forget()
    canvas.delete("case" + str(chosen_atm))
    spalvos[chosen_atm]['in_game'] = False
    sums_on_tableau[nat_order.index(spalvos[chosen_atm]['money'])]['bg'] = "#ff0000"
    sums.remove(spalvos[chosen_atm]['money'])
    #spalvos = [x for x in spalvos if x['in_game']]
    root.statistics = root.after(2000, after_atm)



def stop():
    global b_g_count, b_g_thisvar, money_won, bong, spalvos
    root.after_cancel(root.step)
    stop_game['state'] = 'disabled'
    money_won += b_g_thisvar[b_g_count]
    mb.showinfo("Пополнение счёта!", "Вы взяли из этого банкомата "+str(b_g_thisvar[b_g_count]))
    mb.showinfo("Сколько вы могли бы унести?", "А всего в банкомате было "+str(spalvos[chosen_atm]['money']))
    if (b_g_thisvar[b_g_count]) == spalvos[chosen_atm]['money']:
        log.write("Игрок опустошил этот банкомат, выиграв все "+str(spalvos[chosen_atm]['money'])+'\n')
    else:
        log.write("Игрок унёс "+str(b_g_thisvar[b_g_count])+ " из возможных "+str(spalvos[chosen_atm]['money'])+'\n')
    dummy()


def after_atm():
    root.after_cancel(root.statistics)
    n = 10-sum(1 for i in range(len(spalvos)) if spalvos[i]['in_game'] is False)
    if (n>0):
        k = sum(nlargest(n, sums))
        #print("n="+str(n)+', k='+str(k))
    if (money_won >= aim):
        mb.showinfo("Победа!", "Вы достигли своей цели в "+str(aim)+'!')
        log.write("Игрок достиг своей цели!" + '\n' +"Выигрыш: "+str(aim)+'\n')
        log.close()
        root.destroy()
    elif (n == 0):
        mb.showinfo("Поражение", "Вы не набрали достаточно денег")
        log.write("Игрок проигрывает, не сумев набрать целевую сумму" + '\n')
        log.close()
        root.destroy()
    elif (aim-money_won) > k:
        mb.showinfo("Поражение", "Вы уже не сможете набрать достаточно денег")
        log.write("Игрок терпит досрочное поражение, теряя возможномть набрать целевую сумму"+'\n')
        log.close()
        root.destroy()
    else:
        root.title ('Банкоматов осталось: '+str(n)+'. Вы набрали '+str(money_won)+'. Осталось набрать '+str(aim-money_won))
        canvas['bg'] = '#dfdfdf'
        for i in range(len(spalvos)):
            canvas.itemconfigure("case" + str(i), state='normal')



def higher():
    global b_g_count, b_g_thisvar, spalvos
    root.after_cancel(root.step)
    b_g_count +=1
    if (b_g_count>0) and (b_g_count<len(b_g_thisvar)):
        stop_game['state'] = 'normal'
        bablo['text'] = str(b_g_thisvar[b_g_count])
        root.step = root.after(1750, higher)
    elif (b_g_count>=len(b_g_thisvar)):
        stop_game['state'] = 'disabled'
        bablo['text'] ='X'
        mb.showwarning("X", "Вы не смогли взять деньги из этого банкомата!")
        log.write('Игрок не смог ничего получить из банкомата, а мог бы выиграть ' + str(spalvos[chosen_atm]['money']) + '\n')
        dummy()




def start_atm():
    global  b_g_thisvar, b_g_count
    b_g_count = 0
    bablo.place(relx=0, rely=0)
    bablo['text'] = str(b_g_thisvar[b_g_count])
    start_bng.place_forget()
    stop_game.place(relx=0.6, rely=0)
    stop_game['state'] = 'disabled'
    root.step = root.after(1750, higher)



def place(event, l):
    global etap, b_g_thisvar, chosen_atm
    etap = stadija.bankomat_chosen
    root.title((spalvos[l]['name']+'***')*6)
    canvas['bg'] = spalvos[l]['color']
    chosen_atm = l
    rt = sum(1 for i in range(len(spalvos)) if spalvos[i]['in_game'] is False)+1
    log.write ('Банкомат №'+str(rt)+' - '+spalvos[l]['name']+'\n')
    for i in range(len(spalvos)):
        canvas.itemconfigure("case" + str(i), state='hidden')
    bongsum.place(relx=0.45, rely=0.8)
    start_bng.place(relx=0.6, rely=0)
    b_g_thisvar = list(range(0, spalvos[l]['money']+1000, 1000))










def zaidimo_pradzia(q):
    global etap
    global aim
    start.place_forget()
    mb.showinfo("Мы готовы!", "Ваша целевая сумма - "+str(q))
    aim = q
    log.write('Целевая сумма: '+(str(aim)+'\n'))
    pinigai.place(x=930, y=10)
    canvas.place(x=5, y=5)
    h_w = [125, 97]
    #v = 10+h_w[0]*(cases_pos_x[i]-1.8)
    #v1 = 10+h_w[1]*(cases_pos_y[i]-1)
    for b in range(20):
        p = tk.Label(pinigai, width=10, height=1)
        sums_on_tableau.append(p)
        sums_on_tableau[b]['bg'] = "#afafaf"
        sums_on_tableau[b]['fg'] = "#000000"
        sums_on_tableau[b]["text"] = str(nat_order[b])
        sums_on_tableau[b]["justify"] = tk.CENTER
        c = 10
        sums_on_tableau[b].place(x=15 + 105 * (b // c), y=15 + 35 * (b % c))
        dict = {}
        dict["name"] = COLORS[b][0]
        dict["color"] = COLORS[b][1]
        dict["money"] = sums[b]
        dict["in_game"] = True
        spalvos.append(dict)
        v = 180 * (b % 5) + 30
        v1 = 170 * (b // 5)+25
        f = canvas.create_rectangle(v, v1, v+h_w[0], v1+h_w[1], fill=spalvos[b]['color'], outline = "#222222", tag = "case"+str(b))
        cash_machines.append(f)
        x, y, x1, y1 = canvas.coords(cash_machines[b])
        g = canvas.create_text((x + x1) // 2, (y + y1) // 2, text=spalvos[b]['name'], font=('Arial', 12), tag="case" + str(b))
        #nomera.append(g)
        canvas.tag_bind("case" + str(b), "<Button-1>", lambda event, h=b: place(event, h))
        etap = stadija.pre_choosing
        #print(spalvos[b])




def chosen():
    global aim
    aim = magram
    scal.place_forget()
    accept.place_forget()
    random_sum.place_forget()
    zaidimo_pradzia(aim)

def pick_random():
    global aim
    aim = randrange(50000, 101000, 1000)
    scal.place_forget()
    accept.place_forget()
    random_sum.place_forget()
    zaidimo_pradzia(aim)

def editvalue(event):
    global magram
    magram = val.get()
    #print(magram)


val = tk.IntVar(value=50000)
magram = val.get()
scal = tk.Scale(root,orient='horizontal',length=400,from_=50000,to=100000,resolution=1000, variable=val)
                #command=editvalue())
scal.place(relx=0.4, rely=0.2)
scal.bind("<ButtonRelease-1>", editvalue)
start = tk.Label(root, text="Выберите целевую сумму")
start.place(relx=0.4, rely=0.05)
random_sum = tk.Button(root, text='Случайная сумма', command=pick_random)
accept = tk.Button(root, text='Выбрать сумму', command=chosen)
random_sum.place(relx=0.3, rely=0.4)
accept.place(relx=0.46, rely=0.4)
pinigai = ttk.LabelFrame(root, text = "Суммы в игре", width = 215, height=420)
bongsum = ttk.LabelFrame(root, text = "", width = 200, height=70)
sums = list(range(1000, 21000, 1000))
nat_order = sums.copy()
random.shuffle(sums)
sums_on_tableau = []
COLORS = [["КРАСНЫЙ", "#FF0000"], ["РОЗОВЫЙ", "#FFC0CB"], ["ОРАНЖЕВЫЙ", "#FFA500"], ["ЖЁЛТЫЙ", "#FFFF00"], ["ХАКИ", "#F0E68C"],
          ["ЛАВАНДОВЫЙ", "#E6E6FA"], ["ФИОЛЕТОВЫЙ", "#EE82EE"], ["ЗЕЛЁНЫЙ", "#00FF7F"], ["ОЛИВКОВЫЙ", "#808000"], ["ГОЛУБОЙ", "#00FFFF"],
          ["СИНИЙ", "#0000FF"], ["ИНДИГО", "#4B0082"], ["КОРИЧНЕВЫЙ", "#A52A2A"], ["БЕЖЕВЫЙ", "#F5F5DC"], ["СЕРЕБРЯНЫЙ", "#C0C0C0"],
          ["ФУКСИЯ", "#FF00FF"], ["ЛОСОСЕВЫЙ", "#FA8072"], ["АКВАМАРИН", "#7FFFD4"], ["ШОКОЛАДНЫЙ", "#D2691E"], ["ЖЁЛТО-ЗЕЛЁНЫЙ", "#9ACD32"]]
random.shuffle(COLORS)
spalvos = []
money_won = 0
stop_game = tk.Button(bongsum, text = 'СТОП!', command=stop)
start_bng = tk.Button(bongsum, text = 'СТАРТ', command=start_atm)
bablo = tk.Label(bongsum, text = '')
log = codecs.open('log.txt', 'a', "utf_8_sig")







root.protocol('WM_DELETE_WINDOW', doSomething)
root.mainloop()

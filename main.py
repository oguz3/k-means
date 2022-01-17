from cProfile import label
import warnings
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from functools import partial
from file import readFile, writeFile
from func import calculateCentroid, euclideanDistance, randomCentroid, randomColor

warnings.simplefilter(action='ignore', category=FutureWarning)

#Ibrahim Oguzhan Ulukaya
#2018280072
#https://github.com/oguz3

k = 2
cluster = {}
center = []
newCenter = []
step = 1

data = readFile()
#column name ayıklamak için
rowName =  data.pop(0)

def k_means(n1):
    global k
    global cluster
    global center
    global newCenter
    global step
    k = int(n1.get())
    while(1):
        # ilk giriş için random center atanır ve cluster'a eklenir.
        if step == 1:
            i = 0
            while i < k:
                randomItem = randomCentroid(data, len(data) - 1)
                isExist = randomItem in center
                if isExist:
                    i = i - 1
                else:
                    center.insert(i, randomItem)
                    cluster[i] = [center[i]];
                i += 1
        #bütün elemanlara bakıp yakın olduğu kümeye atama
        for element in data:
            distance = [];
            for index in range(0, len(center)):
                distance.insert(index, euclideanDistance(element, center[index]))
            smallIndex = 0;
            for index1 in range(0, len(distance)):
                if distance[index1] < distance[smallIndex]:
                    smallIndex = index1
            
            for property in cluster:
                for index2 in range(0, len(cluster[property])):
                    if np.array_equal(cluster[property][index2], element):
                        cluster[property].remove(element)
                        break
            
            isExist = element in cluster[smallIndex]
            if isExist == False:
                cluster[smallIndex].append(element);

        # yeni center bulma.
        newCenter = []
        for idx in range(0, len(center)):
            newC = calculateCentroid(cluster[idx])
            if len(center) == len(newCenter):
                newCenter[idx] = newC
            else:
                newCenter.insert(idx, newC)
        # # yeni center eski center'a eşit mi kontrol
        if np.array_equal(newCenter, center):
            center = newCenter
            break
        else:
            center = newCenter
            step += 1

    writeFile(data, cluster)

#genel noktaları ciz
def draw(select_x, select_y):
    global rowName
    xIndex = rowName.index(select_x.get())
    yIndex = rowName.index(select_y.get())
    for idx, property in enumerate(cluster):
        x = []
        y = []
        for item in cluster[property]:
            for index in range(0, len(item)):
                if index == xIndex:
                    x.append(int(item[index]))
                elif index == yIndex:
                    y.append(int(item[index]))
        plt.scatter(x, y, color = randomColor(), label="cluster " + str(idx))
    #center noktaları
    for item in center:
        plt.scatter(item[xIndex], item[yIndex], s=40, marker="X", color = "red", label="center")
    plt.xlabel(select_x.get())
    plt.ylabel(select_y.get())
    handles, labels = plt.gca().get_legend_handles_labels()
    labels, ids = np.unique(labels, return_index=True)
    handles = [handles[i] for i in ids]
    plt.legend(handles, labels, loc='best')
    plt.grid()
    plt.show()


def newWindowOpen():
    newWindow = tk.Toplevel(root)
    newWindow.title("Draw")
    newWindow.geometry("300x200")
    newWindow.config(padx=16, pady=16)
    select_x_varible = tk.StringVar(newWindow, value="Religious")
    select_y_varible = tk.StringVar(newWindow, value="Nature")


    tk.Label(newWindow, text="X ekseni için:").grid(row = 4, column = 0, pady = 2)
    selectbox_x = tk.OptionMenu(newWindow, select_x_varible, "Sports","Religious","Nature","Theatre","Shopping","Picnic").grid(row = 4, column = 1, pady = 2, sticky="ew")
    tk.Label(newWindow, text="Y ekseni için:").grid(row = 5, column = 0, pady = 2) 
    selectbox_y = tk.OptionMenu(newWindow, select_y_varible, "Sports","Religious","Nature","Theatre","Shopping","Picnic").grid(row = 5, column = 1, pady = 2, sticky="ew")
    call_draw = partial(draw, select_x_varible, select_y_varible)
    draw_btn = tk.Button(newWindow, text ="Draw", bg="blue",fg="white", command = call_draw).grid(row=7, column=1) 

root = tk.Tk()
root.geometry("300x250")
root.config(padx=16, pady=16)
number1 = tk.StringVar(root, value='2')

tk.Label(root, text="K değerini giriniz").grid(row = 0, column = 0, pady = 2)
entry_k = tk.Entry(root, textvariable=number1).grid(row = 0, column = 1, pady = 2)
call_k_means = partial(k_means, number1)  
run_btn = tk.Button(root, text ="Run", bg="green",fg="white", command = call_k_means).grid(row=2, column=0) 
new_window_btn = tk.Button(root, text ="Draw", bg="blue",fg="white", command = newWindowOpen).grid(row=2, column=1) 

root.mainloop()
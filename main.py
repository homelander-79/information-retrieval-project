from parsivar import Normalizer , Tokenizer , FindStems
import os
from os.path import exists
from timeit import default_timer

from tkinter import *
from tkinter.ttk import Labelframe
from tkinter import filedialog
import shutil
import pickle

list_stop_words = []
list_len_prefix = []
list_normal_prefix =[]
dict = {}

def stop_words():
    stop_words = open("file_project/stop.txt", encoding="utf8")
    stop_words.seek(0)
    for i in stop_words:
        list_stop_words.append(i.replace("\n", ""))

def normal_prefix():
    normal_prefix = open("file_project/normal_prefix.txt", encoding="utf8")
    for i in normal_prefix:
        list_len_prefix.append(len(i.replace("\n", "")))
        list_normal_prefix.append(i.replace("\n",""))

def elim():
    punc = open("file_project/elim.txt", encoding="utf8")
    result = []
    for i in punc.readlines():
       result.append( i.replace("\n",""))
    return result

def read_document():
    number_dic = os.listdir("document")
    n=len(number_dic)
    stop_words()
    normal_prefix()
    print(list_normal_prefix)
    for doc in range(0, n):
        tokeniz(doc)
    print(dict)

def tokeniz(doc):
    list_elim = elim()
    file = open(f"document/{doc}.txt", encoding="utf8")
    text = file.read()
    normal = Normalizer()
    my_tokenizer = Tokenizer()
    text_normal = normal.normalize(text)
    words = my_tokenizer.tokenize_words(text_normal)
    length = len(words)
    for i in range(0, length):
        if (words[i] in list_elim):
            words[i] = words[i].replace(words[i], "")
        else:
            for j in list_elim:
                if j in words[i]:
                    words[i] = words[i].replace(j, "")

    tokens_without_sw = [
        word.replace("\u200c", " ")
        for word in words
        if (not word in list_stop_words) and (word != "")
    ]


    my_stemmer = FindStems()
    tokens_without_prefix = [
       my_stemmer.convert_to_stem(word) for word in tokens_without_sw
    ]

    for word in tokens_without_prefix:
        if word in dict:
            if dict[word].count(doc) > 0:
                continue
            else:
                dict[word].append(doc)
        if word not in dict:
            dict[word] = [doc]

def AND(x, y):
    list1 = []
    i = 0
    j = 0
    while (i <= x.__len__() - 1) & (j <= y.__len__() - 1):
        if (x[i] == y[j]):
            list1.append(x[i])
            i += 1
            j += 1
        elif (x[i] < y[j]):
            i += 1
        else:
            j += 1
    return list1

def OR(x,y):
    list1=[]
    i=0
    j=0
    while (i<=x.__len__()-1) & (j<=y.__len__()-1) :
        if(x[i]==y[j]) :
            list1.append(x[i])
            i+=1
            j+=1
        elif (x[i]<y[j]):
            list1.append(x[i])
            i+=1
        else:
            list1.append(y[j])
            j+=1
    while (i<=x.__len__()-1):
        list1.append(x[i])
        i+=1
    while (j<=y.__len__()-1):
        list1.append(y[j])
        j+=1

    return list1

def gui_search(query):
    if (query.find("&") != -1):
        try:
            token1 = query[0:query.find("&") - 1]
            token2 = query[query.find("&") + 2:]
            list_id1 = dict[token1]
            list_id2 = dict[token2]
            return (AND(list_id1, list_id2))
        except:
            return("no result found")
    elif (query.find("|") != -1):
        try:
            token1 = query[0:query.find("|") - 1]
            token2 = query[query.find("|") + 2:]
            list_id1 = dict[token1]
            list_id2 = dict[token2]
            return(OR(list_id1, list_id2))
        except:
            return("no result found")
    else:
        try:
            return(dict[query])
        except:
            return("no result found")


if __name__ == '__main__':

    if(exists("file_project/tokeniz.pkl")==False):
         start = default_timer()
         read_document()
         end = default_timer()
         print(end - start)
         f = open("file_project/tokeniz.pkl", "wb")
         pickle.dump(dict, f)
         f.close()
    elif(exists("file_project/tokeniz.pkl")==True):
        f = open("file_project/tokeniz.pkl", "rb")
        dict=pickle.load(f)
        print(dict)
        f.close()


    root = Tk()

    # root.iconbitmap("gui.ico")
    root.title('search engine')
    root.geometry("700x600")

    def add_file():
        root.filename = filedialog.askopenfilename(initialdir="/", title="selecet a text file",
                                                   filetype=[("txt", ".txt"), ("all", ".*")])
        number_dic = os.listdir("document")
        n = len(number_dic)
        doc = shutil.copyfile(r'' + root.filename, r'document/' + str(n) + '.txt')
        tokeniz(n)
        print(dict)
        n += 1
        f = open("file_project/tokeniz.pkl", "wb")
        pickle.dump(dict, f)
        f.close()

    def search():
        v=my_entry.get()
        temp=[]
        for i in v:
            temp.append(i)
        for i in range(len(temp)):
            if temp[i] == "ي":
                temp[i]="ی"
        x="".join(temp)
        data = gui_search(x)
        temp.clear()
        my_entry.delete(0, END)
        result_text.delete(0.0, END)
        result_text.insert(0.0, data)


    def show_doc():
        v=docnum.get()
        text_file = open(r'document/' + str(v) + '.txt','r',encoding="utf8")
        top = Toplevel()
        top.geometry("500x450")
        file_text = Text(top, width=40, height=30)
        file_text.pack()
        file_text.insert(0.0, text_file.read())
        text_file.close()
        docnum.delete(0,END)

    search_frame = Labelframe(root, text="search in documents")
    search_frame.pack(pady=20)

    my_entry = Entry(search_frame, width=90)
    my_entry.pack(pady=20, padx=20)

    button_frame = Frame(root)
    button_frame.pack(pady=5)

    search_button = Button(button_frame, text="search", fg="#3a3a3a", command=search)
    search_button.grid(row=0, column=0, padx=5)

    add_button = Button(button_frame, text="add file", fg="#3a3a3a", command=add_file)
    add_button.grid(row=0, column=1)

    result_frame = Labelframe(root, text="result")
    result_frame.pack(pady=5)

    result_frame = Labelframe(root, text="result")
    result_frame.pack(pady=5)

    result_text = Text(result_frame, height=5, width=73)
    result_text.pack(pady=5)

    doc_search=Labelframe(root, text="doc search")
    doc_search.pack(pady=5)

    docnum = Entry(doc_search, width=90)
    docnum.pack(pady=20, padx=20)

    doc_button = Button(doc_search, text="open", fg="#3a3a3a", command=show_doc)
    doc_button.pack(pady=5)

    root.mainloop()
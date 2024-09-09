import tkinter as tk
import tkinter.ttk as ttk
import time
import random

class Table:
    def __init__(self, root, column_no, data, width_firstcol = 15, width_seccol = 15, scrollbar = False, header_text="", row_headers=[]):

        self.root = root
        self.data = data
        self.header_text = header_text
        self.row_headers = row_headers
        self.column_no = column_no
        self.scrollbar = scrollbar
        self.width_firstcol = width_firstcol
        self.width_seccol = width_seccol

        # Calculate total rows and columns from data
        self.total_rows = len(self.data)
        self.total_columns = len(self.data[0]) if self.total_rows > 0 else 0

        # Create the table layout
        self.create_table()

    # Create a table using grid geometry manager
    def create_table(self):
        
        self.frame = tk.Frame(self.root, bg="#f3f6f4")
        self.frame.grid(row = 1, column=self.column_no, padx=50, pady=50, sticky = "n")
        
        # Create a canvas to hold the table frame
        self.canvas = tk.Canvas(self.frame, bg="#f3f6f4",width=190, height=480)
        self.canvas.grid(row=1, column=0, sticky="nsew")

  
        # Create a frame to contain the table
        self.table_frame = tk.Frame(self.canvas, bg="#f3f6f4")
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Add scrollbar if enabled
        if self.scrollbar:
            self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
            self.scrollbar.grid(row=1, column=1, sticky="ns")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.h_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
            self.h_scrollbar.grid(row=1, column=0, sticky="s", columnspan = self.total_columns)
            self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Bind the canvas to the scrollbar
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create label for header text (if provided)
        if self.header_text:
            label = tk.Label(self.table_frame, text=self.header_text, font=("Courier", 14), bg = "#f3f6f4")
            label.grid(row=1, column=self.column_no, columnspan=self.total_columns, sticky = "w")

        # Create row headers (if provided)
        for i, row_header in enumerate(self.row_headers):
            if row_header:
                label = tk.Label(self.table_frame, text=row_header, width=10, anchor="w", bg = "#f3f6f4")  # Adjust width as needed
                label.grid(row=i+2, column=self.column_no, sticky="nsew", padx=5, pady=5)

        # Create table entries
        for i in range(self.total_rows):
            for j in range(self.total_columns):
                if j == 0:
                    entry = tk.Entry(self.table_frame, width=self.width_firstcol, fg='black', font=('Courier', 14))
                    entry.grid(row=i + 1 + (1 if self.header_text else 0), column=j+ self.column_no + (1 if self.row_headers else 0), padx = 5, pady = 5, sticky = "n")
                    entry.insert(tk.END, self.data[i][j])
                else:
                    #entry = tk.Entry(self.table_frame, width=self.width_seccol, fg='black', font=('Courier', 14))
                    entry = tk.Entry(self.table_frame, width=35, fg='black', font=('Courier', 14))
                    entry.grid(row=i + 1 + (1 if self.header_text else 0), column=j+ self.column_no + (1 if self.row_headers else 0), padx = 5, pady = 5, sticky = "n")
                    entry.insert(tk.END, self.data[i][j])            

# Create the root window
root = tk.Tk()
root.title("Cache mapping") 
root.config(bg = "#d9d2e9")

# Sample data with empty strings replaced with sample values
data_v1 = [["", ""] for i in range(4)]
data_l1 = [["", ""] for i in range(8)]
data_l2 = [["", ""] for i in range(16)]
data_mm = [[str(i) + " " + str(i + 1) + " " + str(i + 2) + " " + str(i + 3)] for i in range(0, 128, 4)]

text = tk.Text(root, height = 5, width = 30)
info = "Main Memory Size: 128B\nL1 Cache Size: 32B\nVictim Cache Size: 16B\nL2 Cache Size: 64B\nSize of each line: 4B"
text.grid(row = 0, column = 2, sticky = "n", columnspan = 2)
text.insert(tk.END, info)


root.geometry('2000x2000')

#SEGMENT 1: INITIALISATION OF CACHES

mainmm=[]
def dir_map(phy_add):
    tag_bit=phy_add[0:2]
    line_no=phy_add[2:5]
    block_off=phy_add[5:]
    #print(tag_bit,line_no,block_off)
    return tag_bit,line_no,block_off

def asso_map(phy_add):
    tag_bit=phy_add[0:5]
    block_off=phy_add[5:]
    return tag_bit,block_off

def sasso_map(phy_add):
    tag_bit=phy_add[0:3]
    set_no=phy_add[3:5]
    block_off=phy_add[5:]
    return tag_bit,set_no,block_off

def add_generator():
  phy_add = format(random.randint(0, 127), 'b') 
  while len(phy_add) < 7:
    phy_add = '0' + phy_add  
  return phy_add

def binary_to_decimal(binary_string):
  decimal_value = 0
  for i, digit in enumerate(binary_string[::-1]):
    decimal_value += int(digit) * 2**i
  return decimal_value

def lru(set_):
    mini=min(set_)
    j=set_.index(mini)
    return j 

for i in range(128):
    a=bin(i)[2:]
    if(len(a)<7):
        while(len(a)<7):
            a='0'+a
    mainmm.append(a)
    
def split_to_fours(original_list):
  nested_list = []
  sublist = []
  for element in original_list:
    sublist.append(element)
    if len(sublist) == 4:
      nested_list.append(sublist)
      sublist = []
  return nested_list

mm=split_to_fours(mainmm)

#l1 initialisation
l1=[]
tag_dir_l1=[]

l1_size=8
#Direct mapping L1
l1_map={}
for i in range(32):
    val = i% l1_size
    if val in l1_map:
        l1_map[val].append(i)
    else:
        l1_map[val]=[i,]      
       
for i in range(l1_size):
    v=l1_map[i][0]
    add_tup=dir_map(mm[v][0])
    l1.append([add_tup[0],mm[v]])
    tag_dir_l1.append(add_tup[0])

#SET ASSOCIATIVE
#l2 initialisation
l2={0:[],1:[],2:[],3:[]}
tag_dir_l2={0:[],1:[],2:[],3:[]}
l2_size=16
#mapping blocks to line
l2_map={}
set_no = 4
for i in range(32):
    val = i% set_no
    if val in l2_map:
        l2_map[val].append(i)
    else:
        l2_map[val]=[i,]
unique=[]
s= 0
for i in range(l2_size):
    v = random.choice(l2_map[i%set_no])   
    while(v in unique):
        v = random.choice(l2_map[i%set_no])
    unique.append(v)
    add_tuple=sasso_map(mm[v][0])
    l2[s]+=[[add_tuple[0],mm[v]]]
    tag_dir_l2[i%set_no].append(add_tuple[0])
    s+=1
    if (s>3):
        s=0

#FULLY ASSOCIATIVE
#Victim cache-
tag_dir_v1=['-1','-1','-1','-1']
v1 = []
line_ini=[['','']]
v1_line = 4
for i in range(v1_line):
    v1.append(line_ini)

#COUNTER
counter = {0:[0,1,2,3],1:[0,1,2,3],2:[0,1,2,3],3:[0,1,2,3]}

#SEGMENT 2 ADDRESS SEARCHING IN CACHES

for add in range(5):
    phy_add=add_generator()
    print("Address generated:",phy_add)


    #L1 searching
    tag_no_l1,line_no_l1,block_off_l1=dir_map(phy_add)
    line_no_l1=binary_to_decimal(line_no_l1)
    if(tag_dir_l1[line_no_l1]==tag_no_l1):
        print("Cache Hit")
    else:
        print("Not found in L1")
        print("Searching in Victim Cache.....")
        tag_no_v1,block_off_v1=asso_map(phy_add)
        if tag_no_v1 in tag_dir_v1:
            print("Element found in Victim Cache")
            kick=l1[line_no_l1]
            kick_tag=tag_dir_l1[line_no_l1]
            if(len(v1)<4):
                tag_v1_l1kick=asso_map(kick[1][0])[0]
                v1.append([tag_v1_l1kick,kick[1]])
                tag_dir_v1.append(tag_v1_l1kick)#appending tag to directory
            else:
                a=v1.pop(0)
                tag_dir_v1.pop(0)
                tag_v1_l1kick=asso_map(kick[1][0])[0]
                v1.append([tag_v1_l1kick,kick[1]])
                tag_dir_v1.append(tag_v1_l1kick)
            ind = tag_dir_v1.index(tag_no_v1)
            l1[line_no_l1] = [tag_no_l1,v1[ind][1]]
            print([tag_no_l1,v1[ind][1]])
            tag_dir_l1[line_no_l1]=tag_no_l1
        else:
            print("Not found in Victim Cache")
            print("Searching in Cache L2......")
            tag_no_l2,set_no_l2,block_off_l2=sasso_map(phy_add)
            set_no_l2=binary_to_decimal( set_no_l2)
            for i in range(set_no_l2):
                if tag_no_l2 == l2[set_no_l2][i][0]:
                    counter[set_no_l2][i]+=1
                    print("Element found in L2")
                    block_cpy = l2[set_no_l2][i][1]
                    kick=l1[line_no_l1]
                    if(len(v1)<4):
                        tag_v1_l1kick=asso_map(kick[1][0])[0]
                        v1.append([tag_v1_l1kick,kick[1]])
                        tag_dir_v1.append(tag_v1_l1kick)#appending tag to directory
                    else:
                        a=v1.pop(0)
                        tag_dir_v1.pop(0)
                        tag_v1_l1kick=asso_map(kick[1][0])[0]
                        v1.append([tag_v1_l1kick,kick[1]])
                        tag_dir_v1.append(tag_v1_l1kick)
                    #ind =tag_dir_v1.index(tag_no_v1)
                    ind=tag_dir_l2[set_no_l2].index(tag_no_l2)
                    print(l2[ind%set_no])
                    for j in l2[ind%set_no]:
                        if j[0][:2]==tag_no_l1:
                            block_act = j
                            print(block_act)
                    l1[line_no_l1] = [tag_no_l1,block_act[1]]
                    tag_dir_l1[line_no_l1]=tag_no_l1
                    break
                else:
                    if(counter[set_no_l2][i]>0):
                        counter[set_no_l2][i]-=1                     
            else:
                print("Not found in L2")
                print("Cache MISS")
                block_line=binary_to_decimal(phy_add[0:5])
                block_mm=mm[block_line]
                j=lru(counter[set_no_l2])
                l2[set_no_l2][j]=[tag_no_l2,block_mm]
                tag_dir_l2[set_no_l2].append(tag_no_l2)
                #print(tag_dir_l2)
                #Line from L2 is copied to L1 cache
                kick=l1[line_no_l1]
                if(len(v1)<4):
                    tag_v1_l1kick=asso_map(kick[1][0])[0]
                    v1.append([tag_v1_l1kick,kick[1]])
                    tag_dir_v1.append(tag_v1_l1kick)#appending tag to directory
                else:
                    a=v1.pop(0)
                    tag_dir_v1.pop(0)
                    tag_v1_l1kick=asso_map(kick[1][0])[0]
                    v1.append([tag_v1_l1kick,kick[1]])
                    tag_dir_v1.append(tag_v1_l1kick)
                #print(tag_no_l2)
                #print(tag_dir_l2)
                ind=tag_dir_l2[set_no_l2].index(tag_no_l2)

                
                #print([tag_no_l1,l2[ind%set_no][1][1]])
                for i in l2[ind%set_no]:
                        if i[0][:2]==tag_no_l1:
                            block_act = i
                print(block_act)
                l1[line_no_l1] = [tag_no_l1,block_act]
                tag_dir_l1[line_no_l1]=tag_no_l1
                print("Block from main memory fetched and copied to L1 and L2")
                
    print("----------------------------------------------------------")
print("Program terminated")
print(tag_dir_l1)
print(l1)
# Getting the data for the tables
data_v1 = []
for i in v1:
    if i == [['', '']]:
        data_v1.append(['', ''])
    else:
        l = []
        l.append(i[0])
        s = ''
        if i[1] != '':
            for j in i[1]:
                    s += j
                    s += ' '
        else:
            s = ''
        l.append(s)
        data_v1.append(l)
data_l2 = []
for i in l2:
    for j in l2[i]:
        data_l2.append(j)
data_l1 = l1

# Create the table object
list_v1 = Table(root, data = data_v1, header_text="Victim Cache", column_no = 2, width_firstcol = 4, width_seccol = 11, scrollbar = True)
list_l1 = Table(root, data = data_l1, header_text = "L1 Cache", column_no = 1, width_firstcol = 4, width_seccol = 11, scrollbar = True)
list_l2 = Table(root, data = data_l2, header_text = "L2 Cache", column_no = 3, scrollbar = True, width_firstcol = 4, width_seccol = 11)
list_mm = Table(root, data = data_mm, header_text = "Main Memory", column_no = 4, scrollbar = True)

root.mainloop()

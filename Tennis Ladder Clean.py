import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
from sqlite3 import Error
import datetime
import random

today = datetime.date.today()
today_string = "{0}/{1}/{2}".format(today.day,today.month,today.year)


def challenge(p1,p2):
    # Έλεγχος αν υπάρχουν τα ονόματα στο ranking
    if empty_check(p2):
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message=f"Δεν υπάρχει παίκτης στη θέση #{p2}")
        return
    
    # Υπολογισμός της διαφοράς των θέσεων που μπορεί να γίνει μια πρόκληση. Συγκεκριμένα για τις θέσεις 1 - 9
    # η διαφορά μπορεί να είναι μέχρι 3 θέσεις, ενώ για τις θέσεις απο 9 - ...  μέχρι 4 θέσεις.
    k5 = 4 if p1 > 9 else 3  # Αντί για   if player1 <= 9 ....
    if p1 - p2 > k5:
        
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message=f'''Ο παίκτης που προκαλείται βρίσκεται {k5} θέσεις πάνω από τον παίκτη που προκαλεί.
Η πρόκληση είναι άκυρη.''')
        return
    
    
    elif p1 - p2 < 0:
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message="Ο παίκτης που προκαλείται είναι κάτω από τον παίκτη που προκαλεί. \nΗ πρόκληση είναι άκυρη.")
        return
    
    
    elif p1 == p2:
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message='Λάθος καταχώρηση.')
        return exit
    
    answer = msg.askyesnocancel(title='Αποτέλεσμα Αγώνα',message=f'''Η πρόκληση είναι αποδεκτή.
Νίκησε ο παίκτης στη θέση #{p1} που έκανε την πρόκληση;''')
    
    if answer == True:
        win(p1, p2)
    if answer == False:
        win(p2,p1)
    if answer == None:
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message="Ο αγώνας δεν καταγράφηκε, ακύρωση από τον χρήστη.")
        return

    
        
def dbconnect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


#Δημιουργία ΔΒ + Πίνακα
def create_table():
    '''Δημιουργία πίνακα με Position, Name, Surname, Wins, Loses, Control_Date 
    όπου Control_Date τελευταία μέρα που έπαιξε αγώνα, ημέρα ένταξης στο club ή τελευταία φορά που υπέστη decay. 
    Position = Primary key'''
    my_conn = dbconnect('tennis_club.db') #Δημιουργεί ΔΒ αν δεν υπάρχει
    
    sql_query = "CREATE TABLE IF NOT EXISTS ranking (Position INTEGER PRIMARY KEY, Name VARCHAR(128),"\
                " Surname VARCHAR(128), Wins INTEGER, Loses INTEGER, Control_Date TEXT);" 
    c = my_conn.cursor()

    c.execute(sql_query) #Δημιουργία Πίνακα με τη Θέση ως Primary Key
    
    my_conn.commit()
    my_conn.close()


#Αρχικοποίηση κατάταξης
def initialization(initializationPlayers,today_string=today_string):
    '''Δέχεται λίστα με όνομα και επίθετο χωρισμένα με κενό και την εκχωρεί στον πίνακα'''
    random.shuffle(players)
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    
    for i,player in enumerate(initializationPlayers):
        entry = (i + 1, initializationPlayers[i][0], initializationPlayers[i][1], 0, 0, today_string)
        c.execute("INSERT INTO ranking VALUES {0}".format(entry))
   
    my_conn.commit()
    my_conn.close()
    msg.showinfo(master=w1, title='Ειδοποίηση', 
                            message='Οι παίκτες καταχωρήθηκαν τυχαία στην κατάταξη.')



#Print όλη την κατάταξη
def print_():
    '''Τυπώνει την κατάταξη με όλα τα στοιχεία σε μορφοποιημένη ευανάγνωστη διάταξη (πλην Control_Date, 
    για αυτή χρησιμοποιήστε print_ranking())'''

    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    allDBData = c.execute("SELECT * FROM ranking;")
    rankingList = []    
    
    for x1,x2,x3,x4,x5,x6 in allDBData.fetchall():
        rankingList.append((x1,x2,x3,x4,x5))
    
    for item in rankingList:
        tree.insert('',tk.END,values=item)
    my_conn.close()
    return

    
#Εισαγωγή παίκτη στο τέλος της κατάταξης, προεπιλεγμένες τιμές για Wins & Loses = 0
#Control_Date σήμερα ως ημέρα ένταξης
def insert_bottom(Name='', Surname='', Wins=0, Loses=0, Control_Date=today_string):
    '''Εισαγωγή παίκτη στο τέλος της κατάταξης. Εισάγετε Όνομα και Επώνυμο. 
    Νίκες και ήττες έχουν προεπιλεγμένες τιμές 0.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    #Αν η πρώτη θέση είναι κενή δε χρειάζεται να ληφθεί το δεδομένο της τελευταίας θέσης, παίρνει τιμή 1
    #Καταχώρηση νέας τελευταίας θέσης
    new_last_place = 1 if empty_check(1) else c.execute("SELECT Position FROM ranking;").fetchall()[-1][0] + 1
    
    newPlayer = (new_last_place, Name, Surname, Wins, Loses, today_string) #Πλειάδα στοιχείων παίκτη
    c.execute("INSERT INTO ranking VALUES {0};".format(newPlayer)) #Εκχώρηση παίκτη σε αυτή τη θέση
    
    msg.showinfo(master=w1,parent=nameEntryWindow, title='Ειδοποίηση', 
                            message=f'Ο {Name} {Surname} τοποθετήθηκε επιτυχώς στη θέση #{new_last_place}.')
    
    my_conn.commit()
    my_conn.close()


#Εισαγωγή παίκτη σε επιλεγμένη θέση στην κατάταξη, προεπιλεγμένες τιμές για Wins & Loses = 0
def insert_place(Rank, Name='', Surname='', Wins=0, Loses=0, Control_Date=today_string):
    '''Εισαγωγή παίκτη σε συγκεκριμένη θέση λόγω γνωστής αντικειμενικά υψηλότερης απόδοσης. 
    Ο παίκτης που βρισκόταν στη θέση θα μεταφερθεί μία θέση κάτω, όπως κι όλοι οι χαμηλότεροι παίκες.'''

    if empty_check(Rank-1) and Rank != 1: #Αν προσπαθεί να βάλει τον παίκτη σε θέση πάνω από την οποία δεν 
    #υπάρχει άλλος παίκτης
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message=f"Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη {Name} {Surname}.")

    else:
        if not empty_check(1): #Αν η λίστα έχει παίκτες
            my_conn = dbconnect('tennis_club.db')
            c = my_conn.cursor()

            # Query για να πάρουμε την τελευταία θέση απο τον πίνακα της κατάταξης σε φθίνουσα σειρά
            # περιορίζοντας τα αποτελέσματα σε 1 σειρά
            last_place = c.execute("SELECT Position FROM ranking ORDER BY Position DESC LIMIT 1;").fetchone()[0]
            my_conn.close()
            update_positions(Rank, last_place) #...για να τεθεί παράμετρος εδώ, που μεταθέτονται όλοι οι παίκτες 
            #μία θέση κάτω αφήνοντας τη θέση ενδιαφέροντος κενή

        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        newPlayer = (Rank, Name, Surname, Wins, Loses, today_string)
        
        #Εισαγωγή στην κατάταξη είτε η λίστα έχει παίκτες, είτε δεν έχει και ο χρήστης διάλεξε θέση 1
        c.execute("INSERT INTO ranking VALUES {0};".format(newPlayer)) 
        msg.showinfo(master=w1, parent=positionEntryWindow, title='Ειδοποίηση', 
                                message=f'Ο παίκτης {Name} {Surname} τοποθετήθηκε επιτυχώς στη θέση #{Rank}.')

        my_conn.commit()
        my_conn.close()



#Διαγραφή παίκτη
def delete_player(index):
    '''Διαγράφει τον παίκτη στη θέση που δίνεται από το index και μετακινεί τους κατώτερους παίκτες μία θέση πάνω, 
    καλύπτοντας το κενό που δημιουργείται'''
    if empty_check(index): #Έλεγχος αν η θέση περιέχει άτομο
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message="Δεν υπάρχει παίκτης στη θέση που προσπαθείτε να κάνετε διαγραφή.")
    else:
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        playerDBData = c.execute("SELECT * FROM ranking WHERE Position = {0};".format(index)).fetchall()
        confirmation = msg.askyesno(
title='Διαγραφή Παίκτη', parent=deletion, 
message=f'''ΠΡΟΣΟΧΉ!!!! Η διαγραφή είναι οριστική κι αμετάκλητη!
Θα χαθούν ΌΛΑ τα δεδομένα του παίκτη.
Θέλετε σίγουρα να διαγράψετε τον παίκτη {playerDBData[0][1]} {playerDBData[0][2]}; ''')
        
        if confirmation == False:
            my_conn.commit()
            my_conn.close()
            msg.showerror(master=w1, parent=deletion, title='Ειδοποίηση', 
                                    message="Η διαγραφή ακυρώθηκε από τον χρήστη.")
            deletionEntry.delete(0,'end')
            return
        
        
        c.execute("DELETE FROM ranking WHERE Position={0};".format(index)) #Διαγραφή παίκτη
        c.execute("UPDATE ranking SET Position = Position - 1 WHERE Position > {0};".format(index)) #Ανανέωση λίστας
        
        my_conn.commit()
        my_conn.close()
        
        msg.showinfo(master=w1, parent=deletion, title='Ειδοποίηση', 
                                message=f'Ο παίκτης στη θέση #{index} διαγράφηκε επιτυχώς.')
        deletionEntry.delete(0,'end')


#Καταγραφή νίκης με παραμέτρους τις θέσεις τους ΠΡΙΝ την αλλαγή κατάταξης
def win(winner_index, loser_index,today_string=today_string):
    '''Εισάγετε την έως τώρα θέση νικητή και μετά ηττημένου. Ο νικητής θα λάβει τη θέση του ηττημένου. 
    Ο ηττημένος και όλοι οι παίκτες μεταξύ των δύο θέσεων θα μετακινηθούν μία θέση κάτω.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

     # +1 Wins σε νικητή και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute("UPDATE ranking SET Wins = Wins + 1, Control_Date = '{0}' WHERE Position = {1};".format(today_string, 
                                                                                                      winner_index))
    # +1 Loses σε ηττημένο και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute("UPDATE ranking SET Loses = Loses + 1, Control_Date = '{0}' WHERE Position = {1};".format(today_string, 
                                                                                                        loser_index))

    if loser_index < winner_index:
        sql_query = "SELECT * FROM Ranking WHERE Position={0};".format(winner_index)  #Προσωρινή αποθήκευση νικητή
        x = c.execute(sql_query)

        playerDBData = x.fetchall() #Επιστρέφει λίστα, με το playerDBData[0] να είναι πλειάδα στοιχείων του νικητή        
        c.execute("DELETE FROM ranking WHERE Position={0};".format(winner_index)) #Διαγραφή νικητή από προηγούμενη θέση
        entryData = (loser_index, playerDBData[0][1], playerDBData[0][2], playerDBData[0][3], playerDBData[0][4], playerDBData[0][5]) #Νέα πλειάδα για αλλαγή "Position"
        
        my_conn.commit()
        my_conn.close()

        #Κλήση συνάρτησης ανακατάταξης που κατεβάζει τους παίκτες κατά μία θέση από 
        #την winner_index μέχρι ΚΑΙ τη loser_index
        update_positions(loser_index, winner_index) 

        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        #Εισαγωγή νικητή στη θέση ηττημένου
        c.execute("INSERT INTO ranking(Position, Name, Surname, Wins, Loses, Control_Date) VALUES {0};".format(entryData))
        msg.showinfo(master=w1, title='Ειδοποίηση', 
                                message='Το παιχνίδι καταγράφηκε επιτυχώς και η κατάταξη ανανεώθηκε!')
    else:
        msg.showinfo(master=w1, title='Ειδοποίηση', 
                                message='Το παιχνίδι καταγράφηκε επιτυχώς, χωρίς αλλαγή στην κατάταξη!')

    my_conn.commit()
    my_conn.close()
    


#Μεταθέτει όλα τα Positions κατά ένα κάτω αρχίζοντας από το big_num --> big_num+1 μέχρι ΚΑΙ το small_num-->small_num+1
def update_positions(small_num, big_num):
    '''Μετακινεί όλες τις Positions κατά μία κάτω αρχίζοντας από το big_num. 
    Προεπιλογή big_num (αν δεν υπάρχει κενό) πρέπει να είναι η τελευταία θέση. 
    Το small_num θα είναι το Position που θα είναι κενό μετά την κλήση.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    counter = big_num + 1 #Μετρητής τιμής Position που θέλουμε να θέσουμε
    #Πρώτα το big_num entry γίνεται big_num+1 για να μην έχουμε σύγκρουση Primal Keys
    for p in range(big_num, small_num-1, -1): 
            c.execute('UPDATE ranking SET Position = {0} WHERE Position={1}'.format(counter, p)) #Το p είναι μετρητής τρέχουσας θέσης για το WHERE και μειώνεται σε κάθε loop
            counter -= 1 #Μείωση counter για σωστή εισαγωγή Position

    my_conn.commit()
    my_conn.close()



#Μεταθέτει τον παίκτη που υπόκειται σε decay λόγω αδράνειας μία θέση κάτω ανεβάζοντας τον κάτω στη θέση του
def rank_decay(index,today_string=today_string):
    '''Ο παίκτης της θέσης index πέφτει μία θέση λόγω αδράνειας κι ο κάτω του ανεβαίνει στη θέση του.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    x = c.execute("SELECT Position FROM ranking;")
    last_place = x.fetchall()[-1][0]  # λήψη τελευταίας θέσης
    
    #Η Control Date ανανεώνεται ως τελευταία ημέρα τροποποίησης ώστε να μην υπόκειται σε decay ξανά πχ αύριο
    x = c.execute("SELECT * FROM ranking WHERE Position={0};".format(index))
    inactive_player = x.fetchall() #Αποθήκευση στοιχείων του παίκτη που υπόκειται σε rank decay
    
    if last_place == inactive_player[0][0]: #Έλεγχος για την περίπτωση που ο παίκτης είναι τελευταίος
        msg.showinfo(master=w1, title='Ειδοποίηση', 
                                message="Ο παικτης {0} {1} είναι ήδη στην τελευταία θέση και δεν πέφτει περαιτέρω.".format(
            inactive_player[0][1], inactive_player[0][2]))
        c.execute("UPDATE ranking SET Control_Date='{0}' WHERE Position={1};".format(today_string, index))
        
    if last_place != inactive_player[0][0]:
        c.execute("DELETE FROM ranking WHERE Position={0};".format(index)) #Διαγραφή του παίκτη
        #Μετακίνηση του κάτω παίκτη στην πλέον κενή θέση
        c.execute("UPDATE ranking SET Position = {0} WHERE Position={1};".format(index,index+1)) 
        entry = (
            inactive_player[0][0]+1, inactive_player[0][1], inactive_player[0][2], inactive_player[0][3],
            inactive_player[0][4], today_string)
        #Εισαγωγή decaying παίκτη στην πλέον κενή θέση του από κάτω παικτή
        c.execute("INSERT INTO ranking VALUES {0};".format(entry)) 

    my_conn.commit()
    my_conn.close()


#Απαραιτητο για τις υπόλοιπες εσωτερικές λειτουργίες συναρτήσεων
def empty_check(index):
    '''Ελέγχει αν ο πίνακας έχει παίκτη στη θέση που καταχωρείται κι επιστρέφει boolean type variable'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    
    c.execute("SELECT Position FROM ranking WHERE Position={0};".format(index))
    empty_check = c.fetchall() #Πλειάδα με νούμερο για Position ή κενή αν δεν υπάρχει παίκτης
    flag = len(empty_check) == 0
    
    my_conn.close()
    return flag
    

def check_ranking_for_decay(today=today):
    '''Ελέγχει αν υπάρχουν παίκτες που υπόκεινται σε decay στην κατάταξη'''
    conn = dbconnect('tennis_club.db')
    cursor = conn.cursor()

    decaylist = [] #Λίστα με παίκτες που θα υποστούν decay
    cursor.execute("SELECT Position, Control_Date FROM ranking;")
    ranking = cursor.fetchall()
    
    for index, date in ranking:
        x = date.split(sep='/') #Διαχωρίζει το string
        last_play_date = datetime.date(int(x[2]),int(x[1]),int(x[0])) #Μετατροπή του string σε datetime object
        days_since_last_play = (today - last_play_date).days
        if days_since_last_play > 30:
            #Προστίθεται στη λίστα, η αλλαγή δεν γίνεται εδώ γιατί οδηγεί σε logical error του περάσματος for
            decaylist.append(index) 
    
    conn.commit()
    conn.close()    
    
    if decaylist: #Αν η λίστα δεν είναι κενή
        st = ','.join([str(ele) for ele in decaylist])
        ts = ''.join(['Οι παίκτες στις θέσεις ', st, ' έπεσαν μία θέση λόγω αδράνειας και η κατάταξη ανανεώθηκε.'])
        msg.showinfo(master=w1, title='Ειδοποίηση', 
                                message=ts)
        #Αντίστροφο πέρασμα της λίστας για αποφυγή λαθών από την αλλαγή θέσης
        for i in decaylist[::-1]: 
            rank_decay(i)            
    
    else:
        msg.showinfo(master=w1, title='Ειδοποίηση', 
                                message="Δεν υπάρχει κανένας παίκτης που να υπόκειται σε μείωση θέσης λόγω αδράνειας.")



def b1pushed():
    flag = empty_check(1) 
    if not flag: #Έλεγχος για το αν ο πίνακας περιέχει παίκτες        
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message='''Ο πίνακας κατάταξης περιέχει ήδη παίκτες και δεν μπορεί να αρχικοποιηθεί τυχαία. 
Παρακαλώ, διαγράψτε όλους τους παίκτες ή προσθέστε παίκτες χρησιμοποιώντας κάποια από τις επιλογές.''')
        return
    
    global players
    players = []
    global myVar
    myVar = tk.StringVar()
    myVar.set('Κενή Λίστα Παικτών')
    global dialogInitialize
    dialogInitialize = tk.Toplevel(w1)
    dialogInitialize.title('Αρχικοποίηση λίστας')
    dialogInitialize.geometry('400x500+700+350')
    
    global bleh
    bleh = tk.Entry(dialogInitialize,justify='center', font='Times 16',selectborderwidth=3)
    bleh.pack(pady=10)
    b = tk.Button(dialogInitialize, text="Καταχώρηση Παίκτη", font='Times 16', command = dialogInitialize1Pushed)
    b.pack(pady=5)
    tk.Button(dialogInitialize,text="Τέλος Καταχωρήσεων",font = 'Times 16', command = dialogInitialize2Pushed).pack(pady=5)
    ttk.Separator(dialogInitialize,orient='horizontal').pack(fill='x',pady=15)
    tk.Label(dialogInitialize, textvariable = myVar, font = 'Times 16',justify='center').pack()     
                   # = input("Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε ή 0 για τερματισμό: ")    
    dialogInitialize.mainloop()
    

def dialogInitialize1Pushed():
    name = bleh.get()
    bleh.delete(0,'end')
    player = name.split(sep=' ')
    
    if len(player) != 2: #Περίπτωση που εισαχθούν πάνω απο 1 κενά
        msg.showerror(master=w1, parent=dialogInitialize,  title='Ειδοποίηση', 
                                message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.")
        return
    players.append(player)
    global myVar
    if myVar.get() == 'Κενή Λίστα Παικτών':
        myVar.set("Λίστα Παικτών\n")
    string = '\n'.join([myVar.get(),name])
    myVar.set(string)
    return

def dialogInitialize2Pushed():
    if players:
        initialization(players)
        dialogInitialize.destroy()
        return
    else: #Αν η λίστα players είναι κενή
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message='Δε δημιουργήθηκε κατάταξη καθώς δεν εισάγατε ονόματα.')
        dialogInitialize.destroy()
        return

def b2pushed():
    global answerAddition
    answerAddition = msg.askyesnocancel(title='Προσθήκη Παίκτη',message='''Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση;''')
    if answerAddition == None:
        msg.showinfo(master=w1, title='Ειδοποίηση', 
                                message='Η προσθήκη παίκτη ακυρώθηκε.')
        return
            
    global nameEntryWindow
    nameEntryWindow = tk.Toplevel(w1)
    nameEntryWindow.geometry("550x150+650+350")
    nameEntryWindow.title('Προσθήκη Παίκτη')
    tk.Label(nameEntryWindow, font=defaultFont, text = "Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε: ").pack(pady=5)
    global nameEntered
    nameEntered = tk.Entry(nameEntryWindow, font=defaultFont, justify='center')
    nameEntered.pack(pady=5)
    tk.Button(nameEntryWindow, text='Προσθήκη', font=defaultFont, command=nameEntryPushed).pack(pady=5)
    

def nameEntryPushed():
    x = nameEntered.get()
    nameEntered.delete(0,'end')
    global playerAdded
    playerAdded = x.split(sep=' ')
    if len(playerAdded) != 2: 
        msg.showerror(master=w1, parent=nameEntered, title='Ειδοποίηση', 
                                         message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.")
        return
    name,surname = playerAdded[0], playerAdded[1]
    if answerAddition == False:
        insert_bottom(name,surname)
        nameEntryWindow.destroy()
    elif answerAddition == True:
        global positionEntryWindow
        positionEntryWindow = tk.Toplevel(nameEntryWindow)
        positionEntryWindow.geometry("600x150+625+450")
        positionEntryWindow.title("Προσθήκη Παίκτη σε Θέση")
        tk.Label(positionEntryWindow, font=defaultFont, text='Δώστε τη θέση κατάταξης του παίκτη που θέλετε να προσθέσετε: ').pack(pady=5)
        global positionEntry
        positionEntry = tk.Entry(positionEntryWindow, font=defaultFont, justify='center')
        positionEntry.pack(pady=5)
        tk.Button(positionEntryWindow, font=defaultFont, text='OK',command=positionPushed).pack(pady=5)
        
    return

def positionPushed():
    try:
        positionEntered = int(positionEntry.get())
        positionEntry.delete(0,'end')
        name,surname = playerAdded[0], playerAdded[1]
        insert_place(positionEntered,name,surname)
        positionEntryWindow.destroy()
        nameEntryWindow.destroy()
    except ValueError:
        msg.showerror(master=positionEntryWindow, parent=positionEntryWindow, title='Ειδοποίηση', 
                                message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")
    return
    

def b3pushed():
    if empty_check(1):
        msg.showerror(master=w1, title='Ειδοποίηση', message="Η κατάταξη δεν περιέχει παίκτες!")
    else:
        global deletion
        deletion = tk.Toplevel(w1)
        deletion.geometry("550x200+650+450")
        deletion.title('Διαγραφή Παίκτη')
        tk.Label(deletion, text='Δώστε τη θέση κατάταξης του παίκτη που θέλετε να διαγράψετε: ', font = 'Times 14').pack(pady=20)
        global deletionEntry
        deletionEntry = tk.Entry(deletion,justify = 'center', font=defaultFont)
        deletionEntry.pack(pady=5)
        tk.Button(deletion, text='Διαγραφή', font='Times 16', command=deletePushed).pack(side='left',padx=60)
        tk.Button(deletion, text='Ακύρωση', font='Times 16', command=deletion.destroy).pack(side='right',padx=60)
        
        deletion.mainloop()
        

def deletePushed():
    try:
        index = int(deletionEntry.get())
        delete_player(index)
    except ValueError:
        msg.showerror(master=w1, parent=deletion, title='Ειδοποίηση', 
                                message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")
        deletionEntry.delete(0,'end')
    return

def b4pushed():
    if empty_check(1):
        msg.showerror(master=w1, title='Ειδοποίηση', message="Η κατάταξη δεν περιέχει παίκτες!")
    elif empty_check(2):
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message="Η κατάταξη περιέχει μόνο έναν παίκτη άρα δεν ορίζεται πρόκληση.")
    else:
        global challengeDialog1
        challengeDialog1 = tk.Toplevel(w1)
        challengeDialog1.geometry("650x200+650+450")
        challengeDialog1.title("Καταγραφη Πρόκλησης")
        global challengeLabel
        challengeLabel = tk.StringVar()
        challengeLabel.set('Δώστε τη θέση κατάταξης του παίκτη που προκαλεί: ')
        tk.Label(master=challengeDialog1, textvariable= challengeLabel, font=defaultFont).pack(pady = 10)
        global challengeEntry
        challengeEntry = tk.Entry(master=challengeDialog1, justify='center', font=defaultFont)
        challengeEntry.pack(pady = 10)
        tk.Button(master=challengeDialog1, text='OK', font = defaultFont, command=challengePushed).pack(pady = 10)
        global pr
        pr = []
        challengeDialog1.mainloop()


def challengePushed():
    try:
        if empty_check(int(challengeEntry.get())):
            msg.showerror(master=w1, title='Ειδοποίηση', 
                                    message=f"Δεν υπάρχει παίκτης στη θέση #{challengeEntry.get()}")
        pr.append(int(challengeEntry.get()))
        challengeEntry.delete(0,'end')
    except ValueError:
        msg.showerror(master=w1, title='Ειδοποίηση', 
                                message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")
        return
    if len(pr) == 1:
        challengeLabel.set('Δώστε τη θέση κατάταξης του παίκτη που δέχεται την πρόκληση:')
    elif len(pr) == 2:
        challenge(pr[0],pr[1])
        challengeDialog1.destroy()
        
    return


def b5pushed():
    if empty_check(1):
        msg.showerror(master=w1, title='Ειδοποίηση', message="Η κατάταξη δεν περιέχει παίκτες!")
    else:
        check_ranking_for_decay()

def b6pushed():
    if empty_check(1):
        msg.showerror(master=w1, title='Ειδοποίηση', message="Η κατάταξη δεν περιέχει παίκτες!")
    else:
        new = tk.Toplevel(w1)
        new.title("Πίνακας Κατάταξης")
        new.geometry("1000x800+350+0")
        style = ttk.Style()
        style.configure("mystyle.Treeview",font=('Times',16),rowheight=30)
        global tree
        tree = ttk.Treeview(new, style="mystyle.Treeview", columns=('Θέση', 'Όνομα', 'Επίθετο', 'Νίκες', 'Ήττες'),show='headings')
        tree.column('Θέση', width=45)
        tree.column('Όνομα', width=150)
        tree.column('Επίθετο', width=225)
        tree.column('Νίκες', width=45)
        tree.column('Ήττες', width=45)
        tree.heading('Θέση', text = 'Θέση')
        tree.heading('Όνομα', text = 'Όνομα')
        tree.heading('Επίθετο', text = 'Επίθετο')
        tree.heading('Νίκες', text = 'Νίκες')
        tree.heading('Ήττες', text = 'Ήττες')
        print_()
        tree.pack(fill='both',expand=1)
        new.mainloop()        
        return
    
def b7pushed():
    w1.destroy()


    
w1 = tk.Tk()
w1.geometry('600x600+650+150')
w1.title("Tennis Ladder App")
defaultFont = 'Times 16'
L1 = tk.Label(w1, text = ' Tennis Ladder App ', font = 'Times 35 bold', 
fg = 'Black', relief='ridge', bd=10)
button1 = tk.Button(w1, text = 'Αρχικοποίηση κατάταξης', font = defaultFont, 
                    command = b1pushed, relief='groove', bd=10)
button2 = tk.Button(w1, text = 'Προσθήκη παίκτη', font = defaultFont, 
                    command = b2pushed, relief='groove', bd=10)
button3 = tk.Button(w1, text = 'Διαγραφή παίκτη', font = defaultFont, 
                    command = b3pushed, relief='groove', bd=10)
button4 = tk.Button(w1, 
                    text = 'Έλεγχος και καταγραφή αποτελέσματος πρόκλησης', 
                    font = defaultFont, 
                    command = b4pushed, relief='groove', bd=10)
button5 = tk.Button(w1, text = 'Έλεγχος κατάταξης για αδρανείς παίκτες', 
                    font = defaultFont, command = b5pushed, relief='groove', bd=10)
button6 = tk.Button(w1, text = 'Εμφάνιση κατάταξης', font = defaultFont, 
                    command = b6pushed, relief='groove', bd=10)
button7 = tk.Button(w1, text = 'Έξοδος', font = defaultFont, 
                    command = b7pushed, relief='groove', bd=10)

ttk.Separator(w1,orient='horizontal').pack(fill='x',pady=15)
button1.pack(fill='x', padx=50, pady=10)
button2.pack(fill='x', padx=50, pady=10)
button3.pack(fill='x', padx=50, pady=10)
button4.pack(fill='x', padx=50, pady=10)
button5.pack(fill='x', padx=50, pady=10)
button6.pack(fill='x', padx=50, pady=10)
button7.pack(fill='x', padx=50, pady=10)
tk.Label(w1, text='Made by Black Baron', font = ('Old English Text MT',12),justify='left').pack(side='right')
create_table()
w1.mainloop()


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
    """
    Συνάρτηση που ελέγχει την πρόκληση και κάνει τις απαραίτητες αλλαγές 
    ή ενημερώνει τον χρήστη για το λάθος.
    
    
    Args:
        p1 (int): Θέση του παίκτη που θέτει την πρόκληση.
        p2 (int): Θέση του παίκτη που δέχεται την πρόκληση.
        
    Returns:
        None.
    """
        
    # Υπολογισμός της διαφοράς των θέσεων που μπορεί να γίνει μια πρόκληση. 
    # Συγκεκριμένα για τις θέσεις 1 - 9 η διαφορά μπορεί να είναι μέχρι 3 θέσεις,
    # ενώ για τις θέσεις από 9 και πάνω, μέχρι 4 θέσεις.
    allowed_challenge_distance = 4 if p1 > 9 else 3
    # Έλεγχος πως επιτρέπεται η διαφορά θέσεων
    if p1 - p2 > allowed_challenge_distance:
        
        msg.showerror(
            master=main_window, 
            parent=challengeDialog, 
            title='Ειδοποίηση', 
            message=f'''Ο παίκτης που προκαλείται βρίσκεται πάνω από {allowed_challenge_distance} θέσεις πάνω από τον παίκτη που προκαλεί.
Η πρόκληση είναι άκυρη.''')
        return
    
    # Έλεγχος πως ο παίκτης που προκαλεί είναι κάτω από τον παίκτη που προκαλείται
    elif p1 < p2:
        msg.showerror(
            master=main_window,
            parent=challengeDialog, 
            title='Ειδοποίηση', 
            message="Ο παίκτης που προκαλείται είναι κάτω από τον παίκτη που προκαλεί. \nΗ πρόκληση είναι άκυρη.")
        return
    
    # Έλεγχος για περίπτωση εισαγωγής ίδιου παίκτη
    elif p1 == p2:
        msg.showerror(
            master=main_window, 
            parent=challengeDialog, 
            title='Ειδοποίηση', 
            message='Λάθος καταχώρηση, ο παίκτης που προκαλεί είναι ο παίκτης που δέχεται την πρόκληση.')
        return
    
    # Ενημέρωση αποδοχής πρόκλησης και ερώτηση έκβασης αγώνα
    answer = msg.askyesnocancel(
        master=main_window, 
        parent=challengeDialog, 
        title='Αποτέλεσμα Αγώνα',
        message=f'''Η πρόκληση είναι αποδεκτή.
Νίκησε ο παίκτης στη θέση #{p1} που έκανε την πρόκληση;'''
        )
    
    if answer == True:
        win(p1, p2)
        return
    if answer == False:
        win(p2,p1)
        return
    # Αν ο χρήστης κλείσει το παράθυρο χωρίς να απαντήσει για νικητή
    if answer == None:
        msg.showerror(
            master=main_window,
            parent=challengeDialog, 
            title='Ειδοποίηση', 
            message="Ο αγώνας δεν καταγράφηκε, ακύρωση από τον χρήστη."
            )
        return

    
      
def dbconnect(db_file):
    """
    Βοηθητική συνάρτηση που συνδέεται με/δημιουργεί ΒΔ.
    
    
    Args:
        db_file (str): Όνομα του αρχείου ΒΔ.
        
    Returns:
        sqlite3.Connection: Αντικείμενο σύνδεσης στη βάση δεδομένων ή None σε 
        περίπτωση αποτυχίας.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table():
    """
    Συνάρτηση που δημιουργεί πίνακα με Position, Name, Surname, Wins, Loses, 
    Control_Date, όπου Control_Date τελευταία μέρα που έπαιξε αγώνα, ημέρα 
    ένταξης στο club ή τελευταία φορά που υπέστη decay. 
    Position = Primary key
    """
    my_conn = dbconnect('tennis_club.db') # Δημιουργεί ΔΒ αν δεν υπάρχει
    
    sql_query = "CREATE TABLE IF NOT EXISTS ranking (Position INTEGER PRIMARY KEY, Name VARCHAR(128),"\
                " Surname VARCHAR(128), Wins INTEGER, Loses INTEGER, Control_Date TEXT);" 
    c = my_conn.cursor()

    c.execute(sql_query) # Δημιουργία Πίνακα με τη Θέση ως Primary Key
    
    my_conn.commit()
    my_conn.close()


def initialization(initializationPlayers,today_string=today_string):
    """
    Συνάρτηση αρχικοποίησης κατάταξης. Δέχεται λίστα με όνομα και επίθετο 
    χωρισμένα με κενό και την εκχωρεί στον πίνακα της ΒΔ με ανακατεμένη σειρά.
    
    
    Args:
        initializationPlayers (list): Λίστα με στοιχεία str όνομα και επίθετο.
        today_string (str): Σημερινή ημερομηνία σε μορφή "{ημέρα}/{μήνας}/{έτος}".
    Returns:
        None.
    """
    
    # Τυχαιοποίηση σειράς παικτών
    random.shuffle(initializationPlayers)
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    
    # Εισαγωγή παικτών στη ΒΔ με τυχαία σειρά
    for i,player in enumerate(initializationPlayers):
        # Το i είναι το index + 1 για να ξεκινάει από τη θέση 1
        # Όνομα, επώνυμο, νίκες, ήττες, ημερομηνία δραστηριότητας
        entry = (
            i + 1, 
            initializationPlayers[i][0], 
            initializationPlayers[i][1], 
            0, 
            0, 
            today_string
            )
        c.execute("INSERT INTO ranking VALUES {0}".format(entry))
   
    my_conn.commit()
    my_conn.close()
    msg.showinfo(
        master=main_window, 
        title='Ειδοποίηση', 
        message='Οι παίκτες καταχωρήθηκαν τυχαία στην κατάταξη.'
        )


def fill_tree():
    """
    Ενημερώνει το tree του UI εκχωρώντας σε αυτό τα στοιχεία όλων των παικτών 
    (πλην Control_Date, για αυτή χρησιμοποιήστε την εσωτερική συνάρτηση 
    print_ranking())
    """
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # Παίρνει όλα τα δεδομένα από τη ΒΔ
    allDBData = c.execute("SELECT * FROM ranking;")
    rankingList = []    
    
    for x1,x2,x3,x4,x5,x6 in allDBData.fetchall():
        rankingList.append((x1,x2,x3,x4,x5))
    
    # Εισάγει τα δεδομένα στο tree
    for item in rankingList:
        tree.insert('',tk.END,values=item)
    
    my_conn.close()
    return

    

def insert_bottom(Name='', Surname='', Wins=0, Loses=0, Control_Date=today_string):
    """
    Εισαγωγή παίκτη στο τέλος της κατάταξης, προεπιλεγμένες τιμές για Wins & 
    Loses = 0. Control_Date σήμερα ως ημέρα ένταξης. Εκχωρεί τα δεδομένα στη ΒΔ.
    
    Args:
        Name (str): Όνομα παίκτη.
        Surname (str): Επίθετο παίκτη.
        Wins (int): Νίκες παίκτη. Προεπιλεγμένη τιμή 0.
        Loses (int): Ήττες παίκτη. Προεπιλεγμένη τιμή 0.
        Control_Date (str): Ημερομηνία τελευταίας δραστηριότητας.
        Προεπιλεγμένη τιμή η σημερινή ημέρα ως ημέρα ένταξης σε μορφή 
        "{ημέρα}/{μήνας}/{έτος}".
    
    Returns:
        None.
    """
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # Αν η πρώτη θέση είναι κενή δε χρειάζεται να ληφθεί το δεδομένο της 
    # τελευταίας θέσης, παίρνει τιμή 1. Καταχώρηση νέας τελευταίας θέσης
    new_last_place = 1 if empty_check(1) else c.execute("SELECT Position FROM ranking;").fetchall()[-1][0] + 1
    
    newPlayer = (
        new_last_place, 
        Name, 
        Surname, 
        Wins, 
        Loses, 
        today_string
        ) #Πλειάδα στοιχείων παίκτη
    c.execute("INSERT INTO ranking VALUES {0};".format(newPlayer)) #Εκχώρηση παίκτη σε αυτή τη θέση
    
    # Μήνυμα ενημέρωσης επιτυχούς εισαγωγής
    msg.showinfo(
        master=main_window,
        parent=nameEntryWindow, 
        title='Ειδοποίηση', 
        message=f'Ο {Name} {Surname} τοποθετήθηκε επιτυχώς στη θέση #{new_last_place}.'
        )
    
    my_conn.commit()
    my_conn.close()


def insert_place(Rank, Name='', Surname='', Wins=0, Loses=0, Control_Date=today_string):
    """
    Εισαγωγή παίκτη σε επιλεγμένη θέση στην κατάταξη της ΒΔ, προεπιλεγμένες τιμές 
    για Wins & Loses = 0, προεπιλεγμένη τιμή για ημέρα δραστηριότητας η σημερινή ως
    ημέρα ένταξης στην κατάταξη. Ο παίκτης που κατείχε τη θέση αυτή και όλοι οι
    παίκτες κάτω του μετακινούνται κατά μία θέση κάτω.
    
    
    Args:
        Rank (int): Θέση κατάταξης που θα μπει ο παίκτης που εισάγεται.
        Name (str): Όνομα παίκτη.
        Surname (str): Επίθετο παίκτη.
        Wins (int): Νίκες παίκτη. Προεπιλεγμένη τιμή 0.
        Loses (int): Ήττες παίκτη. Προεπιλεγμένη τιμή 0.
        Control_Date (str): Ημερομηνία τελευταίας δραστηριότητας. Προεπιλεγμένη
        τιμή η σημερινή ημέρα ως ημέρα ένταξης σε μορφή "{ημέρα}/{μήνας}/{έτος}".
        
    Returns:
        None.
    """
    
    # Αν προσπαθεί να βάλει τον παίκτη σε θέση πάνω από την οποία δεν υπάρχει 
    # άλλος παίκτης
    if empty_check(Rank-1) and Rank != 1: 
        msg.showerror(
            master=main_window, 
            parent=positionEntryWindow,
            title='Ειδοποίηση', 
            message=f"Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη {Name} {Surname}."
            )

    else:
        # Αν η λίστα έχει παίκτες πρέπει να μετακινηθούν όλοι μία θέση κάτω
        if not empty_check(1): 
            my_conn = dbconnect('tennis_club.db')
            c = my_conn.cursor()

            # Λήψη τρέχουσας τελευταίας θέσης κατάταξης
            last_place = c.execute("SELECT Position FROM ranking ORDER BY Position DESC LIMIT 1;").fetchone()[0]
            my_conn.close()
            # Δημιουργείται κενό βάσει της τελευταίας θέσης και της θέσης που 
            # θα εισαχθεί ο παίκτης
            update_positions(Rank, last_place) 
        
        # Αν η λίστα δεν περιέχει παίκτες και πέρασε τον προηγούμενο έλεγχο, 
        # ο χρήστης ζήτησε να εισάγει στη θέση 1 τον παίκτη και δε χρειάζεται
        # κενό η κατάταξη
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        newPlayer = (Rank, Name, Surname, Wins, Loses, today_string)
        
        # Εισαγωγή στην κατάταξη είτε η λίστα έχει παίκτες, 
        # είτε δεν έχει και ο χρήστης διάλεξε θέση 1
        c.execute("INSERT INTO ranking VALUES {0};".format(newPlayer)) 
        msg.showinfo(
            master=main_window, 
            parent=positionEntryWindow, 
            title='Ειδοποίηση', 
            message=f'Ο παίκτης {Name} {Surname} τοποθετήθηκε επιτυχώς στη θέση #{Rank}.'
            )

        my_conn.commit()
        my_conn.close()


def delete_player(index):
    """
    Διαγράφει τον παίκτη στη θέση που δίνεται από το index και μετακινεί τους 
    κατώτερους παίκτες μία θέση πάνω, καλύπτοντας το κενό που δημιουργείται 
    στη ΒΔ. Ζητάει επιβεβαίωση διαγραφής κι ενημερώνει ΒΔ.
    
    
    Args:
        index (int): Θέση κατάταξης του προς διαγραφή παίκτη.
        
    Returns:
        None.
    """
    
    # Έλεγχος αν η θέση περιέχει άτομο και ενημέρωση με μήνυμα σφάλματος
    if empty_check(index): 
        msg.showerror(
            master=main_window, 
            parent=deletionDialog,
            title='Ειδοποίηση', 
            message="Δεν υπάρχει παίκτης στη θέση που προσπαθείτε να κάνετε διαγραφή."
            )
    else:
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()
        # Λήψη δεδομένων προς διαγραφή παίκτη
        playerDBData = c.execute("SELECT * FROM ranking WHERE Position = {0};".format(index)).fetchall()
        # Παράθυρο επιβεβαίωσης διαγραφής
        confirmation = msg.askyesno(
            master=main_window,
            parent=deletionDialog,
            title='Διαγραφή Παίκτη', 
            message=f'''ΠΡΟΣΟΧΉ!!!! Η διαγραφή είναι οριστική κι αμετάκλητη!
Θα χαθούν ΌΛΑ τα δεδομένα του παίκτη.
Θέλετε σίγουρα να διαγράψετε τον παίκτη {playerDBData[0][1]} {playerDBData[0][2]}; '''
            )
        # Ακύρωση διαγραφής και ενημέρωση χρήστη
        if confirmation == False:
            my_conn.commit()
            my_conn.close()
            msg.showerror(
                master=main_window, 
                parent=deletionDialog, 
                title='Ειδοποίηση', 
                message="Η διαγραφή ακυρώθηκε από τον χρήστη."
                )
            deletionEntry.delete(0,'end')
            return
        
        c.execute("DELETE FROM ranking WHERE Position={0};".format(index)) #Διαγραφή παίκτη
        c.execute("UPDATE ranking SET Position = Position - 1 WHERE Position > {0};".format(index)) #Ανανέωση λίστας
        
        my_conn.commit()
        my_conn.close()
        # Μήνυμα ειδοποίησης επιτυχούς διαγραφής
        msg.showinfo(
            master=main_window, 
            parent=deletionDialog, 
            title='Ειδοποίηση', 
            message=f'Ο παίκτης στη θέση #{index} διαγράφηκε επιτυχώς.'
            )
        deletionEntry.delete(0,'end')


def win(winner_index, loser_index,today_string=today_string):
    """
    Καταγράφει τη νίκη με παραμέτρους τις θέσεις των παικτών πριν την αλλαγή της 
    κατάταξης και ανανεώνει τις νίκες και ήττες του κάθε παίκτη στη ΒΔ.
    
    Αν νικήσει ο παίκτης χαμηλότερης θέσης (που κάνει την πρόκληση),
    παίρνει τη θέση του νικημένου (παίκτη που δέχθηκε την πρόκληση). Ο ηττημένος
    και όλοι οι παίκτες μεταξύ των δύο θέσεων θα μετακινηθούν μία θέση κάτω.
    
    Αν νικήσει ο παίκτης υψηλότερης θέσης (που δέχθηκε την πρόκληση), δεν 
    προκαλείται αλλαγή στην κατάταξη, μόνο ενημέρωση νικών και ηττών.
    
    Ο χρήστης ενημερώνεται με κατάλληλο μήνυμα.
    
    
    Args:
        winner_index (int): Θέση του παίκτη που νίκησε τον αγώνα.
        loser_index (int): Θέση του παίκτη που έχασε τον αγώνα.
        today_string (str): Ημερομηνία αγώνα. Προεπιλεγμένη
        τιμή η σημερινή ημέρα σε μορφή "{ημέρα}/{μήνας}/{έτος}".
        
    Returns:
        None.
    """
    
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # +1 Wins σε νικητή και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute("UPDATE ranking SET Wins = Wins + 1, Control_Date = '{0}' WHERE Position = {1};".format(today_string, 
                                                                                                      winner_index))
    # +1 Loses σε ηττημένο και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute("UPDATE ranking SET Loses = Loses + 1, Control_Date = '{0}' WHERE Position = {1};".format(today_string, 
                                                                                                        loser_index))

    # Έλεγχος για την περίπτωση που η νίκη προκαλεί αλλαγή στην κατάταξη
    if loser_index < winner_index:
        # Προσωρινή αποθήκευση νικητή
        sql_query = "SELECT * FROM Ranking WHERE Position={0};".format(winner_index)
        x = c.execute(sql_query)

        # Επιστρέφει λίστα, με το playerDBData[0] να είναι πλειάδα στοιχείων 
        # του νικητή        
        winnerDBData = x.fetchall() 
        # Διαγραφή νικητή από προηγούμενη θέση
        c.execute("DELETE FROM ranking WHERE Position={0};".format(winner_index)) 
        # Νέα πλειάδα για αλλαγή θέσης στην κατάταξη
        entryData = (
            loser_index, 
            winnerDBData[0][1], 
            winnerDBData[0][2], 
            winnerDBData[0][3], 
            winnerDBData[0][4], 
            winnerDBData[0][5]
            ) 
        
        my_conn.commit()
        my_conn.close()

        # Κλήση συνάρτησης ανακατάταξης που κατεβάζει τους παίκτες κατά μία 
        # θέση από την winner_index μέχρι ΚΑΙ τη loser_index
        update_positions(loser_index, winner_index) 

        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        # Εισαγωγή νικητή στη θέση ηττημένου
        c.execute("INSERT INTO ranking(Position, Name, Surname, Wins, Loses, Control_Date) VALUES {0};".format(entryData))
        # Ενημέρωση χρήστη για αλλαγές στην κατάταξη
        msg.showinfo(
            master=main_window,
            parent=challengeDialog, 
            title='Ειδοποίηση', 
            message='Το παιχνίδι καταγράφηκε επιτυχώς και η κατάταξη ανανεώθηκε!'
            )
    # Η νίκη δεν προκαλεί αλλαγές στις θέσεις, μόνο σε νίκες και ήττες
    else:
        msg.showinfo(
            master=main_window,
            parent=challengeDialog,
            title='Ειδοποίηση', 
            message='Το παιχνίδι καταγράφηκε επιτυχώς, χωρίς αλλαγή στην κατάταξη!'
            )
    challengeDialog.destroy()
    my_conn.commit()
    my_conn.close()
    

def update_positions(small_num, big_num):
    """
    Βοηθητική συνάρτηση για αλλαγή θέσεων σε καταγραφή νίκης ή ένταξη παίκτη σε
    συγκεκριμένη θέση, με ενημέρωση ΒΔ. 
    
    Μετακινεί όλες τις θέσεις κατά μία κάτω αρχίζοντας από το 
    big_num θέτοντάς τον παίκτη στη θέση big_num + 1 μέχρι ΚΑΙ το small_num -->
    small_num + 1. Αφήνει δηλαδή κενή την small_num για εισαγωγή παίκτη εκεί.
    Προεπιλογή big_num (αν δεν υπάρχει κενό) πρέπει να είναι η τελευταία θέση.
    
    
    Args:
        small_num (int): Θέση που θέλουμε να αδειάσει για εισαγωγή παίκτη εκεί.
        big_num (int): Τελευταίος παίκτης που κατεβαίνει θέση.
        
    Returns:
        None.
    """
    
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    

    # Πρώτα το big_num entry γίνεται big_num + 1 για να μην έχουμε σύγκρουση 
    # Primal Keys, και συνεχίζει προς το small num
    for p in range(big_num, small_num-1, -1): 
            # Το p είναι μετρητής τρέχουσας θέσης για το WHERE και 
            # μειώνεται σε κάθε loop, και το p+1 νέα θέση που θα λάβει
            c.execute('UPDATE ranking SET Position = {0} WHERE Position={1}'.format(p+1, p)) 

    my_conn.commit()
    my_conn.close()


def rank_decay(index,today_string=today_string):
    """
    Ο παίκτης της θέσης index πέφτει μία θέση λόγω αδράνειας και ο επόμενος
    παίκτης ανεβαίνει στη θέση του και η ΒΔ ενημερώνεται.
    
    
    Args:
        index (int): Θέση του παίκτη που πέφτει μία θέση.
        today_string (str): Ημέρα τελευταίας δραστηριότητας. Προεπιλεγμένη μέρα
        η σημερινή ως ημέρα πτώσης λόγω αδράνειας σε μορφή "{ημέρα}/{μήνας}/{έτος}".
        
    Returns:
        None.
    """
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    x = c.execute("SELECT * FROM ranking WHERE Position={0};".format(index))
    # Προσωρινή αποθήκευση στοιχείων του παίκτη 
    # που υπόκειται σε πτώση λόγω αδράνειας.
    inactive_player = x.fetchall() 
    # Διαγραφή του παίκτη
    c.execute("DELETE FROM ranking WHERE Position={0};".format(index)) 
    # Μετακίνηση του κάτω παίκτη στην πλέον κενή θέση 
    # του παίκτη που υπέστη πτώση λόγω αδράνειας
    c.execute("UPDATE ranking SET Position = {0} WHERE Position={1};".format(index,index+1)) 
    # Η μεταβλητή entry λαμβάνει τα στοιχεία του παίκτη που υπέστη
    # πτώση λόγω αδράνειας, με την θέση +1 από ό,τι ήταν, και ημερομηνία
    # τελευταίας δραστηριότητας τη σημερινή, για να μην ξαναϋποστεί
    # πτώση π.χ. αύριο
    entry = (
        inactive_player[0][0]+1, 
        inactive_player[0][1], 
        inactive_player[0][2], 
        inactive_player[0][3],
        inactive_player[0][4], 
        today_string
        )
    # Εισαγωγή παίκτη που έπεσε στην πλέον κενή θέση του από κάτω παικτή
    c.execute("INSERT INTO ranking VALUES {0};".format(entry)) 

    my_conn.commit()
    my_conn.close()


def empty_check(index):
    """
    Βοηθητική συνάρτηση που ελέγχει αν ο πίνακας έχει παίκτη στη θέση που 
    ελέγχεται.
    
    
    Args:
        index (int): Θέση που ελέγχεται για το αν περιέχει στοιχεία παίκτη.
        
    Returns:
        boolean: True αν η θέση είναι κενή.
    """
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    
    c.execute("SELECT Position FROM ranking WHERE Position={0};".format(index))
    # Πλειάδα με νούμερο για θέση ή κενή αν δεν υπάρχει παίκτης
    empty_check = c.fetchall() 
    flag = len(empty_check) == 0
    
    my_conn.close()
    return flag
    

def check_ranking_for_decay(today=today):
    """Ελέγχει αν υπάρχουν παίκτες που υπόκεινται σε decay στην κατάταξη λόγω
    αδράνειας. Ως αδράνεια ορίζεται ημέρα τελευταίας δραστηριότητας μεγαλύτερη
    των 30 ημερών.
    
    
    Args:
        today (datetime object): Προεπιλεγμένη τιμή η σημερινή ημερομηνία 
        για σύγκριση με το παρόν.
            
    Returns:
        None.
    """
    conn = dbconnect('tennis_club.db')
    cursor = conn.cursor()

    # Λίστα με παίκτες που θα υποστούν πτώση λόγω αδράνειας
    decaylist = [] 
    cursor.execute("SELECT Position, Control_Date FROM ranking;")
    ranking = cursor.fetchall()
    
    for index, date in ranking:
        # Διαχωρίζει το string της ημερομηνίας
        split_date = date.split(sep='/') 
        # Μετατροπή του string σε datetime object για σύγκριση
        last_play_date = datetime.date(int(split_date[2]),int(split_date[1]),int(split_date[0]))
        days_since_last_play = (today - last_play_date).days
        if days_since_last_play > 30:
            # Έλεγχος για την περίπτωση που ο παίκτης είναι τελευταίος και δεν
            # πέφτει περαιτέρω θέση
            if ranking[-1][0] == index: 
                cursor.execute("SELECT Name, Surname FROM ranking WHERE Position={0};".format(index))
                last_player = cursor.fetchone()
                # Μήνυμα ειδοποίησης χρήστη πως ο παίκτης δεν πέφτει περαιτέρω
                msg.showinfo(
                    master=main_window, 
                    title='Ειδοποίηση', 
                    message="Ο παικτης {0} {1} είναι ήδη στην τελευταία θέση και δεν πέφτει περαιτέρω.".format(
                        last_player[0], 
                        last_player[1]
                        )
                    )
                cursor.execute("UPDATE ranking SET Control_Date='{0}' WHERE Position={1};".format(today_string, index))
                break
            # Προστίθεται στη λίστα, η αλλαγή δεν γίνεται εδώ γιατί οδηγεί σε logical error του περάσματος for
            decaylist.append(index) 
    
    conn.commit()
    conn.close()    
    
    # Έλεγχος αν η λίστα είναι κενή
    if decaylist: 
        decay_positions = ','.join([str(single_decay_position) for single_decay_position in decaylist])
        decay_message = ''.join(['Οι παίκτες στις θέσεις ', decay_positions, ' έπεσαν μία θέση λόγω αδράνειας και η κατάταξη ανανεώθηκε.'])
        msg.showinfo(
            master=main_window, 
            title='Ειδοποίηση', 
            message=decay_message
            )
        # Αντίστροφο πέρασμα της λίστας για αποφυγή λαθών από την αλλαγή θέσης
        for i in decaylist[::-1]: 
            rank_decay(i)            
    
    # Η λίστα αδρανών παικτών είναι κενή
    else:
        msg.showinfo(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Δεν υπάρχει κανένας παίκτης που να υπόκειται σε μείωση θέσης λόγω αδράνειας."
            )



def initializeBTNpushed():
    """
    Συνάρτηση κουμπιού Αρχικοποίησης Κατάταξης. Ελέγχει αν υπάρχει ήδη κατάταξη
    και ενημερώνει τον χρήστη για αδυναμία αρχικοποίησης αν υπάρχει.
    Δημιουργεί παράθυρο διαλόγου για εισαγωγή ονομάτων παικτών που θα 
    χρησιμοποιηθούν για την τυχαία αρχικοποίηση κατάταξης.
    """ 
    # Έλεγχος για το αν ο πίνακας περιέχει παίκτες        
    if not empty_check(1): 
        # Αν περιέχει παίκτες, η τυχαία αρχικοποίηση δεν είναι διαθέσιμη
        # και ο χρήστης ενημερώνεται με το ανάλογο μήνυμα λάθους
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message='''Ο πίνακας κατάταξης περιέχει ήδη παίκτες και δεν μπορεί να αρχικοποιηθεί τυχαία. 
Παρακαλώ, διαγράψτε όλους τους παίκτες ή προσθέστε παίκτες χρησιμοποιώντας κάποια από τις επιλογές.'''
            )
        return
    
    # Μεταβλητή για αποθήκευση παικτών προς αρχικοποίηση
    global players
    players = []
    # Δυναμική μεταβλητή StringVar για προβολή εισαχθέντων 
    # παικτών καθώς αυτοί εισάγονται
    global initializationList
    initializationList = tk.StringVar()
    initializationList.set('Κενή Λίστα Παικτών')
    
    # Παράθυρο διαλόγου αρχικοποίησης
    global dialogInitialize
    dialogInitialize = tk.Toplevel(main_window)
    dialogInitialize.title('Αρχικοποίηση λίστας')
    dialogInitialize.geometry('400x500+700+350')
    # Keybind για κλείσιμο παραθύρου με Escape
    dialogInitialize.bind(
        "<Escape>", 
        lambda event: dialogInitialize.destroy()
        )
    
    # Πεδίο εισαγωγής
    global initializationEntry
    initializationEntry = tk.Entry(
        dialogInitialize,
        justify='center', 
        font='Times 16',
        selectborderwidth=3
        )
    initializationEntry.pack(pady=10)
    initializationEntry.focus_set()
    # Keybind για καταχώρηση παίκτη στη λίστα με Enter
    initializationEntry.bind(
        "<Return>", 
        lambda event: dialogInitialize_AddPlayerBTNPushed()
        )
    # Κουμπί καταχώρησης παίκτη στη λίστα
    tk.Button(
        dialogInitialize, 
        text="Καταχώρηση Παίκτη", 
        font='Times 16', 
        command = dialogInitialize_AddPlayerBTNPushed
        ).pack(pady=5)
    # Κουμπί τέλους καταχωρήσεων και αρχικοποίησης κατάταξης
    tk.Button(
        dialogInitialize,
        text="Τέλος Καταχωρήσεων",
        font = 'Times 16', 
        command = dialogInitialize_EntryEndBTNPushed
        ).pack(pady=5)
    ttk.Separator(
        dialogInitialize,
        orient='horizontal'
        ).pack(fill='x',pady=15)
    # Δυναμικό Label που αλλάζει με τις καταχωρήσεις
    tk.Label(
        dialogInitialize, 
        textvariable = initializationList,
        font = 'Times 16',
        justify='center'
        ).pack()     
    dialogInitialize.mainloop()
    

def dialogInitialize_AddPlayerBTNPushed():
    """
    Συνάρτηση κουμπιού καταχώρησης παίκτη στο παράθυρο διαλόγου αρχικοποίησης.
    Ελέγχει το όνομα που εισήχθη, ενημερώνει σε περίπτωση λάθους, ανανεώνει 
    δυναμική λίστα για παρουσίαση παικτών που έχουν ήδη εισαχθεί για αρχικοποίηση.
    """
    name = initializationEntry.get()
    initializationEntry.delete(0,'end')
    player = name.split(sep=' ')
    
    # Περίπτωση που εισαχθούν πάνω απο 1 κενά
    if len(player) != 2: 
        msg.showerror(
            master=dialogInitialize, 
            parent=dialogInitialize,  
            title='Ειδοποίηση', 
            message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό."
            )
        return
    # Προσθήκη παίκτη στη λίστα
    players.append(player)
    global initializationList
    # Ελέγχει αν το δυναμικό Label έδειχνε κενή λίστα και απαιτεί πρώτη
    # μορφοποίηση κι όχι απλά προσθήκη παίκτη σε αυτήν
    if initializationList.get() == 'Κενή Λίστα Παικτών':
        initializationList.set("Λίστα Παικτών\n")
    # Παίρνει τα δεδομένα που είχε το δυναμικό Label 
    # για να προσθέσει το νέο δεδομένο
    string = '\n'.join([initializationList.get(),name])
    # Προσθήκη νέου παίκτη
    initializationList.set(string)
    initializationEntry.focus_set()
    return

def dialogInitialize_EntryEndBTNPushed():
    """
    Συνάρτηση κουμπιού τέλους καταχωρήσεων στο παράθυρο διαλόγου αρχικοποίησης.
    Ελέγχει αν έχει εισαχθεί παίκτης στη λίστα. Αν δεν έχει εισαχθεί έστω ένας, 
    ενημερώνει με το κατάλληλο μήνυμα. Σε αντίθετη περίπτωση, προχωράει στην
    αρχικοποιήση της κατάταξης με τη λίστα παικτών που δόθηκε.
    """
    # Ελέγχει αν η λίστα players είναι κενή
    if players:
        initialization(players)
        dialogInitialize.destroy()
        return
    
    else: 
        dialogInitialize.destroy()
        # Σε περίπτωση που ήταν κενή ενημερώνει τον χρήστη με το κατάλληλο μήνυμα
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message='Δε δημιουργήθηκε κατάταξη καθώς δεν εισάγατε ονόματα.'
            )
        return

def addPlayerBTNpushed():
    """
    Συνάρτηση κουμπιού προσθήκης παίκτης στο αρχικό παράθυρο. Ρωτάει τον χρήστη
    αν ο παίκτης θα εισαχθεί στο τέλος της κατάταξης ή σε συγκεκριμένη θέση,
    δημιουργεί παράθυρο διαλόγου για εισαγωγή ονοματεπωνύμου παίκτη.
    """
    # Ερώτηση εισαγωγής παίκτη σε συγκεκριμένη θέση
    global answerAddition
    answerAddition = msg.askyesnocancel(
        title='Προσθήκη Παίκτη',
        message='''Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση;'''
        )
    if answerAddition == None:
        msg.showinfo(
            master=main_window, 
            title='Ειδοποίηση', 
            message='Η προσθήκη παίκτη ακυρώθηκε.'
            )
        return
            
    # Παράθυρο διαλόγου εισαγωγής ονοματεπωνύμου παίκτη
    global nameEntryWindow
    nameEntryWindow = tk.Toplevel(main_window)
    nameEntryWindow.geometry("550x150+650+350")
    nameEntryWindow.title('Προσθήκη Παίκτη')
    nameEntryWindow.bind(
        "<Escape>", 
        lambda event: nameEntryWindow.destroy()
        )
    tk.Label(
        nameEntryWindow, 
        font=defaultFont, 
        text = "Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε: "
        ).pack(pady=5)
    # Πεδίο εισαγωγής
    global nameEntered
    nameEntered = tk.Entry(
        nameEntryWindow, 
        font=defaultFont, 
        justify='center'
        )
    nameEntered.pack(pady=5)
    nameEntered.focus_set()
    nameEntered.bind(
        "<Return>", 
        lambda event: addPlayerDialog_nameEntryBTNpushed()
        )
    # Κουμπί εισαγωγής ονοματεπωνύμου παίκτη
    tk.Button(
        nameEntryWindow, 
        text='Προσθήκη', 
        font=defaultFont, 
        command=addPlayerDialog_nameEntryBTNpushed
        ).pack(pady=5)
    

def addPlayerDialog_nameEntryBTNpushed():
    """
    Συνάρτηση για το κουμπί διαλόγου εισαγωγής παίκτη. Ελέγχει αν το όνομα και το
    επίθετο δόθηκαν σε αποδεκτή μορφή και ενημερώνει τον χρήστη. 
    
    Αν ο χρήστης απάντησε πως δε θέλει να βάλει τον παίκτη σε συγκεκριμένη θέση,
    βάζει τον παίκτη στην τελευταία θέση της ΒΔ με κλήση της insert_bottom().
    
    Αν ο χρήστης απάντησε πως θέλει να βάλει τον παίκτη σε συγκεκριμένη θέση, 
    ζητάει τη θέση με νέο παράθυρο διαλόγου.
    """
    playerNameEntered = nameEntered.get()
    nameEntered.delete(0,'end')
    global playerAdded
    playerAdded = playerNameEntered.split(sep=' ')
    # Έλεγχος σωστής εισαγωγής ονοματεπωνύμου
    if len(playerAdded) != 2: 
        # Ενημέρωση χρήστη με κατάλληλο μήνυμα
        msg.showerror(
            master=main_window, 
            parent=nameEntered, 
            title='Ειδοποίηση', 
            message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό."
            )
        return
    name, surname = playerAdded[0], playerAdded[1]
    # Αν ο χρήστης απάντησε πως δε θέλει να βάλει σε συγκεκριμένη θέση
    # τον παίκτη, μπαίνει στην τελευταία θέση
    if answerAddition == False:
        insert_bottom(name,surname)
        nameEntryWindow.destroy()
    # Αν ο χρήστης απάντησε πως θέλει να βάλει σε συγκεκριμένη θέση τον παίκτη
    elif answerAddition == True:
        # Δημιουργία παραθύρου διαλόγου
        global positionEntryWindow
        positionEntryWindow = tk.Toplevel(nameEntryWindow)
        positionEntryWindow.geometry("600x150+625+450")
        positionEntryWindow.title("Προσθήκη Παίκτη σε Θέση")
        positionEntryWindow.bind(
            "<Escape>", 
            lambda event: positionEntryWindow.destroy()
            )
        
        tk.Label(
            positionEntryWindow, 
            font=defaultFont, 
            text='Δώστε τη θέση κατάταξης του παίκτη που θέλετε να προσθέσετε: '
            ).pack(pady=5)
        # Πεδίο εισαγωγής
        global positionEntry
        positionEntry = tk.Entry(
            positionEntryWindow, 
            font=defaultFont, 
            justify='center'
            )
        positionEntry.pack(pady=5)
        positionEntry.focus_set()
        positionEntry.bind(
            "<Return>", 
            lambda event: addPlayerDialog_positionEntryBTNpushed()
            )
        # Κουμπί καταχώρησης θέσης εισαγωγής παίκτη προς προσθήκη
        tk.Button(
            positionEntryWindow, 
            font=defaultFont, 
            text='OK',
            command=addPlayerDialog_positionEntryBTNpushed
            ).pack(pady=5)
        
    return

def addPlayerDialog_positionEntryBTNpushed():
    """
    Συνάρτηση κουμπιού εισαγωγής θέσης για το παράθυρο διαλόγου προσθήκης παίκτη
    σε συγκεκριμένη θέση.
    Ελέγχει αν η εισαγωγή είναι σωστή και ανανεώνει τη ΒΔ καλώντας την 
    insert_place() ή ενημερώνει τον χρήστη με μήνυμα σφάλματος.
    """
    
    # Try block για εισαγωγή μη ακεραίου αριθμού.
    # Ο αμυντικός προγραμματισμός για εισαγωγή αποδεκτής τιμής 
    # γίνεται μέσω της insert_place
    try:
        positionEntered = int(positionEntry.get())
        positionEntry.delete(0,'end')
        name,surname = playerAdded[0], playerAdded[1]
        insert_place(positionEntered,name,surname)
        positionEntryWindow.destroy()
        nameEntryWindow.destroy()
    except ValueError:
        # Ενημέρωση χρήστη για μη αποδεκτή εισαγωγή θέση (όχι ακέραιος)
        msg.showerror(
            master=positionEntryWindow, 
            parent=positionEntryWindow, 
            title='Ειδοποίηση', 
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης."
            )
    return
    

def delPlayerBTNpushed():
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για διαγραφή παίκτη.
    Ελέγχει αν η κατάταξη περιέχει έστω έναν παίκτη και δημιουργεί παράθυρο 
    διαλόγου για εισαγωγή θέσης κατάταξης του παίκτη που θα διαγραφεί ή ενημερώνει
    τον χρήστη με το ανάλογο μήνυμα σφάλματος.
    """
    # Ελέγχει αν η κατάταξη περιέχει έστω έναν παίκτη
    if empty_check(1):
        # Ειδοποίηση χρήστη με το κατάλληλο μήνυμα
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    # Η κατάταξη περιέχει παίκτες
    else:
        # Δημιουργία παραθύρου διαλόγου
        global deletionDialog
        deletionDialog = tk.Toplevel(main_window)
        deletionDialog.geometry("550x200+650+450")
        deletionDialog.title('Διαγραφή Παίκτη')
        deletionDialog.bind(
            "<Escape>", 
            lambda event: deletionDialog.destroy()
            )
        tk.Label(
            deletionDialog, 
            text='Δώστε τη θέση κατάταξης του παίκτη που θέλετε να διαγράψετε: ', 
            font = 'Times 14'
            ).pack(pady=20)
        # Πεδίο εισαγωγής
        global deletionEntry
        deletionEntry = tk.Entry(
            deletionDialog,
            justify = 'center', 
            font=defaultFont
            )
        deletionEntry.pack(pady=5)
        deletionEntry.focus_set()
        deletionEntry.bind(
            "<Return>", 
            lambda event: deletionDialog_deleteBTNPushed()
            )
        # Κουμπί διαγραφής
        tk.Button(
            deletionDialog, 
            text='Διαγραφή', 
            font='Times 16', 
            command=deletionDialog_deleteBTNPushed
            ).pack(side='left',padx=60)
        deletionDialog.bind(
            "<Escape>", 
            lambda event: deletionDialog.destroy() 
            )
        # Κουμπί ακύρωσης διαγραφής
        tk.Button(
            deletionDialog, 
            text='Ακύρωση', 
            font='Times 16', 
            command=deletionDialog.destroy
            ).pack(side='right',padx=60)
        
        deletionDialog.mainloop()
        

def deletionDialog_deleteBTNPushed():
    """
    Συνάρτηση για το κουμπί διαγραφής του παραθύρου διαλόγου διαγραφής παίκτη.
    Ελέγχει ότι ο χρήστης εισάγει ακέραιο αριθμό για τη θέση κατάταξης ή 
    ειδοποιεί με το κατάλληλο μήνυμα σφάλματος. Ενημερώνει τη ΒΔ καλώντας την
    delete_player().
    """
    # Ελέγχει πως ο χρήστης εισήγαγε ακέραιο αριθμό
    # Ο έλεγχος αποδεκτής τιμής γίνεται από την delete_player()
    try:
        index = int(deletionEntry.get())
        delete_player(index)
    except ValueError:
        # Ειδοποίηση χρήστη για λάθος εισαγωγή θέσης
        msg.showerror(
            master=main_window, 
            parent=deletionDialog, 
            title='Ειδοποίηση', 
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης."
            )
        deletionEntry.delete(0,'end')
    return

def challengeBTNpushed():
    """
    Συνάρτηση κουμπιού καταγραφής αγώνα του κυρίου παραθύρου. 
    
    Ελέγχει αν η κατάταξη περιέχει 0 ή μόνο 1 παίκτες και ενημερώνει τον χρήστη
    με το κατάλληλο μήνυμα σφάλματος.
    
    Δημιουργεί παράθυρο διαλόγου για καταγραφή της θέσης του παίκτη που θέτει
    την πρόκληση.
    """
    # Έλεγχος αν η κατάταξη περιέχει έναν ή κανέναν παίκτη και δεν ορίζεται αγώνας
    if empty_check(1):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    elif empty_check(2):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη περιέχει μόνο έναν παίκτη άρα δεν ορίζεται πρόκληση."
            )
    # Περιέχει πάνω από 1 παίκτη
    else:
        # Δημιουργία παραθύρου διαλόγου για την πρόκληση
        global challengeDialog
        challengeDialog = tk.Toplevel(main_window)
        challengeDialog.geometry("650x200+650+450")
        challengeDialog.title("Καταγραφη Πρόκλησης")
        challengeDialog.bind(
            "<Escape>", 
            lambda event: challengeDialog.destroy()
            )
        # Τίθεται ως δυναμικό Label για να αλλάζει 
        # μετά την καταχώρηση του πρώτου παίκτη
        global challengeLabel
        challengeLabel = tk.StringVar()
        challengeLabel.set('Δώστε τη θέση κατάταξης του παίκτη που προκαλεί: ')
        tk.Label(
            master=challengeDialog, 
            textvariable= challengeLabel, 
            font=defaultFont
            ).pack(pady = 10)
        # Πεδίο εισαγωγής
        global challengeEntry
        challengeEntry = tk.Entry(
            master=challengeDialog, 
            justify='center', 
            font=defaultFont
            )
        challengeEntry.pack(pady = 10)
        challengeEntry.focus_set()
        challengeEntry.bind(
            "<Return>", 
            lambda event: challengeDialog_challengeBTNPushed()
            )
        # Κουμπί καταχώρησης θέσης παίκτη που εμπλέκεται στην πρόκληση
        tk.Button(
            master=challengeDialog, 
            text='OK', 
            font = defaultFont, 
            command=challengeDialog_challengeBTNPushed
            ).pack(pady = 10)
        # Μεταβλητή που αποθηκεύει τις θέσεις των παικτών
        # που εμπλέκονται στην πρόκληση
        global players_in_challenge
        players_in_challenge = []
        challengeDialog.mainloop()


def challengeDialog_challengeBTNPushed():
    """
    Συνάρτηση κουμπιού καταχώρησης θέσης παίκτη που συμμετέχει στην πρόκληση. 
    
    Όταν πατιέται για τον πρώτο παίκτη το κουμπί, η συνάρτηση ελέγχει αν η 
    εισαγωγή είναι σωστή (ακέραιος) και αν υπάρχει παίκτης στη θέση. 
    Έπειτα, αλλάζει το μήνυμα του παραθύρου διαλόγου για να ζητήσει τη θέση του 
    παίκτη που δέχεται την πρόκληση.
    
    Όταν πατιέται το κουμπί δεύτερη φορά, αφότου δηλαδή έχει καταχωρηθεί ο 
    πρώτος παίκτης, ελέγχεται και πάλι η τιμή και καλεί την challenge() που 
    ελέγχει την πρόκληση σύμφωνα με τους κανόνες και ενημερώνει τη ΒΔ ή 
    ενημερώνει τον χρήστη με το κατάλληλο μήνυμα σφάλματος.
    """
    # Έλεγχοι εισαγωγής για valid θέση και για εισαγωγή ακεραίου.
    try:
        # Ελέγχει πως η θέση που εισήχθη περιέχει παίκτη ή ενημερώνει με
        # το ανάλογο μήνυμα σφάλματος
        if empty_check(int(challengeEntry.get())):
            msg.showerror(
                master=main_window, 
                parent=challengeDialog, 
                title='Ειδοποίηση', 
                message=f"Δεν υπάρχει παίκτης στη θέση #{challengeEntry.get()}"
                )
            return
        # Προσθήκη εισαχθείσας θέσεις στη λίστα παικτών που εμπλέκονται
        players_in_challenge.append(int(challengeEntry.get()))
        challengeEntry.delete(0,'end')
    except ValueError:
        # Ενημέρωση χρήστη για εισαγωγή μη ακεραίου
        # Ο έλεγχος των τιμών της πρόκλησης γίνεται από το try block και
        # από την challenge()
        msg.showerror(
            master=main_window, 
            parent=challengeDialog, 
            title='Ειδοποίηση', 
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης."
            )
        return
    # Εάν έχει λάβει μόνο έναν παίκτη, ενημερώνει το δυναμικό Label
    if len(players_in_challenge) == 1:
        challengeLabel.set('Δώστε τη θέση κατάταξης του παίκτη που δέχεται την πρόκληση:')
    # Εάν έχει λάβει 2 παίκτες, καλεί την challenge()
    elif len(players_in_challenge) == 2:
        challenge(players_in_challenge[0],players_in_challenge[1])
        challengeDialog.destroy()
        
    return


def inactivePlayerCheckBTNpushed():
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για έλεγχο για αδρανείς παίκτες.
    Ελέγχει αν η κατάταξη περιέχει παίκτες και καλεί την 
    check_ranking_for_decay() ή ενημερώνει με μήνυμα λάθους.
    
    Η check_ranking_for_decay() θα ενημερώσει τη ΒΔ αναλόγως με το αν υπάρχουν
    αδρανείς παίκτες.
    """
    # Ελέγχει πως η κατάταξη δεν είναι κενή ή ειδοποιεί με το κατάλληλο μήνυμα
    if empty_check(1):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    else:
        check_ranking_for_decay()

def showRankingBTNpushed():
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για εμφάνιση της κατάταξης.
    
    Ελέγχει αν η κατάταξη περιέχει παίκτες και δημιουργεί ένα παράθυρο με τον
    πίνακα κατάταξης που γεμίζεται από την print_() ή ενημερώνει τον χρήστη
    με μήνυμα σφάλματος περί άδειας κατάταξης.
    """
    # Ελέγχει πως η κατάταξη δεν είναι κενή ή ειδοποιεί με το κατάλληλο μήνυμα
    if empty_check(1):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    else:
        # Δημιουργεί παράθυρο με tree για προβολή κατάταξης
        ranking_table = tk.Toplevel(main_window)
        ranking_table.title("Πίνακας Κατάταξης")
        ranking_table.geometry("1000x800+350+0")
        ranking_table.bind(
            "<Escape>", 
            lambda event: ranking_table.destroy()
            )
        style = ttk.Style()
        style.configure("mystyle.Treeview",font=('Times',16),rowheight=30)
        # Δημιουργία Treeview με τις απαιτούμενες στύλες και μορφοποιήσεις
        global tree
        tree = ttk.Treeview(
            ranking_table, 
            style="mystyle.Treeview", 
            columns=(
                'Θέση', 
                'Όνομα', 
                'Επίθετο', 
                'Νίκες', 
                'Ήττες'
                ),
            show='headings'
            )
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
        # Καλεί την fill_tree() να γεμίσει το tree με τα δεδομένα της ΒΔ
        fill_tree()
        tree.pack(fill='both',expand=1)
        ranking_table.focus_set()
        ranking_table.mainloop()
        return
    
def exitBTNpushed():
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για έξοδο.
    
    Τερματίζει τη λειτουργία της εφαρμογής και κλείνει το κύριο παράθυρο.
    """
    main_window.destroy()


if __name__ == '__main__':
    # Δημιουργία κύριου παραθύρου
    main_window = tk.Tk()
    main_window.geometry('600x600+650+150')
    main_window.title("Tennis Ladder App")
    defaultFont = 'Times 16'
    # Κουμπί αρχικοποίησης
    initializeBTN = tk.Button(
        main_window, 
        text = 'Αρχικοποίηση κατάταξης', 
        font = defaultFont, 
        command = initializeBTNpushed, 
        relief='groove', bd=10
        )
    # Κουμπί προσθήκης παίκτη
    addPlayerBTN = tk.Button(
        main_window, 
        text = 'Προσθήκη παίκτη', 
        font = defaultFont, 
        command = addPlayerBTNpushed,
        relief='groove', bd=10
        )
    # Κουμπί διαγραφής παίκτη
    delPlayerBTN = tk.Button(
        main_window, 
        text = 'Διαγραφή παίκτη', 
        font = defaultFont, 
        command = delPlayerBTNpushed, 
        relief='groove', bd=10
        )
    # Κουμπί ελέγχου και καταγραφής αγώνα
    challengeBTN = tk.Button(
        main_window, 
        text = 'Έλεγχος και καταγραφή αποτελέσματος πρόκλησης', 
        font = defaultFont, 
        command = challengeBTNpushed, 
        relief='groove',
        bd=10
        )
    # Κουμπί ελέγχου για αδρανείς παίκτες
    inactivePlayerCheckBTN = tk.Button(
        main_window, 
        text = 'Έλεγχος κατάταξης για αδρανείς παίκτες', 
        font = defaultFont, 
        command = inactivePlayerCheckBTNpushed,
        relief='groove', 
        bd=10
        )
    # Κουμπί εμφάνισης κατάταξης
    showRankingBTN = tk.Button(
        main_window, 
        text = 'Εμφάνιση κατάταξης', 
        font = defaultFont, 
        command = showRankingBTNpushed, 
        relief='groove', 
        bd=10
        )
    # Κουμπί εξόδου από το πρόγραμμα
    exitBTN = tk.Button(
        main_window, 
        text = 'Έξοδος',
        font = defaultFont, 
        command = exitBTNpushed, 
        relief='groove', 
        bd=10
        )
    
    ttk.Separator(
        main_window,
        orient='horizontal'
        ).pack(
            fill='x',
            pady=15
            )
    initializeBTN.pack(
        fill='x', 
        padx=50, 
        pady=10
        )
    addPlayerBTN.pack(
        fill='x', 
        padx=50, 
        pady=10
        )
    delPlayerBTN.pack(
        fill='x', 
        padx=50,
        pady=10
        )
    challengeBTN.pack(
        fill='x', 
        padx=50, 
        pady=10
        )
    inactivePlayerCheckBTN.pack(
        fill='x', 
        padx=50, 
        pady=10
        )
    showRankingBTN.pack(
        fill='x', 
        padx=50, 
        pady=10
        )
    exitBTN.pack(
        fill='x',
        padx=50, 
        pady=10
        )
    tk.Label(
        main_window, 
        text='Made by Black Baron', 
        font = (
            'Old English Text MT',
            12
            ),
        justify='left'
        ).pack(side='right')
    create_table()
    main_window.mainloop()
    

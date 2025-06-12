import tkinter as tk
from tkinter import ttk, messagebox as msg, PhotoImage
import sqlite3
from sqlite3 import Error
import datetime
import random


def initialization(initialization_players):
    """
    Συνάρτηση αρχικοποίησης κατάταξης. Δέχεται λίστα με όνομα και επίθετο 
    χωρισμένα με κενό και την εκχωρεί στον πίνακα της ΒΔ με ανακατεμένη σειρά.
    
    
    Args:
        initialization_players (list): Λίστα με στοιχεία str όνομα και επίθετο.
        
    Returns:
        None.
    """
    
    today_string = grab_date()
    # Τυχαιοποίηση σειράς παικτών
    random.shuffle(initialization_players)
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    
    # Εισαγωγή παικτών στη ΒΔ με τυχαία σειρά
    for i,player in enumerate(initialization_players):
        # Το i είναι το index + 1 για να ξεκινάει από τη θέση 1
        # Όνομα, επώνυμο, νίκες, ήττες, ημερομηνία δραστηριότητας
        entry = (
            i + 1, 
            initialization_players[i][0], 
            initialization_players[i][1], 
            0, 
            0, 
            today_string
            )
        c.execute("INSERT INTO ranking VALUES (?, ?, ?, ?, ?, ?)", entry)
   
    my_conn.commit()
    my_conn.close()
    return


def insert_player_at_end(name, surname, wins=0, loses=0, control_date=None):
    """
    Εισαγωγή παίκτη στο τέλος της κατάταξης, προεπιλεγμένες τιμές για Wins & 
    Loses = 0. Control_Date σήμερα ως ημέρα ένταξης. Εκχωρεί τα δεδομένα στη ΒΔ.
    
    
    Args:
        name (str): Όνομα παίκτη.
        surname (str): Επίθετο παίκτη.
        wins (int): Νίκες παίκτη. Προεπιλεγμένη τιμή 0.
        loses (int): Ήττες παίκτη. Προεπιλεγμένη τιμή 0.
        control_date (str): Ημερομηνία τελευταίας δραστηριότητας.
        Αν δεν λάβει τιμή στην κλήση, τίθεται στη σημερινή ημερομηνία.
    
    Returns:
        int: Τελευταία θέση της κατάταξης.
    """
    if control_date is None:
        control_date = grab_date()
    
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # Αν η πρώτη θέση είναι κενή δε χρειάζεται να ληφθεί το δεδομένο της 
    # τελευταίας θέσης, παίρνει τιμή 1. Καταχώρηση νέας τελευταίας θέσης
    new_last_place = 1 if is_position_empty(1) else c.execute("SELECT Position FROM ranking;").fetchall()[-1][0] + 1
    
    new_player = (
        new_last_place, 
        name, 
        surname, 
        wins, 
        loses, 
        control_date
        ) #Πλειάδα στοιχείων παίκτη
    c.execute("INSERT INTO ranking VALUES (?, ?, ?, ?, ?, ?);",new_player) #Εκχώρηση παίκτη σε αυτή τη θέση
    
    my_conn.commit()
    my_conn.close()
    return new_last_place


def insert_player_at_position(rank, name='', surname='', wins=0, loses=0, control_date=None):
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
        Control_Date (str): Ημερομηνία τελευταίας δραστηριότητας.
        Αν δεν λάβει τιμή στην κλήση, τίθεται στη σημερινή ημερομηνία.
        
    Returns:
        boolean: False αν δεν τοποθετήθηκε ο παίκτης.
    """
    
    if control_date is None:
        control_date = grab_date()
        
    # Αν προσπαθεί να βάλει τον παίκτη σε θέση πάνω από την οποία δεν υπάρχει 
    # άλλος παίκτης
    if is_position_empty(rank-1) and rank != 1: 
        return False

    else:
        # Αν η λίστα έχει παίκτες πρέπει να μετακινηθούν όλοι μία θέση κάτω
        if not is_position_empty(1): 
            my_conn = dbconnect('tennis_club.db')
            c = my_conn.cursor()

            # Λήψη τρέχουσας τελευταίας θέσης κατάταξης
            last_place = c.execute("SELECT Position FROM ranking ORDER BY Position DESC LIMIT 1;").fetchone()[0]
            my_conn.close()
            # Δημιουργείται κενό βάσει της τελευταίας θέσης και της θέσης που 
            # θα εισαχθεί ο παίκτης
            update_positions(rank, last_place) 
        
        # Αν η λίστα δεν περιέχει παίκτες και πέρασε τον προηγούμενο έλεγχο, 
        # ο χρήστης ζήτησε να εισάγει στη θέση 1 τον παίκτη και δε χρειάζεται
        # κενό η κατάταξη
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        new_player = (rank, name, surname, wins, loses, control_date)
        
        # Εισαγωγή στην κατάταξη είτε η λίστα έχει παίκτες, 
        # είτε δεν έχει και ο χρήστης διάλεξε θέση 1
        c.execute("INSERT INTO ranking VALUES (?, ?, ?, ?, ?, ?);", new_player) 
        

        my_conn.commit()
        my_conn.close()
        return True


def change_position(old_position, new_position):
    """
    Συνάρτηση που αλλάζει τη θέση παίκτη κάνοντας τις απαραίτητες αλλαγές.
    Διατηρεί προσωρινά τα δεδομένα ΒΔ του παίκτη, τον διαγράφει από τη ΒΔ,
    προσπαθεί να τον εισάγει στη νέα θέση. Σε περίπτωση αποτυχίας τον επανεισάγει
    στην προηγούμενή του θέση.
    
    
    Args:
        old_position (str): Τρέχουσα θέση παίκτη.
        new_position (str): Νέα θέση παίκτη.
        
    Returns:
        boolean: True αν η αλλαγή θέσης ήταν επιτυχής.
    """
    my_conn = dbconnect('tennis_club.db')
    cursor = my_conn.cursor()
    query = cursor.execute("SELECT * FROM ranking WHERE Position = ?;", (old_position,))
    # Προσωρινή αποθήκευση των δεδομένων του παίκτη
    player_DB_data = query.fetchall()
    my_conn.close()
    entry = list(player_DB_data[0])
    # Η νέα θέση που θα λάβει
    entry[0] = int(new_position)
    # Διαγραφή της προηγούμενης καταχώρησης
    delete_player(old_position)
    # Αν απέτυχε η τοποθέτηση του παίκτη επειδή η θέση ήταν εκτός ορίου κατάταξης
    # επανεισάγεται στη θέση που ήταν.
    if not insert_player_at_position(*entry):
        entry[0] = int(old_position)
        insert_player_at_position( *entry)
        return False
    else:
        return True


def update_info(rank, name = None, surname = None, wins = None, loses = None, control_date = None):
    """
    Συνάρτηση που ενημερώνει τα δεδομένα χρήστη πλην της θέσης.
    Τα μόνα πεδία που ανανεώνονται είναι όσα λαμβάνουν μη None value.
    Τα υπόλοιπα διατηρούν την τιμή που είχαν πριν την κλήση της συνάρτησης.
    
    Args:
        rank (int): Θέση που έχει ο παίκτης του οποίου τα στοιχεία θα ανανεωθούν.
        name (str): Default None, νέο όνομα παίκτη.
        surname (str): Default None, νέο επώνυμο παίκτη.
        wins (int): Default None, νέος αριθμός νικών παίκτη.
        loses (int): Default None, νέος αριθμός ηττών παίκτη.
        control_date (str): Default None, νέα ημερομηνία τελευταίας δραστηριότητας.
    """
    conn = dbconnect('tennis_club.db')
    cursor = conn.cursor()
    fields = [
        ('Name', name), 
        ('Surname', surname), 
        ('Wins', wins), 
        ('Loses', loses),
        ('Control_Date', control_date)
        ]
    for field_name, field_value in fields:
        if field_value is not None:
            sql_query = "UPDATE ranking SET {0} = ? WHERE Position = ?;".format(field_name)
            cursor.execute(
                sql_query,
                (field_value, rank)
                )
    conn.commit()
    conn.close()
    return


def delete_player(index):
    """
    Διαγράφει τον παίκτη στη θέση που δίνεται από το index και μετακινεί τους 
    κατώτερους παίκτες μία θέση πάνω, καλύπτοντας το κενό που δημιουργείται 
    στη ΒΔ. 
    
    
    Args:
        index (int): Θέση κατάταξης του προς διαγραφή παίκτη.
        
    Returns:
        None.
    """

    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    c.execute("DELETE FROM ranking WHERE Position=?;", (index,)) #Διαγραφή παίκτη
    c.execute("UPDATE ranking SET Position = Position - 1 WHERE Position > ?;", (index,)) #Ανανέωση λίστας
    my_conn.commit()
    my_conn.close()
    return


def fill_tree(tree):
    """
    Ενημερώνει το Treeview του UI εκχωρώντας σε αυτό τα στοιχεία όλων των παικτών.
    
    
    Args:
        tree (Treeview Object): Πίνακας στον οποίο μπαίνουν τα δεδομένα της ΒΔ.
        
    Returns:
        None.
    """
    # Διαγράφει τα δεδομένα του Treeview. 
    # Αν δεν έχει δεδομένα, δεν κάνει κάτι.
    tree.delete(*tree.get_children())
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # Παίρνει όλα τα δεδομένα από τη ΒΔ
    all_DB_data = c.execute("SELECT * FROM ranking;")
    ranking_list = []    
    icon = PhotoImage(file="pencil-button.png")
    
    for data in all_DB_data.fetchall():
        ranking_list.append(data)
    
    # Λίστα για τη διατήρηση αναφορών στην εικόνα για αποφυγή 
    # απώλειας εικόνας λόγω garbage-collection
    tree.image_refs = []
    # Εισάγει τα δεδομένα στο tree
    for item in ranking_list:
        tree.insert('', tk.END, text = ' ', image = icon, values=item)
        tree.image_refs.append(icon)
    
    my_conn.close()
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


def check_challenge(player_1, player_2):
    """
    Συνάρτηση που ελέγχει την πρόκληση και επιστρέφει έγκριση ή μη της
    πρόκλησης καθώς και ανάλογο μήνυμα αποτυχίας ή επιτυχίας.
    
    
    Args:
        player_1 (int): Θέση του παίκτη που θέτει την πρόκληση.
        player_2 (int): Θέση του παίκτη που δέχεται την πρόκληση.
        
    Returns:
        dict:   success (boolean): True αν δεν υπάρχει λάθος.
                message (str): Μήνυμα για το παράθυρο ειδοποίησης.
    """
        
    # Υπολογισμός της διαφοράς των θέσεων που μπορεί να γίνει μια πρόκληση. 
    # Συγκεκριμένα για τις θέσεις 1 - 9 η διαφορά μπορεί να είναι μέχρι 3 θέσεις,
    # ενώ για τις θέσεις από 9 και πάνω, μέχρι 4 θέσεις.
    allowed_challenge_distance = 4 if player_1 > 9 else 3
    # Έλεγχος πως επιτρέπεται η διαφορά θέσεων
    if player_1 - player_2 > allowed_challenge_distance:
        return {
            'success': False,
            'message': 'Ο παίκτης που προκαλείται βρίσκεται πάνω από {0} θέσεις πάνω από τον παίκτη που προκαλεί.\nΗ πρόκληση είναι άκυρη.'.format(allowed_challenge_distance)
            }
    
    # Έλεγχος πως ο παίκτης που προκαλεί είναι κάτω από τον παίκτη που προκαλείται
    elif player_1 < player_2:
        return {
            'success': False,
            'message': "Ο παίκτης που προκαλείται είναι κάτω από τον παίκτη που προκαλεί. \nΗ πρόκληση είναι άκυρη."
            }
    
    # Έλεγχος για περίπτωση εισαγωγής ίδιου παίκτη
    elif player_1 == player_2:
        return {
            'success': False,
            'message': 'Λάθος καταχώρηση, ο παίκτης που προκαλεί είναι ο παίκτης που δέχεται την πρόκληση.'
            }
    
    return {
        'success': True,
        'message':'Η πρόκληση είναι αποδεκτή.\nΝίκησε ο παίκτης στη θέση #{0} που έκανε την πρόκληση;'.format(player_1)
        }


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
    return

    
def win(winner_index, loser_index,today_string=None):
    """
    Καταγράφει τη νίκη με παραμέτρους τις θέσεις των παικτών πριν την αλλαγή της 
    κατάταξης και ανανεώνει τις νίκες και ήττες του κάθε παίκτη στη ΒΔ.
    
    Αν νικήσει ο παίκτης χαμηλότερης θέσης (που κάνει την πρόκληση),
    παίρνει τη θέση του νικημένου (παίκτη που δέχθηκε την πρόκληση). Ο ηττημένος
    και όλοι οι παίκτες μεταξύ των δύο θέσεων θα μετακινηθούν μία θέση κάτω και
    η συνάρτηση επιστρέφει True.
    
    Αν νικήσει ο παίκτης υψηλότερης θέσης (που δέχθηκε την πρόκληση), δεν 
    προκαλείται αλλαγή στην κατάταξη, μόνο ενημέρωση νικών και ηττών και
    επιστρέφει False.
    
    
    Args:
        winner_index (int): Θέση του παίκτη που νίκησε τον αγώνα.
        loser_index (int): Θέση του παίκτη που έχασε τον αγώνα.
        today_string (str): Ημερομηνία αγώνα. 
        Αν δεν λάβει τιμή στην κλήση, τίθεται στη σημερινή ημερομηνία.
        
    Returns:
        boolean: True αν έγινε αλλαγή θέσης.
    """
    
    if today_string is None:
        today_string = grab_date()
        
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # +1 Wins σε νικητή και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute(
        "UPDATE ranking SET Wins = Wins + 1, Control_Date = ? WHERE Position = ?;", 
        (today_string, winner_index))
    # +1 Loses σε ηττημένο και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute(
        "UPDATE ranking SET Loses = Loses + 1, Control_Date = ? WHERE Position = ?;", 
        (today_string, loser_index))

    # Έλεγχος για την περίπτωση που η νίκη προκαλεί αλλαγή στην κατάταξη
    if loser_index < winner_index:
        # Προσωρινή αποθήκευση νικητή
        sql_query = "SELECT * FROM Ranking WHERE Position=?;"
        x = c.execute(sql_query, (winner_index,))

        # Επιστρέφει λίστα, με το playerDBData[0] να είναι πλειάδα στοιχείων 
        # του νικητή        
        winner_DB_data = x.fetchall() 
        # Διαγραφή νικητή από προηγούμενη θέση
        c.execute("DELETE FROM ranking WHERE Position=?;", (winner_index,)) 
        # Νέα πλειάδα για αλλαγή θέσης στην κατάταξη
        entry_data = (
            loser_index, 
            winner_DB_data[0][1], 
            winner_DB_data[0][2], 
            winner_DB_data[0][3], 
            winner_DB_data[0][4], 
            winner_DB_data[0][5]
            ) 
        
        my_conn.commit()
        my_conn.close()

        # Κλήση συνάρτησης ανακατάταξης που κατεβάζει τους παίκτες κατά μία 
        # θέση από την winner_index μέχρι ΚΑΙ τη loser_index
        update_positions(loser_index, winner_index) 

        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        # Εισαγωγή νικητή στη θέση ηττημένου
        c.execute("INSERT INTO ranking(Position, Name, Surname, Wins, Loses, Control_Date) VALUES (?, ?, ?, ?, ?, ?);", entry_data)
        my_conn.commit()
        my_conn.close()
        return True
        
    # Η νίκη δεν προκαλεί αλλαγές στις θέσεις, μόνο σε νίκες και ήττες
    else:
        my_conn.commit()
        my_conn.close()
        return False


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
            c.execute('UPDATE ranking SET Position = ? WHERE Position=?', (p+1, p)) 

    my_conn.commit()
    my_conn.close()
    return


def rank_decay(index, today_string=None):
    """
    Ο παίκτης της θέσης index πέφτει μία θέση λόγω αδράνειας και ο επόμενος
    παίκτης ανεβαίνει στη θέση του και η ΒΔ ενημερώνεται.
    
    
    Args:
        index (int): Θέση του παίκτη που πέφτει μία θέση.
        today_string (str): Ημέρα τελευταίας δραστηριότητας. 
        Αν δεν λάβει τιμή στην κλήση, τίθεται στη σημερινή ημερομηνία.
        
    Returns:
        None.
    """
    if today_string is None:
        today_string = grab_date()
    
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    x = c.execute("SELECT * FROM ranking WHERE Position=?;", (index,))
    # Προσωρινή αποθήκευση στοιχείων του παίκτη 
    # που υπόκειται σε πτώση λόγω αδράνειας.
    inactive_player = x.fetchall() 
    # Διαγραφή του παίκτη
    c.execute("DELETE FROM ranking WHERE Position=?;", (index,)) 
    # Μετακίνηση του κάτω παίκτη στην πλέον κενή θέση 
    # του παίκτη που υπέστη πτώση λόγω αδράνειας
    c.execute("UPDATE ranking SET Position = ? WHERE Position=?;", (index,index+1)) 
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
    c.execute("INSERT INTO ranking VALUES (?, ?, ?, ?, ?, ?);", entry) 

    my_conn.commit()
    my_conn.close()
    return


def is_position_empty(index):
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
    
    c.execute("SELECT Position FROM ranking WHERE Position=?;", (index,))
    # Πλειάδα με νούμερο για θέση ή κενή αν δεν υπάρχει παίκτης
    is_position_empty = c.fetchall() 
    flag = len(is_position_empty) == 0
    
    my_conn.close()
    return flag
    

def check_ranking_for_decay(comparison_date=None):
    """
    Ελέγχει αν υπάρχουν παίκτες που υπόκεινται σε decay στην κατάταξη λόγω
    αδράνειας. Ως αδράνεια ορίζεται ημέρα τελευταίας δραστηριότητας μεγαλύτερη
    των 30 ημερών.
    
    
    Args:
        comparison_date (datetime object): Προεπιλεγμένη τιμή η σημερινή 
        ημερομηνία για σύγκριση με το παρόν.
            
    Returns:
        dict:   
            immune (tuple): Πλειάδα με όνομα και 
            επώνυμο παίκτη που δεν πέφτει περαιτέρω. None αν δεν υπάρχει.
                
            message (str): Μήνυμα ενημέρωσης ύπαρξης παικτών που ήταν 
            αδρανείς και θέσεων αυτών.
    """
    
    if comparison_date is None:
        comparison_date = datetime.date.today()
        today_string = grab_date()
    
    conn = dbconnect('tennis_club.db')
    cursor = conn.cursor()

    # Λίστα με παίκτες που θα υποστούν πτώση λόγω αδράνειας
    decay_list = [] 
    cursor.execute("SELECT Position, Control_Date FROM ranking;")
    ranking = cursor.fetchall()
    # Δημιουργία dictionary για επιστροφή
    return_dict = {
        'immune': (None),
        'message':''
        }
    for index, date in ranking:
        
        # Διαχωρίζει το string της ημερομηνίας
        split_date = date.split(sep='/') 
        
        # Μετατροπή του string σε datetime object για σύγκριση
        last_play_date = datetime.date(
            int(split_date[2]),
            int(split_date[1]),
            int(split_date[0])
            )
        days_since_last_play = (comparison_date - last_play_date).days
        
        if days_since_last_play > 30:
            # Έλεγχος για την περίπτωση που ο παίκτης είναι τελευταίος και δεν
            # πέφτει περαιτέρω θέση
            if ranking[-1][0] == index: 
                cursor.execute(
                    "SELECT Name, Surname FROM ranking WHERE Position=?;", 
                    (index,)
                    )
                last_player = cursor.fetchone()
                # Προσθήκη ονοματεπωνύμου παίκτη στο key 'immune' του dictionary
                return_dict['immune'] = (last_player[0], last_player[1])
                cursor.execute(
                    "UPDATE ranking SET Control_Date=? WHERE Position=?;", 
                    (today_string, index)
                    )
                break
            # Προστίθεται στη λίστα, η αλλαγή δεν γίνεται εδώ γιατί
            # οδηγεί σε logical error του τρέχοντος περάσματος for
            decay_list.append(index) 
    
    conn.commit()
    conn.close()    
    
    # Έλεγχος αν η λίστα είναι κενή
    if decay_list: 
        decay_positions = ','.join(
            [str(single_decay_position) for single_decay_position in decay_list])
        if len(decay_list) == 1:
            decay_message = ''.join(
                ['Ο παίκτης στην θέση ', 
                 decay_positions, 
                 ' έπεσε μία θέση λόγω αδράνειας και η κατάταξη ανανεώθηκε.'
                 ])
        else:
            decay_message = ''.join(
                ['Οι παίκτες στις θέσεις ', 
                 decay_positions, 
                 ' έπεσαν μία θέση λόγω αδράνειας και η κατάταξη ανανεώθηκε.'
                 ])
        return_dict['message'] = decay_message
        # Αντίστροφο πέρασμα της λίστας για αποφυγή λαθών από την αλλαγή θέσης
        # Π.χ. αν πρέπει να πέσουν οι παίκτες των θέσεων 2 και 3, αν πέσει
        # πρώτα ο 2ος, θα γίνει 3ος και ο 3ος θα πάρει τη θέση του και θα γίνει
        # 2ος. Έπειτα, πρέπει να πέσει ο 3ος, αλλά πλεόν ο 3ος είναι ο 2ος.
        # Για αυτό πρώτα 3ος γίνεται 4ος, μετά 2ος γίνεται 3ος.
        for i in decay_list[::-1]: 
            rank_decay(i)            
    
    # Η λίστα αδρανών παικτών είναι κενή
    else:
        return_dict['message'] = "Δεν υπάρχει κανένας παίκτης που να υπόκειται σε μείωση θέσης λόγω αδράνειας."
    return return_dict


def grab_date():
    """
    Συνάρτηση που επιστρέφει τη σημερινή ημερομηνία στη μορφή "ημέρα/μήνας/έτος".
    
    
    Args:
        None.
    
    Returns:
        str: Σημερινή ημερομηνία στη μορφή "{ημέρα}/{μήνας}/{έτος}".
    """
    today = datetime.date.today()
    today_string = "{0}/{1}/{2}".format(today.day,today.month,today.year)
    return today_string


# TODO: front-end starts here
# TODO: fix bug allowing occupation of position #0
def on_initialize_click(main_window):
    """
    Συνάρτηση κουμπιού Αρχικοποίησης Κατάταξης. Ελέγχει αν υπάρχει ήδη κατάταξη
    και ενημερώνει τον χρήστη για αδυναμία αρχικοποίησης αν υπάρχει.
    Δημιουργεί παράθυρο διαλόγου για εισαγωγή ονομάτων παικτών που θα 
    χρησιμοποιηθούν για την τυχαία αρχικοποίηση κατάταξης.
    
    
    Args:
        main_window (Tk Object): Κύριο παράθυρο της εφαρμογής.
        
    Returns:
        None.
    """ 
    # Έλεγχος για το αν ο πίνακας περιέχει παίκτες        
    if not is_position_empty(1): 
        # Αν περιέχει παίκτες, η τυχαία αρχικοποίηση δεν είναι διαθέσιμη
        # και ο χρήστης ενημερώνεται με το ανάλογο μήνυμα λάθους
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message='''Ο πίνακας κατάταξης περιέχει ήδη παίκτες και δεν μπορεί να αρχικοποιηθεί τυχαία. 
Παρακαλώ, διαγράψτε όλους τους παίκτες ή προσθέστε παίκτες χρησιμοποιώντας κάποια από τις επιλογές.'''
            )
        return
    
    
    # Παράθυρο διαλόγου αρχικοποίησης
    initialize_dialog = tk.Toplevel(main_window)
    initialize_dialog.title('Αρχικοποίηση λίστας')
    initialize_dialog.geometry('400x500+700+350')
    # Keybind για κλείσιμο παραθύρου με Escape
    initialize_dialog.bind(
        "<Escape>", 
        lambda event: initialize_dialog.destroy()
        )
    
    # Μεταβλητή για αποθήκευση παικτών προς αρχικοποίηση ως πεδίο του παραθύρου
    initialize_dialog.players = []
    # Δυναμική μεταβλητή StringVar για προβολή εισαχθέντων 
    # παικτών καθώς αυτοί εισάγονται, ως πεδίο του παραθύρου
    initialize_dialog.initialization_list_label = tk.StringVar()
    initialize_dialog.initialization_list_label.set('Κενή Λίστα Παικτών')
    # Πεδίο εισαγωγής
    initialize_dialog.initialization_entry = tk.Entry(
        initialize_dialog,
        justify='center', 
        font='Times 16',
        selectborderwidth=3
        )
    initialize_dialog.initialization_entry.pack(pady=10)
    initialize_dialog.initialization_entry.focus_set()
    # Keybind για καταχώρηση παίκτη στη λίστα με Enter
    initialize_dialog.initialization_entry.bind(
        "<Return>", 
        lambda event: on_initialize_add_player_click(initialize_dialog)
        )
    # Κουμπί καταχώρησης παίκτη στη λίστα
    tk.Button(
        initialize_dialog, 
        text="Καταχώρηση Παίκτη", 
        font='Times 16', 
        command = lambda: on_initialize_add_player_click(initialize_dialog)
        ).pack(pady=5)
    # Κουμπί τέλους καταχωρήσεων και αρχικοποίησης κατάταξης
    tk.Button(
        initialize_dialog,
        text="Τέλος Καταχωρήσεων",
        font = 'Times 16', 
        command = lambda: on_finalize_initialization_click(initialize_dialog)
        ).pack(pady=5)
    ttk.Separator(
        initialize_dialog,
        orient='horizontal'
        ).pack(fill='x',pady=15)
    # Δυναμικό Label που αλλάζει με τις καταχωρήσεις
    tk.Label(
        initialize_dialog, 
        textvariable = initialize_dialog.initialization_list_label,
        font = 'Times 16',
        justify='center'
        ).pack()     
    initialize_dialog.mainloop()
    

def on_initialize_add_player_click(window):
    """
    Συνάρτηση κουμπιού καταχώρησης παίκτη στο παράθυρο διαλόγου αρχικοποίησης.
    Ελέγχει το όνομα που εισήχθη, ενημερώνει σε περίπτωση λάθους, ανανεώνει 
    δυναμική λίστα για παρουσίαση παικτών που έχουν ήδη εισαχθεί για αρχικοποίηση.
    
    
    Args:
        window (Top Level Object): Παράθυρο διαλόγου αρχικοποίησης.
        
    Returns:
        None.
    """
    name = window.initialization_entry.get()
    window.initialization_entry.delete(0,'end')
    player = name.split(sep=' ')
    
    # Περίπτωση που εισαχθούν πάνω απο 1 κενά
    if len(player) != 2: 
        msg.showerror(
            master=window, 
            parent=window,  
            title='Ειδοποίηση', 
            message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό."
            )
        return
    # Προσθήκη παίκτη στη λίστα
    window.players.append(player)
    # Ελέγχει αν το δυναμικό Label έδειχνε κενή λίστα και απαιτεί πρώτη
    # μορφοποίηση κι όχι απλά προσθήκη παίκτη σε αυτήν
    if window.initialization_list_label.get() == 'Κενή Λίστα Παικτών':
        window.initialization_list_label.set("Λίστα Παικτών\n")
    # Παίρνει τα δεδομένα που είχε το δυναμικό Label 
    # για να προσθέσει το νέο δεδομένο
    string = '\n'.join([window.initialization_list_label.get(),name])
    # Προσθήκη νέου παίκτη
    window.initialization_list_label.set(string)
    window.initialization_entry.focus_set()
    return


def on_finalize_initialization_click(window):
    """
    Συνάρτηση κουμπιού τέλους καταχωρήσεων στο παράθυρο διαλόγου αρχικοποίησης.
    Ελέγχει αν έχει εισαχθεί παίκτης στη λίστα. Αν δεν έχει εισαχθεί έστω ένας, 
    ενημερώνει με το κατάλληλο μήνυμα. Σε αντίθετη περίπτωση, προχωράει στην
    αρχικοποιήση της κατάταξης με τη λίστα παικτών που δόθηκε.
    
    
    Args:
        window (Top Level Object): Παράθυρο διαλόγου αρχικοποίησης.
        
    Returns:
        None.
    """
    # Ελέγχει αν η λίστα players είναι κενή
    if window.players:
        initialization(window.players)
        msg.showinfo(
            parent=window,
            title='Ειδοποίηση', 
            message='Οι παίκτες καταχωρήθηκαν τυχαία στην κατάταξη.'
            )
        window.destroy()
        return
    
    else: 
        window.destroy()
        # Σε περίπτωση που ήταν κενή ενημερώνει τον χρήστη με το κατάλληλο μήνυμα
        msg.showerror(
            parent=window, 
            title='Ειδοποίηση', 
            message='Δε δημιουργήθηκε κατάταξη καθώς δεν εισάγατε ονόματα.'
            )
        return


def on_add_player(main_window):
    """
    Συνάρτηση κουμπιού προσθήκης παίκτης στο αρχικό παράθυρο. Ρωτάει τον χρήστη
    αν ο παίκτης θα εισαχθεί στο τέλος της κατάταξης ή σε συγκεκριμένη θέση,
    δημιουργεί παράθυρο διαλόγου για εισαγωγή ονοματεπωνύμου παίκτη.
    
    
    Args:
        main_window (Tk Object): Κύριο παράθυρο της εφαρμογής.
        
    Returns:
        None.
    """
    
   
    # Απάντηση χρήστη περί εισαγωγής παίκτη σε συγκεκριμένη θέση.
    position_entry_answer = msg.askyesnocancel(
        title='Προσθήκη Παίκτη',
        message='''Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση;'''
        )
    if position_entry_answer == None:
        msg.showinfo(
            master=main_window, 
            title='Ειδοποίηση', 
            message='Η προσθήκη παίκτη ακυρώθηκε.'
            )
        return
            
    # Παράθυρο διαλόγου εισαγωγής ονοματεπωνύμου παίκτη
    name_entry_dialog = tk.Toplevel(main_window)
    name_entry_dialog.geometry("550x150+650+350")
    name_entry_dialog.title('Προσθήκη Παίκτη')
    name_entry_dialog.bind(
        "<Escape>", 
        lambda event: name_entry_dialog.destroy()
        )
    # Ορίζεται ως πεδίο του αντικειμένου Top Level για να περαστεί 
    # στις συναρτήσεις που την χρησιμοποιούν
    name_entry_dialog.position_entry_answer = position_entry_answer
    tk.Label(
        name_entry_dialog, 
        font=main_window.default_font, 
        text = "Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε: "
        ).pack(pady=5)
    # Πεδίο εισαγωγής
    name_entry_dialog.name_entry = tk.Entry(
        name_entry_dialog, 
        font=main_window.default_font, 
        justify='center'
        )
    name_entry_dialog.name_entry.pack(pady=5)
    name_entry_dialog.name_entry.focus_set()
    name_entry_dialog.name_entry.bind(
        "<Return>", 
        lambda event: on_new_player_name_submit(name_entry_dialog)
        )
    # Κουμπί εισαγωγής ονοματεπωνύμου παίκτη
    tk.Button(
        name_entry_dialog, 
        text='Προσθήκη', 
        font=main_window.default_font, 
        command= lambda: on_new_player_name_submit(name_entry_dialog)
        ).pack(pady=5)
    

def on_new_player_name_submit(window):
    """
    Συνάρτηση για το κουμπί διαλόγου εισαγωγής παίκτη. Ελέγχει αν το όνομα και το
    επίθετο δόθηκαν σε αποδεκτή μορφή και ενημερώνει τον χρήστη. 
    
    Αν ο χρήστης απάντησε πως δε θέλει να βάλει τον παίκτη σε συγκεκριμένη θέση,
    βάζει τον παίκτη στην τελευταία θέση της ΒΔ με κλήση της insert_player_at_end().
    
    Αν ο χρήστης απάντησε πως θέλει να βάλει τον παίκτη σε συγκεκριμένη θέση, 
    ζητάει τη θέση με νέο παράθυρο διαλόγου.
    
    
    Args:
        window (Top Level Object): Παράθυρο εισαγωγής ονοματεπωνύμου παίκτη.
        
    Returns: 
        None.
    """
    player_name_entry = window.name_entry.get()
    window.name_entry.delete(0,'end')
    
    player_name = player_name_entry.split(sep=' ')
    # Έλεγχος σωστής εισαγωγής ονοματεπωνύμου
    if len(player_name) != 2: 
        # Ενημέρωση χρήστη με κατάλληλο μήνυμα
        msg.showerror(
            parent=window, 
            title='Ειδοποίηση', 
            message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό."
            )
        return
    name, surname = player_name[0], player_name[1]
    # Αν ο χρήστης απάντησε πως δε θέλει να βάλει σε συγκεκριμένη θέση
    # τον παίκτη, μπαίνει στην τελευταία θέση
    if window.position_entry_answer == False:
        new_last_place = insert_player_at_end(name, surname)
        # Μήνυμα ενημέρωσης επιτυχούς εισαγωγής
        msg.showinfo(
            parent=window, 
            title='Ειδοποίηση', 
            message=f'Ο {name} {surname} τοποθετήθηκε επιτυχώς στη θέση #{new_last_place}.'
            )
        window.destroy()
    # Αν ο χρήστης απάντησε πως θέλει να βάλει σε συγκεκριμένη θέση τον παίκτη
    elif window.position_entry_answer == True:
        # Δημιουργία παραθύρου διαλόγου
        default_font = 'Times 16'
        position_entry_dialog = tk.Toplevel(window)
        position_entry_dialog.geometry("600x150+625+450")
        position_entry_dialog.title("Προσθήκη Παίκτη σε Θέση")
        position_entry_dialog.bind(
            "<Escape>", 
            lambda event: position_entry_dialog.destroy()
            )
        
        tk.Label(
            position_entry_dialog, 
            font=default_font, 
            text='Δώστε τη θέση κατάταξης του παίκτη που θέλετε να προσθέσετε: '
            ).pack(pady=5)
        # Πεδίο εισαγωγής
        
        position_entry_dialog.position_entry = tk.Entry(
            position_entry_dialog, 
            font=default_font, 
            justify='center'
            )
        position_entry_dialog.position_entry.pack(pady=5)
        position_entry_dialog.position_entry.focus_set()
        position_entry_dialog.position_entry.bind(
            "<Return>", 
            lambda event: on_new_player_position_submit(
                name, 
                surname, 
                position_entry_dialog
                )
            )
        # Κουμπί καταχώρησης θέσης εισαγωγής παίκτη προς προσθήκη
        tk.Button(
            position_entry_dialog, 
            font=default_font, 
            text='OK',
            command= lambda: on_new_player_position_submit(
                name,
                surname,
                position_entry_dialog
                )
            ).pack(pady=5)
        
    return


def on_new_player_position_submit(name, surname, window):
    """
    Συνάρτηση κουμπιού εισαγωγής θέσης για το παράθυρο διαλόγου προσθήκης παίκτη
    σε συγκεκριμένη θέση.
    Ελέγχει αν η εισαγωγή είναι σωστή και ανανεώνει τη ΒΔ καλώντας την 
    insert_player_at_position() ή ενημερώνει τον χρήστη με μήνυμα σφάλματος.
    
    
    Args:
        name (str): Το όνομα του παίκτη που θα εισαχθεί.
        surname (str): Το επώνυμο του παίκτη που θα εισαχθεί.
        window (Top Level object): Το παράθυρο διαλόγου εισαγωγής θέσης.
        
    Returns:
        None.
    """
    
    # Try block για εισαγωγή μη ακεραίου αριθμού.
    # Ο αμυντικός προγραμματισμός για εισαγωγή αποδεκτής τιμής 
    # γίνεται μέσω της insert_player_at_position
    try:
        player_position = int(window.position_entry.get())
        window.position_entry.delete(0,'end')
        if insert_player_at_position(player_position, name, surname):
            msg.showinfo(
                parent=window, 
                title='Ειδοποίηση', 
                message=f'Ο παίκτης {name} {surname} τοποθετήθηκε επιτυχώς στη θέση #{player_position}.'
                )
        else:
            msg.showerror(
                parent=window,
                title='Ειδοποίηση', 
                message=f"Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη {name} {surname}."
                )
        window.destroy()
    except ValueError:
        # Ενημέρωση χρήστη για μη αποδεκτή εισαγωγή θέση (όχι ακέραιος)
        msg.showerror(
            parent=window, 
            title='Ειδοποίηση', 
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης."
            )
    return
    

def on_del_player(main_window):
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για διαγραφή παίκτη.
    Ελέγχει αν η κατάταξη περιέχει έστω έναν παίκτη και δημιουργεί παράθυρο 
    διαλόγου για εισαγωγή θέσης κατάταξης του παίκτη που θα διαγραφεί ή ενημερώνει
    τον χρήστη με το ανάλογο μήνυμα σφάλματος.
    
    
    Args:
        main_window (Tk Object): Κύριο παράθυρο της εφαρμογής.
        
    Returns:
        None.
    """
    # Ελέγχει αν η κατάταξη περιέχει έστω έναν παίκτη
    if is_position_empty(1):
        # Ειδοποίηση χρήστη με το κατάλληλο μήνυμα
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    # Η κατάταξη περιέχει παίκτες
    else:
        # Δημιουργία παραθύρου διαλόγου
        deletion_dialog = tk.Toplevel(main_window)
        deletion_dialog.geometry("550x200+650+450")
        deletion_dialog.title('Διαγραφή Παίκτη')
        deletion_dialog.bind(
            "<Escape>", 
            lambda event: deletion_dialog.destroy()
            )
        tk.Label(
            deletion_dialog, 
            text='Δώστε τη θέση κατάταξης του παίκτη που θέλετε να διαγράψετε: ', 
            font = 'Times 14'
            ).pack(pady=20)
        # Πεδίο εισαγωγής
        
        deletion_dialog.deletion_entry = tk.Entry(
            deletion_dialog,
            justify = 'center', 
            font=main_window.default_font
            )
        deletion_dialog.deletion_entry.pack(pady=5)
        deletion_dialog.deletion_entry.focus_set()
        deletion_dialog.deletion_entry.bind(
            "<Return>", 
            lambda event: on_dialog_delete_click(deletion_dialog)
            )
        # Κουμπί διαγραφής
        tk.Button(
            deletion_dialog, 
            text='Διαγραφή', 
            font='Times 16', 
            command= lambda: on_dialog_delete_click(deletion_dialog)
            ).pack(side='left',padx=60)
        # Κουμπί ακύρωσης διαγραφής
        tk.Button(
            deletion_dialog, 
            text='Ακύρωση', 
            font='Times 16', 
            command=deletion_dialog.destroy
            ).pack(side='right',padx=60)
        
        deletion_dialog.mainloop()
        

def on_dialog_delete_click(window):
    """
    Συνάρτηση για το κουμπί διαγραφής του παραθύρου διαλόγου διαγραφής παίκτη.
    Ελέγχει ότι ο χρήστης εισάγει ακέραιο αριθμό για τη θέση κατάταξης ή 
    ειδοποιεί με το κατάλληλο μήνυμα σφάλματος, ότι η θέση περιέχει παίκτη
    και ζητάει επιβεβαίωση διαγραφής. Ενημερώνει τη ΒΔ καλώντας την
    delete_player().
    
    
    Args:
        window (Top Level Object): Παράθυρο διαλόγου διαγραφής.
        
    Returns: 
        None.
    """
    # Ελέγχει πως ο χρήστης εισήγαγε ακέραιο αριθμό
    # Ο έλεγχος αποδεκτής τιμής γίνεται από την delete_player()
    try:
        index = int(window.deletion_entry.get())
        delete_player(index)
    except ValueError:
        # Ειδοποίηση χρήστη για λάθος εισαγωγή θέσης
        msg.showerror(
            parent=window, 
            title='Ειδοποίηση', 
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης."
            )
        window.deletion_entry.delete(0,'end')
        
    # Έλεγχος αν η θέση περιέχει άτομο και ενημέρωση με μήνυμα σφάλματος
    if is_position_empty(index):
        msg.showerror(
            parent=window,
            title='Ειδοποίηση', 
            message="Δεν υπάρχει παίκτης στη θέση που προσπαθείτε να κάνετε διαγραφή."
            )
    else:
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()
        # Λήψη δεδομένων προς διαγραφή παίκτη
        playerDBData = c.execute("SELECT * FROM ranking WHERE Position = ?;", (index,)).fetchall()
        my_conn.commit()
        my_conn.close()
        # Παράθυρο επιβεβαίωσης διαγραφής
        confirmation = msg.askyesno(
            parent=window,
            title='Διαγραφή Παίκτη', 
            message=f'''ΠΡΟΣΟΧΉ!!!! Η διαγραφή είναι οριστική κι αμετάκλητη!
Θα χαθούν ΌΛΑ τα δεδομένα του παίκτη.
Θέλετε σίγουρα να διαγράψετε τον παίκτη {playerDBData[0][1]} {playerDBData[0][2]}; '''
            )
        # Ακύρωση διαγραφής και ενημέρωση χρήστη
        if confirmation == False:
            msg.showerror(
                parent=window, 
                title='Ειδοποίηση', 
                message="Η διαγραφή ακυρώθηκε από τον χρήστη."
                )
            window.deletion_entry.delete(0,'end')
            return
        else:
            delete_player(index)
            # Μήνυμα ειδοποίησης επιτυχούς διαγραφής
            msg.showinfo(
                parent=window,
                title='Ειδοποίηση', 
                message=f'Ο παίκτης στη θέση #{index} διαγράφηκε επιτυχώς.'
                )
            window.deletion_entry.delete(0,'end')
        
    return


def on_challenge_click(main_window):
    """
    Συνάρτηση κουμπιού καταγραφής αγώνα του κυρίου παραθύρου. 
    
    Ελέγχει αν η κατάταξη περιέχει 0 ή μόνο 1 παίκτες και ενημερώνει τον χρήστη
    με το κατάλληλο μήνυμα σφάλματος.
    
    Δημιουργεί παράθυρο διαλόγου για καταγραφή της θέσης του παίκτη που θέτει
    την πρόκληση.
    
    
    Args:
        main_window (Tk Object): Κύριο παράθυρο της εφαρμογής.
        
    Returns:
        None.
    """
    # Έλεγχος αν η κατάταξη περιέχει έναν ή κανέναν παίκτη και δεν ορίζεται αγώνας
    if is_position_empty(1):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    elif is_position_empty(2):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη περιέχει μόνο έναν παίκτη άρα δεν ορίζεται πρόκληση."
            )
    # Περιέχει πάνω από 1 παίκτη
    else:
        # Δημιουργία παραθύρου διαλόγου για την πρόκληση
        challenge_dialog = tk.Toplevel(main_window)
        challenge_dialog.geometry("650x200+650+450")
        challenge_dialog.title("Καταγραφη Πρόκλησης")
        challenge_dialog.bind(
            "<Escape>", 
            lambda event: challenge_dialog.destroy()
            )
        # Τίθεται ως δυναμικό Label για να αλλάζει 
        # μετά την καταχώρηση του πρώτου παίκτη
        challenge_dialog.challenge_label = tk.StringVar()
        challenge_dialog.challenge_label.set('Δώστε τη θέση κατάταξης του παίκτη που προκαλεί: ')
        tk.Label(
            master=challenge_dialog, 
            textvariable= challenge_dialog.challenge_label, 
            font=main_window.default_font
            ).pack(pady = 10)
        # Πεδίο εισαγωγής
        challenge_dialog.challenge_entry = tk.Entry(
            master=challenge_dialog, 
            justify='center', 
            font=main_window.default_font
            )
        challenge_dialog.challenge_entry.pack(pady = 10)
        challenge_dialog.challenge_entry.focus_set()
        challenge_dialog.challenge_entry.bind(
            "<Return>", 
            lambda event: on_dialog_challenge_click(challenge_dialog)
            )
        # Μεταβλητή που αποθηκεύει τις θέσεις των παικτών
        # που εμπλέκονται στην πρόκληση ως πεδίου του Top Level object
        challenge_dialog.players_in_challenge = []
        # Κουμπί καταχώρησης θέσης παίκτη που εμπλέκεται στην πρόκληση
        tk.Button(
            master=challenge_dialog, 
            text='OK', 
            font = main_window.default_font, 
            command= lambda: on_dialog_challenge_click(challenge_dialog)
            ).pack(pady = 10)
        challenge_dialog.mainloop()


def on_dialog_challenge_click(window):
    """
    Συνάρτηση κουμπιού καταχώρησης θέσης παίκτη που συμμετέχει στην πρόκληση. 
    
    Όταν πατιέται για τον πρώτο παίκτη το κουμπί, η συνάρτηση ελέγχει αν η 
    εισαγωγή είναι σωστή (ακέραιος) και αν υπάρχει παίκτης στη θέση. 
    Έπειτα, αλλάζει το μήνυμα του παραθύρου διαλόγου για να ζητήσει τη θέση του 
    παίκτη που δέχεται την πρόκληση.
    
    Όταν πατιέται το κουμπί δεύτερη φορά, αφότου δηλαδή έχει καταχωρηθεί ο 
    πρώτος παίκτης, ελέγχεται και πάλι η τιμή και καλεί την check_challenge() που 
    ελέγχει την πρόκληση σύμφωνα με τους κανόνες και ενημερώνει τη ΒΔ ή 
    ενημερώνει τον χρήστη με το κατάλληλο μήνυμα σφάλματος.
    
    
    Args:
        window (Top Level): Παράθυρο διαλόγου καταγραφής πρόκλησης.
        
    Returns:
        None.
    """
    # Έλεγχοι εισαγωγής για valid θέση και για εισαγωγή ακεραίου.
    try:
        # Ελέγχει πως η θέση που εισήχθη περιέχει παίκτη ή ενημερώνει με
        # το ανάλογο μήνυμα σφάλματος
        if is_position_empty(int(window.challenge_entry.get())):
            msg.showerror( 
                parent=window, 
                title='Ειδοποίηση', 
                message=f"Δεν υπάρχει παίκτης στη θέση #{window.challenge_entry.get()}"
                )
            return
        # Προσθήκη εισαχθείσας θέσης στη λίστα παικτών που εμπλέκονται
        window.players_in_challenge.append(int(window.challenge_entry.get()))
        window.challenge_entry.delete(0,'end')
    except ValueError:
        # Ενημέρωση χρήστη για εισαγωγή μη ακεραίου
        # Ο έλεγχος των τιμών της πρόκλησης γίνεται από το try block και
        # από την check_challenge()
        msg.showerror(
            parent=window, 
            title='Ειδοποίηση', 
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης."
            )
        return
    # Εάν έχει λάβει μόνο έναν παίκτη, ενημερώνει το δυναμικό Label
    if len(window.players_in_challenge) == 1:
        window.challenge_label.set('Δώστε τη θέση κατάταξης του παίκτη που δέχεται την πρόκληση:')
    # Εάν έχει λάβει 2 παίκτες, καλεί την check_challenge()
    elif len(window.players_in_challenge) == 2:
        return_dict = check_challenge(
                window.players_in_challenge[0], 
                window.players_in_challenge[1]
                )
        if return_dict['success'] == False:
            msg.showerror(
                parent=window, 
                title='Ειδοποίηση', 
                message=return_dict['message']
                )
        else:
            answer = msg.askyesnocancel(
                parent=window, 
                title='Αποτέλεσμα Αγώνα',
                message=f'''Η πρόκληση είναι αποδεκτή.
Νίκησε ο παίκτης στη θέση #{window.players_in_challenge[0]} που έκανε την πρόκληση;'''
         )
    
            if answer == True:
                change_flag = win(
                    window.players_in_challenge[0], 
                    window.players_in_challenge[1]
                    )
            elif answer == False:
                change_flag = win(
                    window.players_in_challenge[1], 
                    window.players_in_challenge[0]
                    )
            # Αν ο χρήστης κλείσει το παράθυρο χωρίς να απαντήσει για νικητή
            elif answer == None:
                msg.showerror(
                    parent=window, 
                    title='Ειδοποίηση', 
                    message="Ο αγώνας δεν καταγράφηκε, ακύρωση από τον χρήστη."
                    )
                window.destroy()
                # Return εδώ για να μην εντοπίσει πρόβλημα change_flag undefined
                return
            
            if change_flag:
                # Ενημέρωση χρήστη για αλλαγές στην κατάταξη
                msg.showinfo(
                    parent=window, 
                    title='Ειδοποίηση', 
                    message='Το παιχνίδι καταγράφηκε επιτυχώς και η κατάταξη ανανεώθηκε!'
                    )
            else:
                msg.showinfo(
                    parent=window,
                    title='Ειδοποίηση', 
                    message='Το παιχνίδι καταγράφηκε επιτυχώς, χωρίς αλλαγή στην κατάταξη!'
                    )
        window.destroy()
        return


def on_inactive_check_click(main_window):
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για έλεγχο για αδρανείς παίκτες.
    Ελέγχει αν η κατάταξη περιέχει παίκτες και καλεί την 
    check_ranking_for_decay() ή ενημερώνει με μήνυμα λάθους.
    
    Η check_ranking_for_decay() θα ενημερώσει τη ΒΔ αναλόγως με το αν υπάρχουν
    αδρανείς παίκτες.
    
    
    Args:
        main_window (Tk Object): Κύριο παράθυρο της εφαρμογής.
        
    Returns:
        None.
    """
    # Ελέγχει πως η κατάταξη δεν είναι κενή ή ειδοποιεί με το κατάλληλο μήνυμα
    if is_position_empty(1):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    else:
        decay_result = check_ranking_for_decay()
    # Αν το immune δεν είναι None
    if decay_result['immune'] is not None:
        # Μήνυμα ειδοποίησης χρήστη πως ο παίκτης δεν πέφτει περαιτέρω
        msg.showinfo(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Ο παικτης {0} {1} είναι ήδη στην τελευταία θέση και δεν πέφτει περαιτέρω.".format(
                decay_result['immune'][0], 
                decay_result['immune'][1]
                )
            )
    msg.showinfo(
        master=main_window, 
        title='Ειδοποίηση', 
        message=decay_result['message']
        )


def on_show_ranking_click(main_window):
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για εμφάνιση της κατάταξης.
    
    Ελέγχει αν η κατάταξη περιέχει παίκτες και δημιουργεί ένα παράθυρο με τον
    πίνακα κατάταξης που γεμίζεται από την print_() ή ενημερώνει τον χρήστη
    με μήνυμα σφάλματος περί άδειας κατάταξης.
    
    
    Args:
        main_window (Tk Object): Κύριο παράθυρο της εφαρμογής.
        
    Returns:
        None.
    """
    # Ελέγχει πως η κατάταξη δεν είναι κενή ή ειδοποιεί με το κατάλληλο μήνυμα
    if is_position_empty(1):
        msg.showerror(
            master=main_window, 
            title='Ειδοποίηση', 
            message="Η κατάταξη δεν περιέχει παίκτες!"
            )
    else:
        # Δημιουργεί παράθυρο με tree για προβολή κατάταξης
        ranking_window = tk.Toplevel(main_window)
        ranking_window.title("Πίνακας Κατάταξης")
        ranking_window.geometry("1250x800+350+0")
        ranking_window.bind(
            "<Escape>", 
            lambda event: ranking_window.destroy()
            )
        tree_style = ttk.Style()
        tree_style.configure(
            "mystyle.Treeview",
            font=('Times',16),
            rowheight=30
            )
        tree_style.configure(
            "mystyle.Treeview.Heading",  
            font=('Times', 16), 
            )
        # Δημιουργία Treeview με τις απαιτούμενες στύλες και μορφοποιήσεις
        tree = ttk.Treeview(
            ranking_window, 
            style="mystyle.Treeview", 
            columns=(
                'Θέση', 
                'Όνομα', 
                'Επίθετο', 
                'Νίκες', 
                'Ήττες',
                'Ημ/νία Δραστηριότητας'
                ),
            show='tree headings'
            )
        tree.column(
            '#0', 
            anchor = 'center',
            width = 57
            )
        tree.column(
            'Θέση', 
            anchor = 'center',
            width=10
            )
        tree.column(
            'Όνομα',
            anchor = 'center',
            width=150
            )
        tree.column(
            'Επίθετο',
            anchor = 'center',
            width=225
            )
        tree.column(
            'Νίκες', 
            anchor = 'center',
            width=10
            )
        tree.column(
            'Ήττες', 
            anchor = 'center',
            width=10
            )
        tree.column(
            'Ημ/νία Δραστηριότητας',
            anchor = 'center',
            width = 200
            )
        tree.heading('#0', text = 'Επεξεργασία', anchor = 'center')
        tree.heading('Θέση', text = 'Θέση')
        tree.heading('Όνομα', text = 'Όνομα')
        tree.heading('Επίθετο', text = 'Επίθετο')
        tree.heading('Νίκες', text = 'Νίκες')
        tree.heading('Ήττες', text = 'Ήττες')
        tree.heading('Ημ/νία Δραστηριότητας', text = 'Ημ/νία Δραστηριότητας')
        # Καλεί την fill_tree() να γεμίσει το tree με τα δεδομένα της ΒΔ
        fill_tree(tree)
        tree.pack(fill='both',expand=1)
        # Εντοπίζει clicks στο παράθυρο
        tree.bind(
            "<Button-1>", 
            lambda event: on_tree_click(event, tree, main_window)
            )
        ranking_window.focus_set()
        ranking_window.mainloop()
        return
 
    
def on_tree_click(event, tree, main_window):
    """
    Συνάρτηση που λαμβάνει τα events clicks στο παράθυρο και ελέγχει αν ήταν
    στο κουμπί επεξεργασίας. Αν ήταν όντως, καλεί την on_edit_click().
    
    
    Args:
        event (Event Object): Αντικείμενο με τα στοιχεία του event.
        tree (Treeview Object): Το Tree του αρχικού παραθύρου.
        main_window (Tk Object): Κύριο παράθυρο εφαρμογής.
        
    Returns:
        None.
    """
    region = tree.identify("region", event.x, event.y)
    col = tree.identify_column(event.x)
    row = tree.identify_row(event.y)
    if col == "#0" and region == 'tree' and row:
        on_edit_click(row, tree, main_window)
    return


def on_edit_click(item_id, tree, main_window):
    """
    Συνάρτηση απόκρισης στο click στην στήλη επεξεργασία. Ανοίγει παράθυρο
    διαλόγου για επεξεργασία των πεδίων.
    
    
    Args:
        item_id (event.y object): Παράμετρος που καθορίζει ποια γραμμή επιλέχθηκε.
        tree (Treeview object): Ο πίνακας του παραθύρου.
        main_window (Tk object): Κύριο παράθυρο εφαρμογής.
        
    Returns:
        None.
    """
    edit_details_dialog = tk.Toplevel(main_window)
    edit_details_dialog.title("Επεξεργασία")
    edit_details_dialog.geometry('350x550+650+150')
    edit_details_dialog.bind(
        "<Escape>", 
        lambda event: edit_details_dialog.destroy()
        )
    edit_details_dialog.values = tree.item(item_id, 'values')
    columns = [
        'Θέση',
        'Όνομα', 
        'Επώνυμο',
        'Νίκες',
        'Ήττες',
        'Ημ/νία Δραστηριότητας'
        ]
    col_index = 0
    # Μεταβλητή στην οποία αποθηκεύεται αναφορά στα Entries
    edit_details_dialog.entry_fields = []
    for value in edit_details_dialog.values:
        tk.Label(
            edit_details_dialog,
            font = main_window.default_font,
            text = columns[col_index],
            ).pack(pady=5)
        entry = tk.Entry(
            edit_details_dialog,
            font = main_window.default_font,
            justify = 'center', 
            )
        entry.insert(0,value)
        entry.pack(pady=5)
        edit_details_dialog.entry_fields.append(entry)
        col_index += 1
    
    edit_details_dialog.focus_set()
    edit_details_dialog.bind(
        "<Return>",
        lambda event: on_edit_save(edit_details_dialog,tree)
        )

    tk.Button(
        edit_details_dialog, 
        font = main_window.default_font,
        text = "Αποθήκευση", 
        command = lambda: on_edit_save(edit_details_dialog,tree)
        ).pack(pady=5)
    edit_details_dialog.mainloop()


def on_edit_save(window, tree):
    """
    Συνάρτηση κουμπιού αποθήκευσης στην επεξεργασία καταχώρησης του
    παραθύρου εμφάνισης κατάταξης.
    Ελέγχει εισαγωγή θετικών ακεραίων για Θέση, Νίκες και ήττες και εισαγωγή 
    χωρίς κενά για όνομα και επώνυμο.
    Ανανεώνει δεδομένα της ΒΔ με τη βοήθεια της update_info() και θέσεις με τη
    βοήθεια των delete_player() και insert_player_at_position().
    
    
    Args:
        window (Top Level Object): Το παράθυρο διαλόγου επεξεργασίας καταχώρησης.
        tree (Treeview Object): Ο πίνακας κατάταξης για ανανέωσή του με νέα δεδομένα.
    
    Returns:
        None.
    """
    
    # Λίστα στην οποία αποθηκεύονται οι τιμές που εισήχθησαν
    entered_values = []
    for entry_field in window.entry_fields:
        entered_values.append(entry_field.get())
    
    # Έλεγχος σωστής εισαγωγής ακεραίων για θέση, νίκες, ήττες.
    values_index_tag = [
        (0,'την θέση κατάταξης.'),
        (3,'τις νίκες.'),
        (4,'τις ήττες.')
        ]
    entered_rank_wins_loses = []
    for index, tag in values_index_tag:
        try:
            entered_rank_wins_loses.append(int(entered_values[index]))
            # Ελέγχει πως η τελευταία τιμή που μπήκε στη λίστα 
            # δεν είναι αρνητική. Ο έλεγχος για μη αποδοχή μηδενικής θέσης
            # γίνεται από την insert_player_at_position()
            if entered_rank_wins_loses[-1] < 0:
                raise(ValueError)
            
        except ValueError:
            msg.showerror(
                parent=window, 
                title='Ειδοποίηση', 
                message="Παρακαλώ, εισάγετε ακέραιο θετικό αριθμό για {0}".format(tag)
                )
            # Επαναφέρει το πεδίο στην τελευταία αποθηκευμένη τιμή
            window.entry_fields[index].delete(0,'end')
            window.entry_fields[index].insert(0, window.values[index])
            return
    
    # Έλεγχος πως εισάγεται μόνο μια μη κενή λέξη σε Όνομα και Επώνυμο.
    for index in range(1,3):
        if len(entered_values[index].split(' ')) > 1 or entered_values[index] =='':
            if index == 1:
                tag = 'όνομα'
                # Αντικαθιστά τα κενά με παύλες
                window.entry_fields[1].delete(0, 'end')
                entered_values[index] = entered_values[index].replace(' ', '-')
                window.entry_fields[1].insert(0, entered_values[index])
            else:
                tag = 'επώνυμο'
                window.entry_fields[2].delete(0, 'end')
                entered_values[index] = entered_values[index].replace(' ', '-')
                window.entry_fields[2].insert(0, entered_values[index])

            msg.showerror(
                parent = window,
                title = 'Ειδοποίηση',
                message = '''Παρακαλώ εισάγετε μόνο μία λέξη χωρίς κενά για το {0}.
Αν χρειάζεται, παρακαλώ χρησιμοποιήστε παύλες.'''.format(tag)
                )
            return
    # Έλεγχος πως η εισαγωγή περιέχει 2 '/', και διαχωρισμός της
    entered_date = entered_values[-1].split('/')
    if len(entered_date) != 3:
        window.entry_fields[-1].delete(0,'end')
        window.entry_fields[-1].insert(0, window.values[-1])
        msg.showerror(
            parent = window,
            title = 'Ειδοποίηση', 
            message = 'Παρακαλώ εισάγετε ημερομηνία στη μορφή 16/6/2025'
            )
        return
    # Έλεγχος πως τα επιμέρους μέρη της εισαχθείσας ημερομηνίας
    # συμβαδίζουν με την ημερομηνία (πχ μέρες <=31)
    try:
        entered_datetime_obj = datetime.date(
            int(entered_date[2]),
            int(entered_date[1]),
            int(entered_date[0])
            )
        # Έλεγχος εισαγωγής μελλοντικής ημερομηνίας τελευταίας δραστηριότητας.
        today = datetime.date.today()
        if entered_datetime_obj > today:
            msg.showerror(
                parent = window,
                title = 'Ειδοποίηση', 
                message = 'Μη αποδεκτή μελλοντική ημερομηνία τελευταίας δραστηριότητας.'
                )
            return
    except ValueError:
        msg.showerror(
            parent = window,
            title = 'Ειδοποίηση', 
            message = 'Παρακαλώ ελέγξτε την ημερομηνία και ξαναπροσπαθήστε.'
            )
        window.entry_fields[-1].delete(0,'end')
        window.entry_fields[-1].insert(0, window.values[-1])
        return

    # Απαραίτητο για μετατροπή των '01' σε 1 και μετά σε '1' για να μην
    # έχει λάθος η σύγκριση νέου δεδομένου
    entered_values[0] = str(entered_rank_wins_loses[0])
    entered_values[3] = str(entered_rank_wins_loses[1])
    entered_values[4] = str(entered_rank_wins_loses[2])
    
    # Έλεγχος για στοιχεία που αλλάχθηκαν, πλην θέσης
    index = 0
    # Σημαία για αλλαγή λοιπών στοιχείων
    new_values_flag = False
    # Σημαία για αλλαγή θέσης
    new_rank_flag = True
    new_values = [
        None,
        None,
        None,
        None,
        None,
        None
        ]
    for entered_value in entered_values:
        if entered_value != window.values[index]:
            # To new_values_flag γίνεται True μόνο αν η αλλαγή δεν αφορά τη θέση
            if index != 0:
                new_values_flag = True
            new_values[index] = entered_value
        index += 1
    # Ελέγχει αν εισήχθη νέα θέση. Αν δεν εισήχθη νέα θέση, λαμβάνει
    # την προηγούμενη θέση για αναζήτηση παίκτη.
    if new_values[0] is None:
        new_values[0] = entered_values[0]
        new_rank_flag = False
    
    # Ανανέωση των στοιχείων του παίκτη πριν την αλλαγή θέσης
    if new_values_flag:    
        # Χρησιμοποιείται η προηγούμενη θέση window.values[0]
        update_info(
            window.values[0],
            *new_values[1:]
            )
    
        msg.showinfo(
            parent = window,
            title = 'Ειδοποίηση',
            message = 'Τα δεδομένα αποθηκεύτηκαν επιτυχώς.'
            )
        
    # Ανανέωση θέσης
    if new_rank_flag:
        if change_position(window.values[0], new_values[0]):
            msg.showinfo(
                parent=window,
                title='Ειδοποίηση',
                message='Η αλλαγή θέσης καταχωρήθηκε.'
                )
        else:
            name = new_values[1] if new_values[1] is not None else window.values[1]
            surname = new_values[2] if new_values[2] is not None else window.values[2]
            msg.showerror(
                parent=window,
                title='Ειδοποίηση', 
                message=f"Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη {name} {surname}.\nΗ αλλαγή θέσης ακυρώθηκε."
                )
            
    window.destroy()
    # Ανανέωση δεδομένων πίνακα
    fill_tree(tree)
    return
    
    
def on_exit_click(main_window):
    """
    Συνάρτηση κουμπιού κυρίου παραθύρου για έξοδο.
    Τερματίζει τη λειτουργία της εφαρμογής και κλείνει το κύριο παράθυρο.
    
    
    Args:
        main_window (Tk Object): Κύριο παράθυρο της εφαρμογής.
        
    Returns:
        None.
    """
    main_window.destroy()

def start_app():
    main_window = tk.Tk()
    main_window.geometry('600x600+650+150')
    main_window.title("Tennis Ladder App")
    main_window.default_font = 'Times 16'
    
    ttk.Separator(
        main_window,
        orient='horizontal'
        ).pack(
            fill='x',
            pady=15
            )
    # Λίστα με τα κουμπιά
    buttons = [
        ('Αρχικοποίηση κατάταξης', on_initialize_click),
        ('Προσθήκη παίκτη', on_add_player),
        ('Διαγραφή παίκτη', on_del_player),
        ('Έλεγχος και καταγραφή αποτελέσματος πρόκλησης', on_challenge_click),
        ('Έλεγχος κατάταξης για αδρανείς παίκτες', on_inactive_check_click),
        ('Εμφάνιση κατάταξης', on_show_ranking_click),
        ('Έξοδος', on_exit_click)
    ]
    for label, function in buttons:
        tk.Button(
            main_window,
            text = label,
            font = main_window.default_font,
            command = lambda f=function: f(main_window),
            relief = 'groove', 
            bd = 10
            ).pack(
                fill = 'x',
                padx = 50,
                pady = 10)
    tk.Label(
        main_window, 
        text = 'Made by Black Baron', 
        font = (
            'Old English Text MT',
            12
            ),
        justify = 'left'
        ).pack(
            side = 'right'
            )
    create_table()
    main_window.mainloop()

if __name__ == '__main__':
    start_app()
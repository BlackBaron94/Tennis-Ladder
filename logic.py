# -*- coding: utf-8 -*-

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


def fill_tree(tree, icon):
    """
    Ενημερώνει το Treeview του UI εκχωρώντας σε αυτό τα στοιχεία όλων των παικτών.
    
    
    Args:
        tree (Treeview Object): Πίνακας στον οποίο μπαίνουν τα δεδομένα της ΒΔ.
        icon (PhotoImage Object): Εικονίδιο μολυβιού για στήλη επεξεργασία.
        
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
    
    for data in all_DB_data.fetchall():
        ranking_list.append(data)
    
    # Λίστα για τη διατήρηση αναφορών στην εικόνα για αποφυγή 
    # απώλειας εικόνας λόγω garbage-collection
    tree.image_refs = []
    # Εισάγει τα δεδομένα στο tree
    for item in ranking_list:
        tree.insert('', 'end', text = ' ', image = icon, values=item)
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
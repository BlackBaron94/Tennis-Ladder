# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox as msg, PhotoImage
import datetime
from logic import (
    is_position_empty,
    initialization,
    insert_player_at_end,
    insert_player_at_position,
    dbconnect,
    delete_player,
    check_challenge,
    win,
    check_ranking_for_decay,
    fill_tree,
    update_info,
    change_position,
    create_table,
)


def start_app():
    main_window = tk.Tk()
    main_window.geometry("600x600+650+150")
    main_window.title("Tennis Ladder App")
    main_window.default_font = "Times 16"

    ttk.Separator(main_window, orient="horizontal").pack(fill="x", pady=15)
    # Λίστα με τα κουμπιά
    buttons = [
        ("Αρχικοποίηση κατάταξης", on_initialize_click),
        ("Προσθήκη παίκτη", on_add_player),
        ("Διαγραφή παίκτη", on_del_player),
        ("Έλεγχος και καταγραφή αποτελέσματος πρόκλησης", on_challenge_click),
        ("Έλεγχος κατάταξης για αδρανείς παίκτες", on_inactive_check_click),
        ("Εμφάνιση κατάταξης", on_show_ranking_click),
        ("Έξοδος", on_exit_click),
    ]
    for label, function in buttons:
        tk.Button(
            main_window,
            text=label,
            font=main_window.default_font,
            command=lambda f=function: f(main_window),
            relief="groove",
            bd=10,
        ).pack(fill="x", padx=50, pady=10)
    tk.Label(
        main_window,
        text="Made by Black Baron",
        font=("Old English Text MT", 12),
        justify="left",
    ).pack(side="right")

    create_table()
    main_window.focus_set()
    main_window.mainloop()
    return


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
            title="Ειδοποίηση",
            message="""Ο πίνακας κατάταξης περιέχει ήδη παίκτες και δεν μπορεί να αρχικοποιηθεί τυχαία. 
Παρακαλώ, διαγράψτε όλους τους παίκτες ή προσθέστε παίκτες χρησιμοποιώντας κάποια από τις επιλογές.""",
        )
        return

    # Παράθυρο διαλόγου αρχικοποίησης
    initialize_dialog = tk.Toplevel(main_window)
    initialize_dialog.title("Αρχικοποίηση λίστας")
    initialize_dialog.geometry("400x500+700+350")
    # Keybind για κλείσιμο παραθύρου με Escape
    initialize_dialog.bind(
        "<Escape>", lambda event: initialize_dialog.destroy()
    )

    # Μεταβλητή για αποθήκευση παικτών προς αρχικοποίηση ως πεδίο του παραθύρου
    initialize_dialog.players = []
    # Δυναμική μεταβλητή StringVar για προβολή εισαχθέντων
    # παικτών καθώς αυτοί εισάγονται, ως πεδίο του παραθύρου
    initialize_dialog.initialization_list_label = tk.StringVar()
    initialize_dialog.initialization_list_label.set("Κενή Λίστα Παικτών")
    # Πεδίο εισαγωγής
    initialize_dialog.initialization_entry = tk.Entry(
        initialize_dialog,
        justify="center",
        font=main_window.default_font,
        selectborderwidth=3,
    )
    initialize_dialog.initialization_entry.pack(pady=10)
    initialize_dialog.initialization_entry.focus_set()
    # Keybind για καταχώρηση παίκτη στη λίστα με Enter
    initialize_dialog.initialization_entry.bind(
        "<Return>",
        lambda event: on_initialize_add_player_click(initialize_dialog),
    )
    # Κουμπί καταχώρησης παίκτη στη λίστα
    tk.Button(
        initialize_dialog,
        text="Καταχώρηση Παίκτη",
        font=main_window.default_font,
        command=lambda: on_initialize_add_player_click(initialize_dialog),
    ).pack(pady=5)
    # Κουμπί τέλους καταχωρήσεων και αρχικοποίησης κατάταξης
    tk.Button(
        initialize_dialog,
        text="Τέλος Καταχωρήσεων",
        font=main_window.default_font,
        command=lambda: on_finalize_initialization_click(initialize_dialog),
    ).pack(pady=5)
    ttk.Separator(initialize_dialog, orient="horizontal").pack(
        fill="x", pady=15
    )
    # Δυναμικό Label που αλλάζει με τις καταχωρήσεις
    tk.Label(
        initialize_dialog,
        textvariable=initialize_dialog.initialization_list_label,
        font=main_window.default_font,
        justify="center",
    ).pack()
    initialize_dialog.mainloop()
    return


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
    window.initialization_entry.delete(0, "end")
    player = name.split(sep=" ")

    # Περίπτωση που εισαχθούν πάνω απο 1 κενά
    if len(player) != 2:
        msg.showerror(
            master=window,
            parent=window,
            title="Ειδοποίηση",
            message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.",
        )
        return
    # Προσθήκη παίκτη στη λίστα
    window.players.append(player)
    # Ελέγχει αν το δυναμικό Label έδειχνε κενή λίστα και απαιτεί πρώτη
    # μορφοποίηση κι όχι απλά προσθήκη παίκτη σε αυτήν
    if window.initialization_list_label.get() == "Κενή Λίστα Παικτών":
        window.initialization_list_label.set("Λίστα Παικτών\n")
    # Παίρνει τα δεδομένα που είχε το δυναμικό Label
    # για να προσθέσει το νέο δεδομένο
    string = "\n".join([window.initialization_list_label.get(), name])
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
            title="Ειδοποίηση",
            message="Οι παίκτες καταχωρήθηκαν τυχαία στην κατάταξη.",
        )
        window.destroy()
        return

    else:
        window.destroy()
        # Σε περίπτωση που ήταν κενή ενημερώνει τον χρήστη με το κατάλληλο μήνυμα
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Δε δημιουργήθηκε κατάταξη καθώς δεν εισάγατε ονόματα.",
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
        title="Προσθήκη Παίκτη",
        message="""Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση;""",
    )
    if position_entry_answer == None:
        msg.showinfo(
            master=main_window,
            title="Ειδοποίηση",
            message="Η προσθήκη παίκτη ακυρώθηκε.",
        )
        return

    # Παράθυρο διαλόγου εισαγωγής ονοματεπωνύμου παίκτη
    name_entry_dialog = tk.Toplevel(main_window)
    name_entry_dialog.geometry("550x150+650+350")
    name_entry_dialog.title("Προσθήκη Παίκτη")
    name_entry_dialog.bind(
        "<Escape>", lambda event: name_entry_dialog.destroy()
    )
    # Ορίζεται ως πεδίο του αντικειμένου Top Level για να περαστεί
    # στις συναρτήσεις που την χρησιμοποιούν
    name_entry_dialog.position_entry_answer = position_entry_answer
    tk.Label(
        name_entry_dialog,
        font=main_window.default_font,
        text="Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε: ",
    ).pack(pady=5)
    # Πεδίο εισαγωγής
    name_entry_dialog.name_entry = tk.Entry(
        name_entry_dialog, font=main_window.default_font, justify="center"
    )
    name_entry_dialog.name_entry.pack(pady=5)
    name_entry_dialog.name_entry.focus_set()
    name_entry_dialog.name_entry.bind(
        "<Return>", lambda event: on_new_player_name_submit(name_entry_dialog)
    )
    # Κουμπί εισαγωγής ονοματεπωνύμου παίκτη
    tk.Button(
        name_entry_dialog,
        text="Προσθήκη",
        font=main_window.default_font,
        command=lambda: on_new_player_name_submit(name_entry_dialog),
    ).pack(pady=5)

    name_entry_dialog.mainloop()
    return


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
    window.name_entry.delete(0, "end")

    player_name = player_name_entry.split(sep=" ")
    # Έλεγχος σωστής εισαγωγής ονοματεπωνύμου
    if len(player_name) != 2:
        # Ενημέρωση χρήστη με κατάλληλο μήνυμα
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.",
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
            title="Ειδοποίηση",
            message=f"Ο {name} {surname} τοποθετήθηκε επιτυχώς στην θέση #{new_last_place}.",
        )
        window.destroy()
    # Αν ο χρήστης απάντησε πως θέλει να βάλει σε συγκεκριμένη θέση τον παίκτη
    elif window.position_entry_answer == True:
        # Δημιουργία παραθύρου διαλόγου
        default_font = "Times 16"
        position_entry_dialog = tk.Toplevel(window)
        position_entry_dialog.geometry("600x150+625+450")
        position_entry_dialog.title("Προσθήκη Παίκτη σε Θέση")
        position_entry_dialog.bind(
            "<Escape>", lambda event: position_entry_dialog.destroy()
        )

        tk.Label(
            position_entry_dialog,
            font=default_font,
            text="Δώστε τη θέση κατάταξης του παίκτη που θέλετε να προσθέσετε: ",
        ).pack(pady=5)
        # Πεδίο εισαγωγής

        position_entry_dialog.position_entry = tk.Entry(
            position_entry_dialog, font=default_font, justify="center"
        )
        position_entry_dialog.position_entry.pack(pady=5)
        position_entry_dialog.position_entry.focus_set()
        position_entry_dialog.position_entry.bind(
            "<Return>",
            lambda event: on_new_player_position_submit(
                name, surname, position_entry_dialog
            ),
        )
        # Κουμπί καταχώρησης θέσης εισαγωγής παίκτη προς προσθήκη
        tk.Button(
            position_entry_dialog,
            font=default_font,
            text="OK",
            command=lambda: on_new_player_position_submit(
                name, surname, position_entry_dialog
            ),
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
        window.position_entry.delete(0, "end")
        if insert_player_at_position(player_position, name, surname):
            msg.showinfo(
                parent=window,
                title="Ειδοποίηση",
                message=f"Ο παίκτης {name} {surname} τοποθετήθηκε επιτυχώς στη θέση #{player_position}.",
            )
        else:
            msg.showerror(
                parent=window,
                title="Ειδοποίηση",
                message=f"Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη {name} {surname}.",
            )
        window.destroy()
    except ValueError:
        # Ενημέρωση χρήστη για μη αποδεκτή εισαγωγή θέση (όχι ακέραιος)
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.",
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
            title="Ειδοποίηση",
            message="Η κατάταξη δεν περιέχει παίκτες!",
        )
    # Η κατάταξη περιέχει παίκτες
    else:
        # Δημιουργία παραθύρου διαλόγου
        deletion_dialog = tk.Toplevel(main_window)
        deletion_dialog.geometry("550x200+650+450")
        deletion_dialog.title("Διαγραφή Παίκτη")
        deletion_dialog.bind(
            "<Escape>", lambda event: deletion_dialog.destroy()
        )
        tk.Label(
            deletion_dialog,
            text="Δώστε τη θέση κατάταξης του παίκτη που θέλετε να διαγράψετε: ",
            font="Times 14",
        ).pack(pady=20)
        # Πεδίο εισαγωγής

        deletion_dialog.deletion_entry = tk.Entry(
            deletion_dialog, justify="center", font=main_window.default_font
        )
        deletion_dialog.deletion_entry.pack(pady=5)
        deletion_dialog.deletion_entry.focus_set()
        deletion_dialog.deletion_entry.bind(
            "<Return>", lambda event: on_dialog_delete_click(deletion_dialog)
        )
        # Κουμπί διαγραφής
        tk.Button(
            deletion_dialog,
            text="Διαγραφή",
            font="Times 16",
            command=lambda: on_dialog_delete_click(deletion_dialog),
        ).pack(side="left", padx=60)
        # Κουμπί ακύρωσης διαγραφής
        tk.Button(
            deletion_dialog,
            text="Ακύρωση",
            font="Times 16",
            command=deletion_dialog.destroy,
        ).pack(side="right", padx=60)

        deletion_dialog.mainloop()
    return


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
    except ValueError:
        # Ειδοποίηση χρήστη για λάθος εισαγωγή θέσης
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.",
        )
        window.deletion_entry.delete(0, "end")

    # Έλεγχος αν η θέση περιέχει άτομο και ενημέρωση με μήνυμα σφάλματος
    if is_position_empty(index):
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Δεν υπάρχει παίκτης στη θέση που προσπαθείτε να κάνετε διαγραφή.",
        )
    else:
        my_conn = dbconnect("tennis_club.db")
        c = my_conn.cursor()
        # Λήψη δεδομένων προς διαγραφή παίκτη
        playerDBData = c.execute(
            "SELECT * FROM ranking WHERE Position = ?;", (index,)
        ).fetchall()
        my_conn.commit()
        my_conn.close()
        # Παράθυρο επιβεβαίωσης διαγραφής
        confirmation = msg.askyesno(
            parent=window,
            title="Διαγραφή Παίκτη",
            message=f"""ΠΡΟΣΟΧΉ!!!! Η διαγραφή είναι οριστική κι αμετάκλητη!
Θα χαθούν ΌΛΑ τα δεδομένα του παίκτη.
Θέλετε σίγουρα να διαγράψετε τον παίκτη {playerDBData[0][1]} {playerDBData[0][2]}; """,
        )
        # Ακύρωση διαγραφής και ενημέρωση χρήστη
        if confirmation == False:
            msg.showerror(
                parent=window,
                title="Ειδοποίηση",
                message="Η διαγραφή ακυρώθηκε από τον χρήστη.",
            )
            window.deletion_entry.delete(0, "end")
            return
        else:
            delete_player(index)
            # Μήνυμα ειδοποίησης επιτυχούς διαγραφής
            msg.showinfo(
                parent=window,
                title="Ειδοποίηση",
                message=f"Ο παίκτης στη θέση #{index} διαγράφηκε επιτυχώς.",
            )
            window.deletion_entry.delete(0, "end")

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
            title="Ειδοποίηση",
            message="Η κατάταξη δεν περιέχει παίκτες!",
        )
    elif is_position_empty(2):
        msg.showerror(
            master=main_window,
            title="Ειδοποίηση",
            message="Η κατάταξη περιέχει μόνο έναν παίκτη άρα δεν ορίζεται πρόκληση.",
        )
    # Περιέχει πάνω από 1 παίκτη
    else:
        # Δημιουργία παραθύρου διαλόγου για την πρόκληση
        challenge_dialog = tk.Toplevel(main_window)
        challenge_dialog.geometry("650x200+650+450")
        challenge_dialog.title("Καταγραφη Πρόκλησης")
        challenge_dialog.bind(
            "<Escape>", lambda event: challenge_dialog.destroy()
        )
        # Τίθεται ως δυναμικό Label για να αλλάζει
        # μετά την καταχώρηση του πρώτου παίκτη
        challenge_dialog.challenge_label = tk.StringVar()
        challenge_dialog.challenge_label.set(
            "Δώστε τη θέση κατάταξης του παίκτη που προκαλεί: "
        )
        tk.Label(
            master=challenge_dialog,
            textvariable=challenge_dialog.challenge_label,
            font=main_window.default_font,
        ).pack(pady=10)
        # Πεδίο εισαγωγής
        challenge_dialog.challenge_entry = tk.Entry(
            master=challenge_dialog,
            justify="center",
            font=main_window.default_font,
        )
        challenge_dialog.challenge_entry.pack(pady=10)
        challenge_dialog.challenge_entry.focus_set()
        challenge_dialog.challenge_entry.bind(
            "<Return>",
            lambda event: on_dialog_challenge_click(challenge_dialog),
        )
        # Μεταβλητή που αποθηκεύει τις θέσεις των παικτών
        # που εμπλέκονται στην πρόκληση ως πεδίου του Top Level object
        challenge_dialog.players_in_challenge = []
        # Κουμπί καταχώρησης θέσης παίκτη που εμπλέκεται στην πρόκληση
        tk.Button(
            master=challenge_dialog,
            text="OK",
            font=main_window.default_font,
            command=lambda: on_dialog_challenge_click(challenge_dialog),
        ).pack(pady=10)
        challenge_dialog.mainloop()

    return


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
                title="Ειδοποίηση",
                message=f"Δεν υπάρχει παίκτης στη θέση #{window.challenge_entry.get()}",
            )
            return
        # Προσθήκη εισαχθείσας θέσης στη λίστα παικτών που εμπλέκονται
        window.players_in_challenge.append(int(window.challenge_entry.get()))
        window.challenge_entry.delete(0, "end")
    except ValueError:
        # Ενημέρωση χρήστη για εισαγωγή μη ακεραίου
        # Ο έλεγχος των τιμών της πρόκλησης γίνεται από το try block και
        # από την check_challenge()
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.",
        )
        return
    # Εάν έχει λάβει μόνο έναν παίκτη, ενημερώνει το δυναμικό Label
    if len(window.players_in_challenge) == 1:
        window.challenge_label.set(
            "Δώστε τη θέση κατάταξης του παίκτη που δέχεται την πρόκληση:"
        )
    # Εάν έχει λάβει 2 παίκτες, καλεί την check_challenge()
    elif len(window.players_in_challenge) == 2:
        return_dict = check_challenge(
            window.players_in_challenge[0], window.players_in_challenge[1]
        )
        if return_dict["success"] == False:
            msg.showerror(
                parent=window,
                title="Ειδοποίηση",
                message=return_dict["message"],
            )
        else:
            answer = msg.askyesnocancel(
                parent=window,
                title="Αποτέλεσμα Αγώνα",
                message=f"""Η πρόκληση είναι αποδεκτή.
Νίκησε ο παίκτης στη θέση #{window.players_in_challenge[0]} που έκανε την πρόκληση;""",
            )

            if answer == True:
                change_flag = win(
                    window.players_in_challenge[0],
                    window.players_in_challenge[1],
                )
            elif answer == False:
                change_flag = win(
                    window.players_in_challenge[1],
                    window.players_in_challenge[0],
                )
            # Αν ο χρήστης κλείσει το παράθυρο χωρίς να απαντήσει για νικητή
            elif answer == None:
                msg.showerror(
                    parent=window,
                    title="Ειδοποίηση",
                    message="Ο αγώνας δεν καταγράφηκε, ακύρωση από τον χρήστη.",
                )
                window.destroy()
                # Return εδώ για να μην εντοπίσει πρόβλημα change_flag undefined
                return

            if change_flag:
                # Ενημέρωση χρήστη για αλλαγές στην κατάταξη
                msg.showinfo(
                    parent=window,
                    title="Ειδοποίηση",
                    message="Το παιχνίδι καταγράφηκε επιτυχώς και η κατάταξη ανανεώθηκε!",
                )
            else:
                msg.showinfo(
                    parent=window,
                    title="Ειδοποίηση",
                    message="Το παιχνίδι καταγράφηκε επιτυχώς, χωρίς αλλαγή στην κατάταξη!",
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
            title="Ειδοποίηση",
            message="Η κατάταξη δεν περιέχει παίκτες!",
        )
    else:
        decay_result = check_ranking_for_decay()
    # Αν το immune δεν είναι None
    if decay_result["immune"] is not None:
        # Μήνυμα ειδοποίησης χρήστη πως ο παίκτης δεν πέφτει περαιτέρω
        msg.showinfo(
            master=main_window,
            title="Ειδοποίηση",
            message="Ο παικτης {0} {1} είναι ήδη στην τελευταία θέση και δεν πέφτει περαιτέρω.".format(
                decay_result["immune"][0], decay_result["immune"][1]
            ),
        )
    msg.showinfo(
        master=main_window, title="Ειδοποίηση", message=decay_result["message"]
    )
    return


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
            title="Ειδοποίηση",
            message="Η κατάταξη δεν περιέχει παίκτες!",
        )
    else:
        # Δημιουργεί παράθυρο με tree για προβολή κατάταξης
        ranking_window = tk.Toplevel(main_window)
        ranking_window.title("Πίνακας Κατάταξης")
        ranking_window.geometry("1250x800+350+0")
        ranking_window.bind("<Escape>", lambda event: ranking_window.destroy())
        tree_style = ttk.Style()
        tree_style.configure(
            "mystyle.Treeview", font=main_window.default_font, rowheight=30
        )
        tree_style.configure(
            "mystyle.Treeview.Heading",
            font=main_window.default_font,
        )
        # Λίστα με όνομα στήλης και width της
        columns_widths = [
            ("#0", 57),
            ("Θέση", 10),
            ("Όνομα", 150),
            ("Επίθετο", 225),
            ("Νίκες", 10),
            ("Ήττες", 10),
            ("Ημ/νία Δραστηριότητας", 200),
        ]
        # Διατήρηση ονομάτων στηλών (πλην #0)
        column_names = [col[0] for col in columns_widths[1:]]
        # Δημιουργία Treeview με τις απαιτούμενες στύλες και μορφοποιήσεις
        tree = ttk.Treeview(
            ranking_window,
            style="mystyle.Treeview",
            columns=column_names,
            show="tree headings",
        )
        for column_name, column_width in columns_widths:
            tree.column(column_name, anchor="center", width=column_width)
        for column_name, column_width in columns_widths:
            # Η στήλη #0 είναι η μόνη που το index != text
            if column_name == "#0":
                tree.heading(column_name, text="Επεξεργασία")
                continue
            tree.heading(column_name, text=column_name)
        icon = PhotoImage(file="pencil-button.png")
        # Καλεί την fill_tree() να γεμίσει το tree με τα δεδομένα της ΒΔ
        fill_tree(tree, icon)
        tree.pack(fill="both", expand=1)
        # Εντοπίζει clicks στο παράθυρο
        tree.bind(
            "<Button-1>", lambda event: on_tree_click(event, tree, main_window)
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
    if col == "#0" and region == "tree" and row:
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
    edit_details_dialog.geometry("350x550+650+150")
    edit_details_dialog.bind(
        "<Escape>", lambda event: edit_details_dialog.destroy()
    )
    edit_details_dialog.values = tree.item(item_id, "values")
    columns = [
        "Θέση",
        "Όνομα",
        "Επώνυμο",
        "Νίκες",
        "Ήττες",
        "Ημ/νία Δραστηριότητας",
    ]
    col_index = 0
    # Μεταβλητή στην οποία αποθηκεύεται αναφορά στα Entries
    edit_details_dialog.entry_fields = []
    for value in edit_details_dialog.values:
        tk.Label(
            edit_details_dialog,
            font=main_window.default_font,
            text=columns[col_index],
        ).pack(pady=5)
        entry = tk.Entry(
            edit_details_dialog,
            font=main_window.default_font,
            justify="center",
        )
        entry.insert(0, value)
        entry.pack(pady=5)
        edit_details_dialog.entry_fields.append(entry)
        col_index += 1

    edit_details_dialog.focus_set()
    edit_details_dialog.bind(
        "<Return>", lambda event: on_edit_save(edit_details_dialog, tree)
    )

    tk.Button(
        edit_details_dialog,
        font=main_window.default_font,
        text="Αποθήκευση",
        command=lambda: on_edit_save(edit_details_dialog, tree),
    ).pack(pady=5)
    edit_details_dialog.mainloop()
    return


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
        (0, "την θέση κατάταξης."),
        (3, "τις νίκες."),
        (4, "τις ήττες."),
    ]
    entered_rank_wins_loses = []
    for index, tag in values_index_tag:
        try:
            entered_rank_wins_loses.append(int(entered_values[index]))
            # Ελέγχει πως η τελευταία τιμή που μπήκε στη λίστα
            # δεν είναι αρνητική. Ο έλεγχος για μη αποδοχή μηδενικής θέσης
            # γίνεται από την insert_player_at_position()
            if entered_rank_wins_loses[-1] < 0:
                raise (ValueError)

        except ValueError:
            msg.showerror(
                parent=window,
                title="Ειδοποίηση",
                message="Παρακαλώ, εισάγετε ακέραιο θετικό αριθμό για {0}".format(
                    tag
                ),
            )
            # Επαναφέρει το πεδίο στην τελευταία αποθηκευμένη τιμή
            window.entry_fields[index].delete(0, "end")
            window.entry_fields[index].insert(0, window.values[index])
            return

    # Έλεγχος πως εισάγεται μόνο μια μη κενή λέξη σε Όνομα και Επώνυμο.
    for index in range(1, 3):
        if (
            len(entered_values[index].split(" ")) > 1
            or entered_values[index] == ""
        ):
            if index == 1:
                tag = "όνομα"
                # Αντικαθιστά τα κενά με παύλες
                window.entry_fields[1].delete(0, "end")
                entered_values[index] = entered_values[index].replace(" ", "-")
                window.entry_fields[1].insert(0, entered_values[index])
            else:
                tag = "επώνυμο"
                window.entry_fields[2].delete(0, "end")
                entered_values[index] = entered_values[index].replace(" ", "-")
                window.entry_fields[2].insert(0, entered_values[index])

            msg.showerror(
                parent=window,
                title="Ειδοποίηση",
                message="""Παρακαλώ εισάγετε μόνο μία λέξη χωρίς κενά για το {0}.
Αν χρειάζεται, παρακαλώ χρησιμοποιήστε παύλες.""".format(
                    tag
                ),
            )
            return
    # Έλεγχος πως η εισαγωγή περιέχει 2 '/', και διαχωρισμός της
    entered_date = entered_values[-1].split("/")
    if len(entered_date) != 3:
        window.entry_fields[-1].delete(0, "end")
        window.entry_fields[-1].insert(0, window.values[-1])
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Παρακαλώ εισάγετε ημερομηνία στη μορφή 16/6/2025",
        )
        return
    # Έλεγχος πως τα επιμέρους μέρη της εισαχθείσας ημερομηνίας
    # συμβαδίζουν με την ημερομηνία (πχ μέρες <=31)
    try:
        entered_datetime_obj = datetime.date(
            int(entered_date[2]), int(entered_date[1]), int(entered_date[0])
        )
        # Έλεγχος εισαγωγής μελλοντικής ημερομηνίας τελευταίας δραστηριότητας.
        today = datetime.date.today()
        if entered_datetime_obj > today:
            msg.showerror(
                parent=window,
                title="Ειδοποίηση",
                message="Μη αποδεκτή μελλοντική ημερομηνία τελευταίας δραστηριότητας.",
            )
            return
    except ValueError:
        msg.showerror(
            parent=window,
            title="Ειδοποίηση",
            message="Παρακαλώ ελέγξτε την ημερομηνία και ξαναπροσπαθήστε.",
        )
        window.entry_fields[-1].delete(0, "end")
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
    new_values = [None, None, None, None, None, None]
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
        update_info(window.values[0], *new_values[1:])

        msg.showinfo(
            parent=window,
            title="Ειδοποίηση",
            message="Τα δεδομένα αποθηκεύτηκαν επιτυχώς.",
        )

    # Ανανέωση θέσης
    if new_rank_flag:
        if change_position(window.values[0], new_values[0]):
            msg.showinfo(
                parent=window,
                title="Ειδοποίηση",
                message="Η αλλαγή θέσης καταχωρήθηκε.",
            )
        else:
            name = (
                new_values[1]
                if new_values[1] is not None
                else window.values[1]
            )
            surname = (
                new_values[2]
                if new_values[2] is not None
                else window.values[2]
            )
            msg.showerror(
                parent=window,
                title="Ειδοποίηση",
                message=f"Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη {name} {surname}.\nΗ αλλαγή θέσης ακυρώθηκε.",
            )

    window.destroy()
    # Ανανέωση δεδομένων πίνακα
    icon = PhotoImage(file="pencil-button.png")
    fill_tree(tree, icon)
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
    return

<a id="readme-top"></a>
# Tennis Ladder Project

## Περιεχόμενα
- [Περιγραφή Project](#περιγραφή-project)
- [Οδηγίες Εγκατάστασης](#οδηγίες-εγκατάστασης)
- [Χρήση](#χρήση)
- [Μελλοντικές Προσθήκες](#μελλοντικές-προσθήκες)
- [Επικοινωνία](#επικοινωνία)

## Περιγραφή Project

Η εφαρμογή δημιουργήθηκε με σκοπό να διατηρεί και να επεξεργάζεται δεδομένα μιας κατάταξης Τέννις. Οι δυνατότητες περιλαμβάνουν προσθήκη, 
διαγραφή παίκτη, τυχαιοποιημένη αρχική εισαγωγή παικτών, έλεγχο και καταγραφή πρόκλησης και 
αποτελεσμάτων αγώνων. Επιπλέον, υπάρχει λειτουργία ελέγχου αδράνειας.

### Τεχνολογίες και βιβλιοθήκες που χρησιμοποιήθηκαν

* [![Python][python.org]][Python-url]
* [![tkinter][tkinter.python]][tkinter-url]
* [![SQLite3][sqlite3.python]][sqlite3-url]
* [![datetime][datetime.python]][datetime-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Οδηγίες Εγκατάστασης


- Executable

Για να τρέξει το onefile .exe δεν υπάρχουν προαπαιτούμενα. Κάνοντας clone το repo είστε έτοιμοι!

1. Clone του repo
   ```sh
   git clone https://github.com/BlackBaron94/Tennis-Ladder-UI-Upgrade.git
   ```

- Κώδικας

Για να τρέξει το αρχείο .py χρειάζεται εγκατεστημένη έκδοση 3. Python καθώς και το πακέτο βιβλιοθήκης tkinter

2. Έλεγχος εγκατεστημένης έκδοσης Python
   ```ssh
   python --version
   ```
3. Έλεγχος εγκατάστασης pip
   ```sh
   pip -v
   ```

4. Εγκατάταση πακέτου tkinter
   ```sh
   pip install tk
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Χρήση

Μπορείτε να παρακολουθήσετε video demo [εδώ](https://drive.google.com/file/d/1DFihKx1Vyke6czRwdj_89D8w2RjAyyhL/view?usp=drive_link).

Εναλλακτικά, παρακάτω φαίνονται παραδείγματα χρήσης με εικόνες.
Αυτό είναι το κύριο μενού της εφαρμογής.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Main-Menu.jpg" alt="App Main Menu" width="500"/>
</div>

Ξεκινώντας με άδεια κατάταξη, μπορούμε είτε να προσθέσουμε έναν έναν τους παίκτες σε θέση που θέλουμε είτε να 
επιλέξουμε τυχαιοποιημένη αρχικοποίηση κατάταξης με πολλαπλή εισασγωγή. Η τυχαιποιημένη αρχικοποίηση είναι διαθέσιμη μόνο
όταν η κατάταξη είναι άδεια.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Initialization-Empty-List.jpg" alt="Tennis-Initialization-Empty-List" width="500"/>
</div>

Εισάγοντας παίκτες, η λίστα γεμίζει με τα ονόματα, δείχνοντάς μας τι έχουμε εισάγει μέχρι τώρα.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Initialization-List.jpg" alt="Tennis-Initialization-List" width="500"/>
</div>

Εμφανίζοντας την κατάταξη βλέπουμε την τυχαιοποίηση των εισαγωγών.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Randomized-Ranking.jpg" alt="Tennis-Randomized-Ranking" width="500"/>
</div>

Μπορούμε να προσθέσουμε παίκτη είτε σε συγκεκριμένη θέση είτε στο τέλος της κατάταξης.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Add-Player-Question.jpg" alt="Tennis-Add-Player-Question" width="500"/>
</div>

Αυτό είναι το παράθυρο εισαγωγής παίκτη σε συγκεκριμένη θέση.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Added-Player.jpg" alt="Tennis-Added-Player" width="500"/>
</div>

Η διαγραφή παίκτη γίνεται με τη θέση κατάταξης και υπάρχει επιβεβαίωση διαγραφής που παρουσιάζει
το όνομα του εν λόγω παίκτη.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Delete-Player-Question.jpg" alt="Tennis-Delete-Player-Question" width="500"/>
</div>

Για έλεγχο και καταγραφή αποτελέσματος πρόκλησης, εισάγουμε πρώτα τη θέση του παίκτη που κάνει την πρόκληση.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Challenger.jpg" alt="Tennis-Challenger" width="500"/>
</div>

Έπειτα τον παίκτη που δέχεται την πρόκληση για να γίνει έλεγχος αν η πρόκληση είναι σύμφων με τους κανόνες

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Challenged.jpg" alt="Tennis-Challenged" width="500"/>
</div>

Ενημερωνόμαστε με το ανάλογο μήνυμα για το αν είναι έγκυρη, και απαντάμε αν νίκησε ο παίκτης που έκανε την πρόκληση

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Challenge-Result-Querry.jpg" alt="Tennis-Challenge-Result-Querry" width="500"/>
</div>

Απαντώντας ενημερωνόμαστε αν το αποτέλεσμα προκάλεσε αλλαγή στην κατάταξη (περίπτωση νίκης παίκτη χαμηλότερης θέσης)

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Result-Registered.jpg" alt="Tennis-Result-Registered" width="500"/>
</div>

Εμφανίζοντας την κατάταξη μπορούμε να δούμε τις αλλαγές που προκαλούνται.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ranking-After-Match.jpg" alt="Tennis-Ranking-After-Match" width="500"/>
</div>

Ο έλεγχος για αδρανείς παίκτες ελέγχει αν κάποιος παίκτης έχει τελευταία ημερομηνία δραστηριότητας (εισαγωγή στο tennis club,
έπαιξε match ή έπεσε λόγω αδράνειας) μεγαλύτερη από 1 μήνα πριν και τους ρίχνει μία θέση. 

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-No-Decay.jpg" alt="Tennis-No-Decay" width="500"/>
</div>

Τώρα ας δούμε περίπτωση στην οποία οι παίκτες στις θέσεις 1, 4, 6, 8 είναι αδρανείς. Σημειώνεται πως ο τελευταίος παίκτης (8 στην προκειμένη) δεν
δέχεται ποινή σε περίπτωση αδράνειας και παίρνει ασυλία για 1 μήνα (ανανεώνεται η ημερομηνία δραστηριότητας) σύμφωνα
με τους κανόνες Τέννις του Brixworth Tennis Club που χρησιμοποιούνται παγκοσμίως.
Παρακάτω είναι η κατάταξη πριν τον έλεγχο αδράνειας.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ranking-Before-Decay.jpg" alt="Tennis-Ranking-Before-Decay" width="500"/>
</div>

Πρώτα μας ειδοποιεί πως ο τελευταίος παίκτης, παρότι αδρανής, δεν πέφτει θέση.   

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Last-Player-Decay.jpg" alt="Tennis-Last-Player-Decay" width="500"/>
</div>

Και έπειτα μας ενημερώνει για τους υπόλοιπους παίκτες.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Decay-YES.jpg" alt="Tennis-Decay-YES" width="500"/>
</div>

Βλέπουμε πως η κατάταξη ενημερώνεται κατάλληλα.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ranking-After-Decay.jpg" alt="Tennis-Ranking-After-Decay" width="500"/>
</div>

Υπάρχει αμυντικός προγραμματισμός σε όλες τις εισαγωγές δεδομένων (εισαγωγή παικτών, εισαγωγή
θέσεων παικτών, ακύρωση λειτουργιών χωρίς αλλαγές) και ο χρήστης ειδοποιείται με το κατάλληλο
μήνυμα και υπόδειξη για τη σωστή μορφή δεδομένων.

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Wrong-Name.jpg" alt="Tennis-Wrong-Name" width="500"/>
</div>

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Wrong-Rank.jpg" alt="Tennis-Wrong-Rank" width="500"/>
</div>

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Challenge-Canceled.jpg" alt="Tennis-Challenge-Canceled" width="500"/>
</div>

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Deletion-Cancelled.jpg" alt="Tennis-Deletion-Cancelled" width="500"/>
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>    

### Διαδικασία Σύνταξης

Αναπτύχθηκε και χρησιμοποιήθηκε Python Script για την αυτοματοποίηση παραγωγής των links των εικονών και του alt text του README, 
εξασφαλίζοντας συνέπεια με την αποφυγή λαθών και εξοικονόμηση χρόνου κατά την προσθήκη πολλών στιγμιότυπων οθόνης.

## Μελλοντικές Προσθήκες

- [ ] Προβολή δεδομένων τελευταίας δραστηριότητας παικτών
- [ ] Δυνατότητα εισαγωγής παικτών με αριθμό νικών, ηττών και ημερομηνία τελευταίας δραστηριότητας.
- [ ] Απευθείας τροποποίηση δεδομένων παικτών (νικών, ηττών) με νούμερα κι όχι με καταγραφή αγώνα.
- [ ] Εισαγωγή προγραμματισμένου αγώνα που δεν έχει ολοκληρωθεί.
- [ ] Έλεγχος και μείωση θέσης λόγω αναβολής αγώνα.
- [ ] Διατήρηση δεδομένων προκλήσεσων, αρνήσεων προγραμματισμού.
- [ ] Μείωση θέσης σε περίπτωση άρνησης προγραμματισμού αγώνα 3 φορές.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Επικοινωνία

Γιώργος Τσολακίδης - [Linked In: Giorgos Tsolakidis](https://www.linkedin.com/in/black-baron/) - black_baron94@hotmail.com 

Project Link: [Tennis Ladder](https://github.com/BlackBaron94/Tennis-Ladder-UI-Upgrade)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://python.org/
[tkinter.python]: https://img.shields.io/badge/Frontend-tkinter-blue
[tkinter-url]: https://docs.python.org/3/library/tkinter.html
[sqlite3.python]: https://img.shields.io/badge/SQLite-blue?logo=sqlite&logoColor=white
[sqlite3-url]: https://docs.python.org/3/library/sqlite3.html
[datetime.python]: https://img.shields.io/badge/datetime-5.3-66ccff?style=flat&labelColor=3670A0&logo=python&logoColor=ffdd54
[datetime-url]: https://docs.python.org/3/library/datetime.html

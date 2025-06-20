<a id="readme-top"></a>
<div align="center">
  <h1 align="center">Tennis Ladder Project</h1>

  <p align="center">
    Ένα project που επιτρέπει την εισαγωγή παικτών, διατήρηση δεδομένων αγώνων και αυτοματοποιεί την ενημέρωση των θέσεων βάσει δραστηριότητας!
    </p>
</div>

## Περιεχόμενα
- [Περιγραφή Project](#περιγραφή-project)
- [Οδηγίες Εγκατάστασης](#οδηγίες-εγκατάστασης)
- [Λειτουργίες](#λειτουργίες)
- [Κανόνες Προγράμματος](#κανόνες-προγράμματος)
- [Χρήση](#χρήση)
- [Μελλοντικές Προσθήκες](#μελλοντικές-προσθήκες)
- [Επικοινωνία](#επικοινωνία)
- [License](#license)

## Περιγραφή Project 

Η εφαρμογή δημιουργήθηκε με σκοπό να διατηρεί και να επεξεργάζεται δεδομένα μιας κατάταξης Τέννις. Οι δυνατότητες περιλαμβάνουν προσθήκη, 
διαγραφή παίκτη και επεξεργασία στοιχείων παίκτη (CRUD), τυχαιοποιημένη αρχική εισαγωγή παικτών, έλεγχο και καταγραφή πρόκλησης και 
αποτελεσμάτων αγώνων. Επιπλέον, υπάρχει η λειτουργία ελέγχου αδράνειας που ενημερώνει αυτοματοποιημένα τις θέσεις κατάταξης.

### Τεχνολογίες και βιβλιοθήκες που χρησιμοποιήθηκαν:

<a href="https://python.org/"> <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&style=plastic" alt="Python-logo" width=100px/></a>

<a href="https://docs.python.org/3/library/tkinter.html"> <img src="https://img.shields.io/badge/Frontend-tkinter-blue?style=plastic" alt="tkinter-logo" width=140px/></a>

<a href="https://docs.python.org/3/library/sqlite3.html"> <img src="https://img.shields.io/badge/SQLite3-003B57?logo=sqlite&logoColor=white&style=plastic" alt="SQLite-Logo" width=100px/></a>

<a href="https://docs.python.org/3/library/datetime.html"> <img src="https://img.shields.io/badge/DateTime-5.3-66ccff?style=flat&labelColor=3670A0&logo=python&logoColor=ffdd54" alt="DateTime-Logo" width=140px height=28px/></a>
  
<a href="https://pyinstaller.org/"><img src="https://raw.githubusercontent.com/BlackBaron94/images/main/PyInstaller-Logo.png" alt="PyInstaller-Logo" width=37px/><img src="https://img.shields.io/badge/PyInstaller-23364D" alt="PyInstaller-Logo-Text" width=100px/></a>


### Αρχεία του Project

- main.py: Εκτελεί τη συνάρτηση start_app() που ξεκινάει το Application και εμφανίζει το παράθυρο
- gui.py: Το αρχείο αυτό περιέχει τον κώδικα για το GUI. Εδώ υλοποιούνται τα παράθυρα, τα κουμπιά και οι λοιπές
διεπαφές με τον χρήστη, ώστε να μπορεί να αλληλεπιδρά με την εφαρμογή, καθώς και βασικό input validation.
- logic.py: Στον κώδικα του αρχείου αυτού περιλαμβάνονται όλες οι επιχειρησιακές λειτουργίες, η επεξεργασία
των δεδομένων και οι εγγραφές με τη Βάση Δεδομένων.


### Διαδικασία Σύνταξης

Αναπτύχθηκε και χρησιμοποιήθηκε ένα σύντομο Python Script για την αυτοματοποίηση παραγωγής των links των εικονών και του alt text του README 
κατά τη σύνταξή του, εξασφαλίζοντας συνέπεια με την αποφυγή λαθών και εξοικονόμηση χρόνου κατά την προσθήκη πολλών στιγμιότυπων οθόνης.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Οδηγίες Εγκατάστασης


- Executable

Το onefile .exe είναι fully portable και δεν υπάρχουν προαπαιτούμενα. Κάνοντας clone το repo είστε έτοιμοι!

1. Clone του repo
   ```sh
   git clone https://github.com/BlackBaron94/Tennis-Ladder.git
   ```

- Κώδικας

Για να τρέξει το αρχείο .py χρειάζεται εγκατεστημένη έκδοση 3. Python καθώς και το πακέτο βιβλιοθήκης tkinter

2. Έλεγχος εγκατεστημένης έκδοσης Python
   ```sh
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

## Λειτουργίες

1. **Αρχικοποίηση κατάταξης**

(Διαθέσιμη μόνο με άδεια κατάταξη) Εισαγωγή πολλών παικτών ταυτόχρονα σε τυχαιοποιημένες θέσεις. 

---

2. **Προσθήκη παίκτη**

Εισαγωγή παίκτη είτε σε συγκεκριμένη θέση εντός των ορίων της κατάταξης, είτε στο τέλος της. 

---

3. **Διαγραφή παίκτη**

Διαγραφή βάσει θέσης κατάταξης.

---

4. **Έλεγχος και καταγραφή αποτελέσματος πρόκλησης**

Εισάγονται ο παίκτης που προκαλεί και ο παίκτης που δέχεται την πρόκληση. Ελέγχεται αν η πρόκληση είναι
έγκυρη βάσει κανονισμών. Εισάγεται νικητής και τροποποιείται η κατάταξη καταλλήλως.

---

5. **Έλεγχος κατάταξης για αδρανείς παίκτες**

Ελέγχεται η κατάταξη για αδρανείς παίκτες, εφαρμόζεται ποινή και ανανεώνεται η κατάταξη.

---

6. **Εμφάνιση κατάταξης**

Εμφανίζει πίνακα με τα στοιχεία των παικτών. Παρουσιάζονται θέσεις κατάταξης, ονοματεπώνυμα, νίκες, ήττες  και
ημερομηνία τελευταίας δραστηριότητας σε πίνακα. Ο χρήστης μπορεί να επεξεργαστεί τα δεδομένα των χρηστών εδώ.

---

7. **Έξοδος**

Τερματισμός του προγράμματος.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Κανόνες Προγράμματος

Παρακάτω, ακολουθούν οι κανόνες κατάταξης Tennis του Brixworth Tennis Club που χρησιμοποιούνται παγκοσμίως και σύμφωνα
με τους οποίους δημιουργήθηκε το πρόγραμμα.
Σε γενικές γραμμές τονίζεται πως οι παίκτες δεν ταξινομούνται ανάλογα με τον αριθμό των νικών/ηττών τους ή πόντων, αλλά
αναλόγως με την θέση που κατείχε ο παίκτης που νίκησαν.


1. Εισαγωγή παίκτη:

Η εισαγωγή παίκτη προκαλεί μετακίνηση του παίκτη που καταλάμβανε τη θέση και των υπολοίπων κατά μία θέση κάτω.
Εναλλακτικά, γίνεται στο τέλος της κατάταξης.

2. Διαγραφή παίκτη:

Η διαγραφή παίκτη μετακινεί όλους τους επόμενους παίκτες μία θέση πάνω, καλύπτοντας το κενό που δημιουργείται.

3. Πρόκληση σε αγώνα

Η πρόκληση γίνεται αποδεκτή όταν ο παίκτης που προκαλεί είναι χαμηλότερη θέση από τον παίκτη που θέλει να προκαλέσει.
Η μέγιστη διαφορά θέσης είναι 3 θέσεις για παίκτες που είναι από τις θέσεις 1 έως 9. Για παίκτες που είναι μεγαλύτερη
θέση της 9ης, η διαφορά θέσης μπορεί να είναι έως και 4 θέσεις. 

4. Αποτέλεσμα αγώνα

Σε περίπτωση νίκης του παίκτη στη μεγαλύτερη θέση κατάταξης, καταγράφονται η νίκη και η ήττα και δεν προκαλείται αλλαγή
κατάταξης. 
Σε περίπτωση νίκης του παίκτη στη μικρότερη θέση κατάταξης, αυτός παίρνει τη θέση του ηττημένου. Ο ηττημένος και όλοι
ανάμεσα στον νικητή και τον ηττημένο μετακινούνται μία θέση κάτω.

5. Αδράνεια παικτών

Διατηρούνται ημερομηνίες δραστηριότητας των παικτών. Δραστηριότητα θεωρείται η προσθήκη του παίκτη στην κατάταξη, η
συμμετοχή του σε αγώνα και η εφαρμογή ποινής. Αν η ημερομηνία δραστηριότητας είναι μεγαλύτερη του 1 μήνα πριν, ο παίκτης
δέχεται την ποινή και ανανεώνεται η ημερομηνία δραστηριότητας. Η ποινή είναι η πτώση κατά μία θέση. 
Λόγω της ανανέωσης της ημερομηνίας δραστηριότητας, ο ίδιος παίκτης δεν μπορεί να ξαναδεχθεί ποινή σε διάστημα μικρότερο 
του 1 μήνα από την τελευταία ποινή.
Ο τελευταίος παίκτης έχει ασυλία σε ποινή αδράνειας καθώς δεν μπορεί να πέσει περαιτέρω. Η ημερομηνία δραστηριότητάς του
ανανεώνεται κανονικά.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Χρήση

Υπάρχει διαθέσιμο video demo [εδώ](https://drive.google.com/file/d/1MkW2A-iyxVoFGQkGixezvF2cfNggmixp/view?usp=drive_link).

Εναλλακτικά, παρακάτω φαίνονται παραδείγματα χρήσης με εικόνες.

---

> **Αυτό είναι το κύριο μενού της εφαρμογής.**

---

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Main-Menu.jpg" alt="Tennis-Main-Menu" width="500"/>
</div>

<p align="center"><b>Το κύριο μενού της εφαρμογής.</b></p>

---

> **Παρακάτω φαίνεται το παράθυρο διαλόγου αρχικοποίησης κατάταξης και η εμφάνιση του πίνακα κατάταξης. Η τυχαιποιημένη αρχικοποίηση είναι διαθέσιμη μόνο όταν η κατάταξη είναι άδεια. Αυτή η λειτουργία
επιτρέπει την προσθήκη πολλών παικτών ταυτόχρονα. Κατά την εισαγωγή παικτών, η λίστα αρχικοποίησης ενημερώνεται με τα εισαχθέντα ονόματα, όπως φαίνεται στις εικόνες.**

---

<div align="center">
  <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Initialization-Empty-List.jpg" alt="Tennis-Initialization-Empty-List" width="500" style="display: inline-block;"/>
  <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Initialilzation-List.jpg" alt="Tennis-Initialilzation-List" width="500" style="display: inline-block;"/>
</div>

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Randomized-Ranking.jpg" alt="Tennis-Randomized-Ranking" width="850"/>
</div>

<p align="center"><b>Παράθυρο διαλόγου αρχικοποίησης και πίνακας κατάταξης.</b></p>

---

> **Η λειτουργία προσθήκης παίκτη είναι διαθέσιμη με εισαγωγή είτε σε συγκεκριμένη θέση είτε στο τέλος της κατάταξης. Η λειτουργία διαγραφής παίκτη γίνεται βάσει θέσης και υπάρχει επιβεβαίωση διαγραφής. Σε αυτό το παράθυρο διαλόγου παρουσιάζεται το όνομα του εν λόγω παίκτη για αποφυγή λαθών.**

---

<div align="center">
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Added-Player.jpg" alt="Tennis-Added-Player" width="500" style="display: inline-block;"/>
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Delete-Player-Question.jpg" alt="Tennis-Delete-Player-Question" width="500" style="display: inline-block;"/>
</div>

<p align="center"><b>Παράθυρο διαλόγου προσθήκης παίκτη και διαγραφής παίκτη.</b></p>

---

> **Για έλεγχο και καταγραφή αποτελέσματος πρόκλησης, χρησιμοποιείται η θέση του παίκτη που κάνει την πρόκληση και του παίκτη που δέχεται την πρόκληση. Στη συνέχεια ελέγχεται η εγκυρότητα της πρόκλησης και καταχωρείται το αποτέλεσμα, προκαλώντας αλλαγή στα δεδομένα της κατάταξης.**

---

<div align="center">
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Challenger.jpg" alt="Tennis-Challenger" width="500" style="display: inline-block;"/>
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Challenged.jpg" alt="Tennis-Challenged" width="500" style="display: inline-block;"/>
</div>

<div align="center">
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Challenge-Result-Querry.jpg" alt="Tennis-Challenge-Result-Querry" width="500" style="display: inline-block;"/>
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Result-Registered.jpg" alt="Tennis-Result-Registered" width="500" style="display: inline-block;"/>
</div>

<p align="center"><b>Παράθυρο διαλόγου ελέγχου και καταγραφής αγώνα.</b></p>

---

> **Ο έλεγχος για αδρανείς παίκτες αφορά το αν κάποιος παίκτης είναι αδρανής για ένα μήνα. Η ποινή για αδράνεια συνεπάγεται πτώση μιας θέσης στην κατάταξη. Στην παρακάτω περίπτωση οι παίκτες 1, 4, 6, 8 είναι αδρανείς, αλλά ο παίκτης 8 είναι τελευταίος και δεν εφαρμόζεται ποινή.**

---

<div align="center">
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Last-Player-Decay.jpg" alt="Tennis-Last-Player-Decay" width="500" style="display: inline-block;"/>
   <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Decay-YES.jpg" alt="Tennis-Decay-YES" width="500" style="display: inline-block;"/>
</div>

<p align="center"><b>Έλεγχος κατάταξης για αδρανείς παίκτες.</b></p>

---

>**Πατώντας εμφάνιση κατάταξης, ο χρήστης μπορεί να δει την κατάταξη και πατώντας στο μολυβάκι της στήλης "Επεξεργασία", μπορεί να αλλάξει όλα τα δεδομένα που διατηρούνται για τον συγκεκριμένο παίκτη. Υπάρχει έλεγχος για την σωστή εισαγωγή δεδομένων και σύσταση για διόρθωση, παραδείγματος χάριν αν ο χρήστης βάλει παραπάνω από μία λέξη στο όνομα ή το επώνυμο, τα κενά αντικαθίστανται με παύλες (για να δώσουν λύση στην περίπτωση διπλού ονόματος).**

---

<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Show-Ranking-Editing-Values.jpg" alt="Tennis-Show-Ranking-Editing-Values.jpg" width="850"/>
</div>
<div align="center">
    <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Show-Ranking-Changed-Values.jpg" alt="Tennis-Show-Ranking-Changed-Values.jpg" width="850"/>
</div>

<p align="center"><b>Τροποποίηση δεδομένων στην εμφάνιση κατάταξης.</b>

---

> **Υπάρχει αμυντικός προγραμματισμός σε όλες τις εισαγωγές δεδομένων (εισαγωγή παικτών, εισαγωγή θέσεων παικτών, ακύρωση λειτουργιών χωρίς αλλαγές). Ο χρήστης ειδοποιείται με το κατάλληλο μήνυμα και οδηγίες για τη σωστή μορφή δεδομένων. Παρακάτω φαίνονται μερικές από αυτές τις περιπτώσεις.**

---

<div align="center">
  <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Wrong-Name.jpg" alt="Tennis-Wrong-Name" width="500" style="display: inline-block;"/>
  <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Wrong-Rank.jpg" alt="Tennis-Wrong-Rank" width="500" style="display: inline-block;"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Challenge-Canceled.jpg" alt="Tennis-Challenge-Canceled" width="500" style="display: inline-block;"/>
  <img src="https://raw.githubusercontent.com/BlackBaron94/images/main/Tennis-Ladder/Tennis-Deletion-Cancelled.jpg" alt="Tennis-Deletion-Cancelled" width="500" style="display: inline-block;"/>
</div>

<p align="center"><b>Παραδείγματα αμυντικού προγραμματισμού.</b></p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Μελλοντικές Προσθήκες

- [X] Έλεγχος και εφαρμογή ποινής αδρανών παικτών.
- [X] Προβολή δεδομένων τελευταίας δραστηριότητας παικτών.
- [X] Απευθείας τροποποίηση όλων των δεδομένων παικτών.
- [ ] Εισαγωγή προγραμματισμένου αγώνα που δεν έχει ολοκληρωθεί.
- [ ] Έλεγχος και μείωση θέσης λόγω αναβολής αγώνα.
- [ ] Ανάπτυξη λειτουργίας για αποθήκευση ιστορικών προκλήσεων με timestamp και αρνήσεων προγραμματισμού αγώνα.
- [ ] Μείωση θέσης σε περίπτωση άρνησης προγραμματισμού αγώνα 3 φορές.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Επικοινωνία

Γιώργος Τσολακίδης - [Linked In: Giorgos Tsolakidis](https://www.linkedin.com/in/black-baron/) - black_baron94@hotmail.com 

Project Link: [Tennis Ladder](https://github.com/BlackBaron94/Tennis-Ladder)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License


This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


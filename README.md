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

<p align="right">(<a href="#readme-top">back to top</a>)</p>    

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

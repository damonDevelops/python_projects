import csv
import os
import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl


# import uses Twilio REST client

from twilio.rest import Client
import random


# Couple class for holding the couples with their first name and phone number


class Person:

    def __init__(
        self,
        first_name,
        first_number,
        ):
        self.first_name = first_name
        self.first_number = first_number
        self.person_pool = []

    def set_secretSanta(self, x):
        self.secretSanta = x

    def addToPersonPool(self, person):
        self.person_pool.append(person)

    def send_message(self, client, messaging_sid, organiser):
        print("Got to send message function")

        # the twilio client sends two messages, one to each couple member
        message = client.messages.create(  
          messaging_service_sid=messaging_sid, 
          body= 'Merry Christmas ' + self.first_name + 
            ", your secret santa is: " + self.secretSanta.first_name + ', '
            "Programmed by yours truly, " + organiser,   
          to= self.first_number 
        )

        

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.person_list = []

        QFontDatabase.addApplicationFont('Christmas Bell - Personal Use.otf'
                )
        heading_font = QFont('Christmas Bell - Personal Use')
        heading_font.setPointSize(35)

        h2Font = QFont()
        h2Font.setPointSize(18)

        textFont = QFont()
        textFont.setPointSize(12)

        self.headingLabel = QLabel('Individual Secret Santa Python Program!')
        self.headingLabel.setFont(heading_font)

        self.headingLabel.setStyleSheet('color: #0BD6A8; background-color: #D6001C;'
                )
          
        self.headingLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.radioButtonTesting = QtWidgets.QRadioButton("Testing Mode")
        self.radioButtonTesting.setChecked(True)
        self.radioButtonTesting.toggled.connect(self.testingSelected)
        self.testingBool = True

        self.workingMode = QtWidgets.QRadioButton("Working Mode")
        self.workingMode.toggled.connect(self.workingSelected)
        self.workingBool = False

        self.openFileButton = QPushButton()
        self.openFileButton.setObjectName('openFile')
        self.openFileButton.setText('Import People from CSV')
        self.openFileButton.clicked.connect(self.openFile)

        self.twilioLabel = QLabel('Twilio Information')
        self.twilioLabel.setContentsMargins(0, 20, 0, 5)
        self.twilioLabel.setFont(h2Font)

        self.account_sid = QLineEdit()
        self.account_sid.setObjectName('sid')
        self.account_sid.setPlaceholderText('Enter your twilio account SID')
        self.setFont(textFont)
        self.account_sid.setEchoMode(QtWidgets.QLineEdit.Password)

        self.account_auth = QLineEdit()
        self.account_auth.setObjectName('auth')
        self.account_auth.setPlaceholderText('Enter your twilio account Authentication Token')
        self.account_auth.setEchoMode(QtWidgets.QLineEdit.Password)

        self.messaging_sid = QLineEdit()
        self.messaging_sid.setObjectName('msgSid')
        self.messaging_sid.setPlaceholderText('Enter your twilio messaging service SID')
        self.messaging_sid.setEchoMode(QtWidgets.QLineEdit.Password)

        self.organiserLabel = QLabel('Organiser Information')
        self.organiserLabel.setContentsMargins(0, 20, 0, 5)
        self.organiserLabel.setFont(h2Font)

        self.organiser = QLineEdit()
        self.organiser.setObjectName('organiser')
        self.organiser.setPlaceholderText('Organiser Name')

        self.personLabel = QLabel('Person Information')
        self.personLabel.setContentsMargins(0, 20, 0, 5)
        self.personLabel.setFont(h2Font)

        self.person_name = QLineEdit()
        self.person_name.setObjectName('fName')
        self.person_name.setPlaceholderText('Name')

        self.person_phone = QLineEdit()
        self.person_phone.setObjectName('fPhone')
        self.person_phone.setPlaceholderText('Phone Number (include area code ie +61)')

        self.list = QListWidget()

        self.addPersonButton = QPushButton()
        self.addPersonButton.setObjectName('addPerson')
        self.addPersonButton.setText('Add Person')
        self.addPersonButton.clicked.connect(self.addPerson)

        self.sendMessageButton = QPushButton()
        self.sendMessageButton.setObjectName('sendMessage')
        self.sendMessageButton.setText('Send Secret Santa Messages!')
        self.sendMessageButton.clicked.connect(self.sendMessage)

        self.resetButton = QPushButton()
        self.resetButton.setObjectName('reset')
        self.resetButton.setText('Reset Secret Santa Service!')
        self.resetButton.clicked.connect(self.resetSS)

        layout = QFormLayout()

        layout.addWidget(self.headingLabel)
        layout.addWidget(self.openFileButton)
        layout.addWidget(self.radioButtonTesting)
        layout.addWidget(self.workingMode)

        layout.addWidget(self.organiserLabel)
        layout.addWidget(self.organiser)

      
        layout.addWidget(self.twilioLabel)

        layout.addWidget(self.account_sid)
        layout.addWidget(self.account_auth)
        layout.addWidget(self.messaging_sid)

        
        layout.addWidget(self.personLabel)

        layout.addWidget(self.person_name)
        layout.addWidget(self.person_phone)

        layout.addWidget(self.addPersonButton)

        layout.addWidget(self.list)

        layout.addWidget(self.sendMessageButton)
        layout.addWidget(self.resetButton)

        self.setLayout(layout)

        self.setWindowTitle('Secret Santa Twilio Application')
        self.setFixedSize(900, 900)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint,False)

    def openFile(self):
      path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')

      try:
        with open(path[0], 'r', encoding='utf-8-sig') as csvfile:
          datareader = csv.reader(csvfile)
          for row in datareader:
            first_name = row[0]
            first_number = '+' + row[1]

            person = Person(first_name, first_number)
            self.person_list.append(person)

            person_string = 'Name: ' + first_name + ', Phone: ' + first_number

            self.list.addItem(person_string)
      except Exception as e:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error!")
        dlg.setText("An error occured: " + str(e))
        button = dlg.exec()
        if button == QMessageBox.Ok:
          print("OK!")
          return


    def addPerson(self):

        # checks that all fields are there otherwise doesn't add person
        if not self.person_name.text() \
            or not self.person_phone.text():
              dlg = QMessageBox(self)
              dlg.setWindowTitle("Error!")
              dlg.setText("You've missed a field, make sure all details are there and try again :)")
              button = dlg.exec()
              if button == QMessageBox.Ok:
                print("OK!")
                return

        # shost is a QString object

        fName = self.person_name.text()
        fphone = self.person_phone.text()


        person_string = 'Name: ' + fName + ', Phone: ' + fphone

        new_person = Person(fName, fphone)
        self.person_list.append(new_person)


        self.list.addItem(person_string)

        self.person_name.setText('')
        self.person_phone.setText('')

    def testingSelected(self, selected):
      if selected:
        self.testingBool = True
        self.workingBool = False
    
    def workingSelected(self, selected):
      if selected:
        self.testingBool = False
        self.workingBool = True

    def sendMessage(self):
      if(self.testingBool == True):
        print("Testing mode")

        if not self.organiser.text():
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("No organiser field! Make sure you add that bad boy for all the credit! :)")
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        # Check that couplex exist
        if self.list.count() <= 1 :
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("You entered less than two couples... How you gonna do secret santa all by yourself?")
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        print("No worries with fields")

        try:
          for person in self.person_list:
              for p in self.person_list:
                  if p.first_name != person.first_name:
                      if p not in person.person_pool:
                          person.addToPersonPool(p)
        except Exception as e:
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("An error occured while making person pools: \n",str(e))
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        print("Made person pools")

        try:
          for person in self.person_list:
              random_person = random.choice(person.person_pool)
              person.set_secretSanta(random_person)

              if person in random_person.person_pool:
                  random_person.person_pool.remove(person)

              for x in self.person_list:
                if random_person in x.person_pool:
                  x.person_pool.remove(random_person)
        except Exception as e:
          dlg = QMessageBox(self)

          dlg.setWindowTitle("Error!")
          dlg.setText("An error occured while assigning secret santas to people: \n",str(e))
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        print("Assigned secret santas")

        secret_santas_message = ""
        for person in self.person_list:   
          secret_santas_message += ("Pretend message sent to (" + person.first_number + "): " + "Merry Christmas " + person.first_name  +
            ", your secret santa person is: " + person.secretSanta.first_name +  ", sent by yours truly, " + self.organiser.text() + "\n")

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Merry Christmas!")
        dlg.setText(secret_santas_message)
        dlg.resize(400,400)
        button = dlg.exec()
        if button == QMessageBox.Ok:
          print("OK!")
          return
        
      if(self.workingBool):
        print("Working mode")
        print("Got to the start of Send Message")

        if not self.account_sid.text() or not self.account_auth.text():
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("You've missed a field, make sure all details are there and try again :)")
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        print("No worries with fields")

        self.client = Client(self.account_sid.text(),
                              self.account_auth.text())

        print("Client made")

        msid = self.messaging_sid.text()

        print("Msid made")

        if self.list.count() <= 1 :
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("You entered less than two people... How you gonna do secret santa all by yourself?")
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        try:
          for people in self.person_list:
              for p in self.person_list:
                  if p.first_name != people.first_name:
                      if p not in people.person_pool:
                          people.addToPersonPool(p)
        except Exception as e:
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("An error occured while making people pools: \n",str(e))
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        print("Made people pools")

        try:
          for person in self.person_list:
              random_person = random.choice(person.person_pool)
              person.set_secretSanta(random_person)

              if person in random_person.person_pool:
                  random_person.person_pool.remove(person)

              for x in self.person_list:
                if random_person in x.person_pool:
                  x.person_pool.remove(random_person)
        except Exception as e:
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText(str(e))
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        print("Assigned secret santas")
        
        try:
          for person in self.person_list:
            print("Currently sending message for: ", person.first_name)
            person.send_message(self.client, msid, self.organiser.text())
        except Exception as e:
          print_string = escape_ansi(str(e))
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("An error occured while sending the messages\n It's likely a phone number was wrong or the Twilio details were incorrect: \n" + print_string)
          print(print_string)
          button = dlg.exec()
          if button == QMessageBox.Ok:
            return

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Success!")
        dlg.setText("The messages were sent successfully! Happy Secret Santa! Merry Christmas!")
        button = dlg.exec()
        if button == QMessageBox.Ok:
          print("OK!")
          return

    def resetSS(self):
      print("Clicked")
      self.person_name.setText('')
      self.person_phone.setText('')
      self.account_sid.setText('')
      self.account_auth.setText('')
      self.messaging_sid.setText('')
      self.person_list.clear()
      self.list.clear()
      


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets
from PyQt5 import Qt

# import uses Twilio REST client

from twilio.rest import Client
import random


# Couple class for holding the couples with their first name and phone number

class Couple:

    def __init__(
        self,
        first_name,
        first_number,
        second_name,
        second_number,
        ):
        self.first_name = first_name
        self.first_number = first_number
        self.second_name = second_name
        self.second_number = second_number
        self.couple_pool = []

    def set_secretSanta(self, x):
        self.secretSanta = x

    def addToCouplePool(self, couple):
        self.couple_pool.append(couple)

    def send_message(self, client, messaging_sid):
        print("Got to send message function")

        try:
          # the twilio client sends two messages, one to each couple member
          message = client.messages.create(  
            messaging_service_sid=messaging_sid, 
            body= 'Merry Christmas ' + self.first_name + 
              ", your secret santa couple is: " + self.secretSanta.first_name + ' & ' + self.secretSanta.second_name + ', '
              "Programmed by yours truly, Damon",   
            to= self.first_number 
          )

          message2 = client.messages.create(  
            messaging_service_sid=messaging_sid, 
            body= 'Merry Christmas ' + self.second_name + 
              ", your secret santa couple is: " + self.secretSanta.first_name + ' & ' + self.secretSanta.second_name + ', '
              "Programmed by yours truly, Damon", 
            to= self.second_number 
          )
        except Exception as e:
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Error!")
          dlg.setText("An error occured while sending the messages\n It's likely a phone number was wrong or the Twilio details were incorrect: \n",str(e))
          button = dlg.exec()
          if button == QMessageBox.Ok:
            print("OK!")
            return

        print("Got past all the exceptions... message should be sending")

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.couple_list = []

        QFontDatabase.addApplicationFont('Christmas Bell - Personal Use.otf'
                )
        heading_font = QFont('Christmas Bell - Personal Use')
        heading_font.setPointSize(42)

        h2Font = QFont()
        h2Font.setPointSize(18)

        textFont = QFont()
        textFont.setPointSize(12)

        self.headingLabel = QLabel('Secret Santa Python Program!')
        self.headingLabel.setFont(heading_font)

        self.headingLabel.setStyleSheet('color: #0BD6A8; background-color: #D6001C;'
                )
          
        self.headingLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.twilioLabel = QLabel('Twilio Information')
        self.twilioLabel.setContentsMargins(0, 20, 0, 5)
        self.twilioLabel.setFont(h2Font)

        self.account_sid = QLineEdit()
        self.account_sid.setObjectName('sid')
        self.account_sid.setPlaceholderText('Enter your twilio account SID'
                )
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

        self.coupleLabel = QLabel('Couple Information')
        self.coupleLabel.setContentsMargins(0, 20, 0, 5)
        self.coupleLabel.setFont(h2Font)

        self.couple_f_name = QLineEdit()
        self.couple_f_name.setObjectName('fName')
        self.couple_f_name.setPlaceholderText('First Couple Name')

        self.couple_f_phone = QLineEdit()
        self.couple_f_phone.setObjectName('fPhone')
        self.couple_f_phone.setPlaceholderText('First Couple Phone Number (include area code ie +61)'
                )

        self.couple_s_name = QLineEdit()
        self.couple_s_name.setObjectName('sName')
        self.couple_s_name.setPlaceholderText('Second Couple Name')

        self.couple_s_phone = QLineEdit()
        self.couple_s_phone.setObjectName('sPhone')
        self.couple_s_phone.setPlaceholderText('Second Couple Phone Number (include area code ie +61)'
                )

        self.list = QListWidget()

        self.addCoupleButton = QPushButton()
        self.addCoupleButton.setObjectName('addCouple')
        self.addCoupleButton.setText('Add Couple')
        self.addCoupleButton.clicked.connect(self.addCouple)

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
        layout.addWidget(self.twilioLabel)

        layout.addWidget(self.account_sid)
        layout.addWidget(self.account_auth)
        layout.addWidget(self.messaging_sid)

        layout.addWidget(self.coupleLabel)

        layout.addWidget(self.couple_f_name)
        layout.addWidget(self.couple_f_phone)

        layout.addWidget(self.couple_s_name)
        layout.addWidget(self.couple_s_phone)
        layout.addWidget(self.addCoupleButton)

        layout.addWidget(self.list)

        layout.addWidget(self.sendMessageButton)
        layout.addWidget(self.resetButton)

        self.setLayout(layout)

        self.setWindowTitle('Secret Santa Twilio Application')
        self.resize(800, 7000)
        self.setFixedSize(800,700)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint,False)

    # button click event

    def addCouple(self):

        # checks that all fields are there otherwise doesn't add person
        if not self.couple_f_name.text() \
            or not self.couple_s_name.text() \
            or not self.couple_f_phone.text() \
            or not self.couple_s_name.text() \
            or not self.couple_s_phone.text():

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error!")
            dlg.setText("You've missed a field, make sure all details are there and try again :)")
            button = dlg.exec()
            if button == QMessageBox.Ok:
              print("OK!")
              return

        # shost is a QString object

        fName = self.couple_f_name.text()
        fphone = self.couple_f_phone.text()

        sName = self.couple_s_name.text()
        sphone = self.couple_s_phone.text()

        couple_string = 'Name: ' + fName + ', Phone: ' + fphone \
            + ', Name: ' + sName + ', Phone: ' + sphone

        new_couple = Couple(fName, fphone, sName, sphone)
        self.couple_list.append(new_couple)


        self.list.addItem(couple_string)

        self.couple_f_name.setText('')
        self.couple_s_name.setText('')
        self.couple_f_phone.setText('')
        self.couple_s_phone.setText('')

    def sendMessage(self):
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
        dlg.setText("You entered less than two couples... How you gonna do secret santa all by yourself?")
        button = dlg.exec()
        if button == QMessageBox.Ok:
          print("OK!")
          return

      try:
        for couple in self.couple_list:
            for p in self.couple_list:
                if p.first_name != couple.first_name:
                    if p not in couple.couple_pool:
                        couple.addToCouplePool(p)
      except Exception as e:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error!")
        dlg.setText("An error occured while making couple pools: \n",str(e))
        button = dlg.exec()
        if button == QMessageBox.Ok:
          print("OK!")
          return

      print("Made couple pools")

      try:
        for couple in self.couple_list:
            random_couple = random.choice(couple.couple_pool)
            couple.set_secretSanta(random_couple)

            if couple in random_couple.couple_pool:
                random_couple.couple_pool.remove(couple)

            for x in self.couple_list:
              if random_couple in x.couple_pool:
                x.couple_pool.remove(random_couple)
      except Exception as e:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error!")
        dlg.setText("An error occured while assigning secret santas to couples: \n",str(e))
        button = dlg.exec()
        if button == QMessageBox.Ok:
          print("OK!")
          return

      print("Assigned secret santas")
      
      for couple in self.couple_list:
        print("Currently sending message for: ", couple.first_name)
        couple.send_message(self.client, msid)

    def resetSS(self):
      print("Clicked")
      self.couple_f_name.setText('')
      self.couple_s_name.setText('')
      self.couple_f_phone.setText('')
      self.couple_s_phone.setText('')
      self.account_sid.setText('')
      self.account_auth.setText('')
      self.couple_list.clear()
      self.list.clear()
      


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

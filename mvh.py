import clr
import re
from time import sleep

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Windows.Forms as Winforms
import System.Drawing as draw
from System.IO import File
from System.Text import Encoding
import System
from System.Threading import ApartmentState, Thread, ThreadStart

clr.AddReference("System.Windows.Forms")

clr.AddReference("System.Drawing")



# --Globals


class PacketAnalyser(Winforms.Form):
    """
    
    """
    def __init__(self):

        #setting Caption to GUI
        self.Text = "Packet Analyzer"
        #setting GUI color
        self.BackColor = draw.Color.FromArgb(250, 250, 250)
        #setting GUI size
        self.FormSize = draw.Size(700, 700)

        # create buttons and labels font and colors variables
        self.buttonsFont = draw.Font("Lato", System.Single(12))
        self.buttonsForeColor = draw.Color.FromName("White")
        self.buttonsBackColor = draw.Color.FromArgb(255, 68, 90, 100)
        self.labelsFont = draw.Font("Lato", System.Single(9))

        # self.components = System.ComponentModel.Container()

        #setting the minimum and the maximum size of the GUI
        self.MinimumSize = draw.Size(700, 700)
        self.MaximumSize = draw.Size(700, 700)

        #calling functions in this class to create the controls and add them to the GUI
        self.createSendButton()
        self.createReceiveButton()
        self.createSaveButton()
        self.createSelectFrameTypeBox()
        self.createDestinationMacIpTextbox()
        self.createSourceLabel()
        self.createDestinationLabel()
        self.createPayloadLabel()
        self.createPacketsTextBox()
        self.createOnePacketRadioButton()
        self.createMultiplePacketsRadioButton()
        self.createPayloadDataTextBox()
        self.createPayloadDataLabel()
        self.createMacIpLabel()
        self.createClearButton()
        self.createTypeLabel()

        
        self.saveFileDialog = Winforms.SaveFileDialog()
        self.saveFileDialog.Title = "Save document"
        self.saveFileDialog.FileName = "Untitled"

        #adding a help button next to close button and disabling the minimize and maximize functionalities
        self.HelpButton = True
        self.MaximizeBox = False
        self.MinimizeBox = False

        #binding event when help button is clicked 
        self.HelpButtonClicked += self.formHelpButtonClicked
        #binding event when exit button is clicked
        self.FormClosing += self.SaveChangesDialog
        
        #getting the ip and the mac address of the machine
        #myIp, myMac : used to be displayed in the message box after help button is clicked
        self.myIp = Logging.get_ip()
        self.myMac = Logging.get_mac()

        #string variable to store the ip address or the mac address of the source machine,depends on what the user selects the frame type
        self.myIpOrMac = ""
        #string variable to store the ip address or the mac address of the target machine,depends on what the user selects the frame type
        self.destIpOrMac = ""
        #flag used to kill the thread when it's True
        self.exiting = False

        #two flags for send and receive buttons. used to determine the condition of the buttons (ON or OFF)
        self.receiveButtonFlag = 0
        self.sendButtonFlag = 0
        
    def createSourceLabel(self):
        """Function to create Source Label"""
        
        #creating label object
        self.sourceLabel = Winforms.Label()
        #setting label position
        self.sourceLabel.Location = draw.Point(30, 130)
        #setting label size
        self.sourceLabel.Size = draw.Size(70, 20)
        #setting label text
        self.sourceLabel.Text = "Source"
        #setting label font
        self.sourceLabel.Font = self.labelsFont
        #adding label to controls
        self.Controls.Add(self.sourceLabel)

    def createDestinationLabel(self):
        """Function to create Destination Label"""

        #creating label object
        self.DestinationLabel = Winforms.Label()
        #setting label position
        self.DestinationLabel.Location = draw.Point(300, 130)
        #setting label size
        self.DestinationLabel.Size = draw.Size(70, 20)
        #setting label text
        self.DestinationLabel.Text = "Destination"
        #setting label font
        self.DestinationLabel.Font = self.labelsFont
        #adding label to controls
        self.Controls.Add(self.DestinationLabel)

    def createPayloadLabel(self):
        """Function to create Data-Hex Label"""

        #creating label object
        self.hexDataLabel = Winforms.Label()
        #setting label position
        self.hexDataLabel.Location = draw.Point(550, 130)
        #setting label size
        self.hexDataLabel.Size = draw.Size(70, 20)
        #setting label text
        self.hexDataLabel.Text = "Data-hex"
        #setting label font
        self.hexDataLabel.Font = self.labelsFont
        #adding label to controls
        self.Controls.Add(self.hexDataLabel)

    def createMacIpLabel(self):
        """Function to create macIp Label"""

        #creating label object
        self.macIpLabel = Winforms.Label()
        #setting label position
        self.macIpLabel.Location = draw.Point(480, 52)
        #setting label size
        self.macIpLabel.Size = draw.Size(55, 20)
        #setting label text
        self.macIpLabel.Text = "Dest."
        #setting label font
        self.macIpLabel.Font = self.labelsFont
        #adding label to controls
        self.Controls.Add(self.macIpLabel)

    def createPayloadDataLabel(self):
        """Function to create payload Data Label"""

        #creating label object
        self.payloadDataLabel = Winforms.Label()
        #setting label position
        self.payloadDataLabel.Location = draw.Point(480, 82)
        #setting label size
        self.payloadDataLabel.Size = draw.Size(52, 20)
        #setting label text
        self.payloadDataLabel.Text = "Data"
        #setting label font
        self.payloadDataLabel.Font = self.labelsFont
        #adding label to controls
        self.Controls.Add(self.payloadDataLabel)
    
    def createTypeLabel(self):
        """Function to create frame type Label"""

        #creating label object
        self.typeLabel = Winforms.Label()
        #setting label position
        self.typeLabel.Location = draw.Point(480, 22)
        #setting label size
        self.typeLabel.Size = draw.Size(52, 20)
        #setting label text
        self.typeLabel.Text = "Type"
        #setting label font
        self.typeLabel.Font = self.labelsFont
        #adding label to controls
        self.Controls.Add(self.typeLabel)

    def createSendButton(self):
        """Function to create a send Button  : used for sending IP or MAC packets"""

        # creating button object
        self.sendButton = Winforms.Button()
        # setting location of button
        self.sendButton.Location = draw.Point(20, 20)
        # setting button size
        self.sendButton.Size = draw.Size(150, 40)
        # adding flat style to send button
        self.sendButton.FlatStyle = Winforms.FlatStyle.Flat
        #setting button's border
        self.sendButton.FlatAppearance.BorderSize = 0
        # Add button text
        self.sendButton.Text = "Send"
        # setting button font
        self.sendButton.Font = self.buttonsFont
        # setting Fore color
        self.sendButton.ForeColor = self.buttonsForeColor
        # setting Back color
        self.sendButton.BackColor = self.buttonsBackColor
        # adding on click event ( sendButtonOnClick function is triggered )
        self.sendButton.Click += self.sendButtonOnClick
        # adding button to the form
        self.Controls.Add(self.sendButton)

    def createReceiveButton(self):
        """Function to create Receive button : used for receiving IP or MAC packets"""

        # creating button object
        self.receiveButton = Winforms.Button()
        # setting location of button
        self.receiveButton.Location = draw.Point(200, 20)
        # setting button size
        self.receiveButton.Size = draw.Size(150, 40)
        # adding flat style to send button
        self.receiveButton.FlatStyle = Winforms.FlatStyle.Flat
        #setting button's border
        self.receiveButton.FlatAppearance.BorderSize = 0
        # Add button text
        self.receiveButton.Text = "Receive"
        # setting button font
        self.receiveButton.Font = self.buttonsFont
        # setting Fore color
        self.receiveButton.ForeColor = self.buttonsForeColor
        # setting Back color
        self.receiveButton.BackColor = self.buttonsBackColor
        # adding on click event ( receiveButtonOnClick function is triggered )
        self.receiveButton.Click += self.receiveButtonOnClick
        # adding button to the form
        self.Controls.Add(self.receiveButton)

    def createPacketsTextBox(self):
        """Function to create Packets text box which displays outgoing and incomming packets"""

        self.filename = ''

        self.word_wrap = 1

        self.doctype = 1

        self.saveFileDialog = Winforms.SaveFileDialog()

        self.saveFileDialog.Title = "Save document"

        self.saveFileDialog.FileName = "Untitled"

        self.richTextBox = Winforms.RichTextBox()

        self.richTextBox.Size = draw.Size(650, 400)

        self.richTextBox.ReadOnly = True

        self.richTextBox.TabIndex = 0

        self.richTextBox.AutoSize = 1

        self.richTextBox.ScrollBars = Winforms.RichTextBoxScrollBars.ForcedBoth

        self.richTextBox.Font = draw.Font("Courier New", System.Single(11))

        self.richTextBox.AcceptsTab = 1

        self.richTextBox.Location = draw.Point(20, 150)

        self.Controls.Add(self.richTextBox)

    def createSaveButton(self):
        """Function to create Save button : used for saving sent or received packets in a text file"""

        # creating button object
        self.saveButton = Winforms.Button()
        # setting location of button    
        self.saveButton.Location = draw.Point(550, 600)
        # setting button size
        self.saveButton.Size = draw.Size(120, 40)
        # adding flat style to send button
        self.saveButton.FlatStyle = Winforms.FlatStyle.Flat
        #setting button's border
        self.saveButton.FlatAppearance.BorderSize = 0
        # Add button text
        self.saveButton.Text = "Save"
        # setting button font
        self.saveButton.Font = self.buttonsFont
        # setting Fore color
        self.saveButton.ForeColor = self.buttonsForeColor
        # setting Back color
        self.saveButton.BackColor = self.buttonsBackColor
        # adding on click event ( saveButtonOnClick function is triggered )
        self.saveButton.Click += self.saveButtonOnClick
        # adding button to the form
        self.Controls.Add(self.saveButton)

    def createOnePacketRadioButton(self):
        """Function to create a radio button for one packet option """

        # creating radio button object
        self.onePacket = Winforms.RadioButton()
        # Add radio button text
        self.onePacket.Text = "One frame"
        # setting location of radio button   
        self.onePacket.Location = draw.Point(30, 80)
        # setting width
        self.onePacket.Width = 90
        # making it checked by default
        self.onePacket.Checked = True
        #adding radio button to controls
        self.Controls.Add(self.onePacket)

    def createMultiplePacketsRadioButton(self):
        """Function to create a radio button for multiple packets option """

        # creating radio button object
        self.multiplePackets = Winforms.RadioButton()
        # Add radio button text
        self.multiplePackets.Text = "Multiple frames"
        # setting location of radio button 
        self.multiplePackets.Location = draw.Point(120, 80)
        # setting width
        self.multiplePackets.Width = 110
        # unchecked by default
        self.multiplePackets.Checked = False
        #adding radio button to controls
        self.Controls.Add(self.multiplePackets)

    def createPayloadDataTextBox(self):
        """Function to create a payload data textbox"""

        #creating textbox object
        self.payloadData = Winforms.TextBox()
        #setting location
        self.payloadData.Location = draw.Point(520, 80)
        #setting a max length 
        self.payloadData.MaxLength = 14
        #setting texbox size
        self.payloadData.Size = draw.Size(150, 100)
        #setting Forecolor
        self.payloadData.ForeColor = draw.Color.FromName('Black')
        #Setting Font
        self.payloadData.Font = draw.Font("Lato", System.Single(8))
        #Setting a default text
        self.payloadData.Text = "00 02 03 04 09"
        #adding textbox to controls
        self.Controls.Add(self.payloadData)

    def createClearButton(self):
        """Function to create Clear button : used for clearing incomming and outgoing packets textbox"""

        # creating button object
        self.clearButton = Winforms.Button()
        # setting location of button    
        self.clearButton.Location = draw.Point(250, 600)
        # setting button size
        self.clearButton.Size = draw.Size(120, 40)
        # adding flat style to 
        self.clearButton.FlatStyle = Winforms.FlatStyle.Flat
        #setting button's border
        self.clearButton.FlatAppearance.BorderSize = 0
        # Add button text
        self.clearButton.Text = "Clear"
        # setting button font
        self.clearButton.Font = self.buttonsFont
        # setting Fore color
        self.clearButton.ForeColor = self.buttonsForeColor
        # setting Back color
        self.clearButton.BackColor = self.buttonsBackColor
        # adding on click event ( clearButtonOnClick function is triggered )
        self.clearButton.Click += self.clearButtonOnClick
        # adding button to controls
        self.Controls.Add(self.clearButton)

    def createSelectFrameTypeBox(self):
        """Function to create Combobox for frame type selection button when sending or receiving packets"""

        # creating Combobox object
        self.frameTypeSelectBox = Winforms.ComboBox()
        # setting location of Combobox
        self.frameTypeSelectBox.Location = draw.Point(520, 20)
        # setting Combobox size
        self.frameTypeSelectBox.Size = draw.Size(150, 100)
        # setting height of the drop down list 
        self.frameTypeSelectBox.DropDownHeight = 50
        # setting Fore color
        self.frameTypeSelectBox.ForeColor = draw.Color.FromName('Black')
        # adding flat style
        self.frameTypeSelectBox.FlatStyle = Winforms.FlatStyle.Flat
        #adding drop down list style to Combobox object
        self.frameTypeSelectBox.DropDownStyle = Winforms.ComboBoxStyle.DropDownList
        # setting Combobox font
        self.frameTypeSelectBox.Font = draw.Font("Lato", System.Single(8))
        # adding 1st item at index 0 of the drop down list
        self.frameTypeSelectBox.Items.Insert(0, "IP Packets")
        # adding 2nd item at index 1 of the drop down list
        self.frameTypeSelectBox.Items.Insert(1, "MAC")
        # setting the default value to IP Packets
        self.frameTypeSelectBox.SelectedIndex = 0
        # Adding on select event ( selectedFrameType function is triggered )
        self.frameTypeSelectBox.SelectedIndexChanged += self.selectedFrameType
        # adding Combobox object to controls
        self.Controls.Add(self.frameTypeSelectBox)

    def selectedFrameType(self, sender, args):
        """This function gets called when the user selects an item from the combobox
           It's used to check user selection and display a placeholder accordingly in the destinationMacIp textbox, to show the user the
           Data format they need to type in that text box"""

        if self.frameTypeSelectBox.SelectedIndex == 0:
            #If user selects Ip Packets option
            self.destinationMacIp.Text = "Ex. 192.168.1.1"
            self.destinationMacIp.ForeColor = draw.Color.FromName('Gray')
        
        elif self.frameTypeSelectBox.SelectedIndex == 1:
            #If user selects Mac option
            self.destinationMacIp.Text = "Ex. FF:FF:FF:FF:FF:FF"
            self.destinationMacIp.ForeColor = draw.Color.FromName('Gray')

    def destinationMacIpChanged(self, sender, args):
        """This function gets called when the text in destinationMacIp textbox changes.
           It checks if the text isnt equal to the default one(placeholder text)"""

        if self.destinationMacIp.Text != "Ex. 192.168.1.1" and self.destinationMacIp.Text != "Ex. FF:FF:FF:FF:FF:FF":
            #changing the color of the text to black
            self.destinationMacIp.ForeColor = draw.Color.FromName('Black')

    def createDestinationMacIpTextbox(self):
        """Function to create a textbox for the destination IP or MAC Address"""

        ##creating textbox object
        self.destinationMacIp = Winforms.TextBox()
        #setting textbox location
        self.destinationMacIp.Location = draw.Point(520, 50)
        #setting textbox size
        self.destinationMacIp.Size = draw.Size(150, 100)
        #setting textbox Forecolor
        self.destinationMacIp.ForeColor = draw.Color.FromName('Gray')
        #setting textbox font
        self.destinationMacIp.Font = draw.Font("Lato", System.Single(8))
        #setting text - placeholder
        self.destinationMacIp.Text = "Ex. 192.168.1.1"
        #adding GotFocus event, destinationMacIpTextBoxOnFocus gets called when the user clicks on this textbox
        self.destinationMacIp.GotFocus += self.destinationMacIpTextBoxOnFocus
        #adding LostFocus event, destinationMacIpTextBoxLostFocus gets called when the user clicks somewhere else
        self.destinationMacIp.LostFocus += self.destinationMacIpTextBoxLostFocus
        #adding TextChnged event, destinationMacIpChanged gets called when the text changes 
        self.destinationMacIp.TextChanged += self.destinationMacIpChanged
        #adding textbox to controls
        self.Controls.Add(self.destinationMacIp)

    def sendButtonOn(self):
        """This function changes the send button to ON behaviour"""

        #setting flag to 1 which indicates the send button is ON
        self.sendButtonFlag = 1
        #setting Forecolor
        self.sendButton.ForeColor = self.buttonsForeColor
        #setting backcolor
        self.sendButton.BackColor = draw.Color.FromArgb(59, 118, 1)
        #changing text of the send button
        self.sendButton.Text = "Stop send"
    
    def sendButtonOff(self):
        """This function changes the send button to OFF behaviour"""

        #setting flag back to 0 which indicates the send button is OFF
        self.sendButtonFlag = 0
        #setting Forecolor
        self.sendButton.ForeColor = self.buttonsForeColor
        #setting backcolor
        self.sendButton.BackColor = self.buttonsBackColor
        #changing text of the send button
        self.sendButton.Text = "Send"

    def checkHexValidity(self):
        """This function checks if the data entered by the user is in hexadecimal format"""

         for letter in self.payloadData.Text.lower():
            if letter not in "1234567890abcdef ":
                return True
                
    def destinationMacIpTextBoxOnFocus(self, sender, args):
        """This function is triggered when the user click on destinationMacIp textbox.
           It removes the placeholder text if the conditions are true"""

        if self.destinationMacIp.Text == "Ex. 192.168.1.1" or self.destinationMacIp.Text == "Ex. FF:FF:FF:FF:FF:FF":
            self.destinationMacIp.Text = ""

    def destinationMacIpTextBoxLostFocus(self, sender, args):
        """This function is triggered when the user click somewhere outside destinationMacIp textbox.
           It sets the placeholder text when conditions are met"""

        if self.destinationMacIp.Text == "":

            #changing color back to Gray
            self.destinationMacIp.ForeColor = draw.Color.FromName('Gray')

            if self.frameTypeSelectBox.SelectedIndex == 0:
                #If selected dropdownlist item is Ip packets, it sets the text back to the placeholder text
                self.destinationMacIp.Text = "Ex. 192.168.1.1"

            #If selected dropdownlist item is Mac frames, it sets the text back to the placeholder text 
            elif self.frameTypeSelectBox.SelectedIndex == 1:
                self.destinationMacIp.Text = "Ex. FF:FF:FF:FF:FF:FF"
            
    def sendButtonOnClick(self, sender, args):
        """This function gets called when send button is clicked. IT checks if the button is already ON or OFF, selected frame type, destination ip or mac address
           format and selected mode( one packet or multiple packets)"""

        #Checking if the button is ON, to turn it OFF by executing sendButtonOff function
        if self.sendButtonFlag == 1:
            self.sendButtonOff()

        #If the button is already Off
        else:

            if self.frameTypeSelectBox.SelectedIndex == 0:
                #checking destination ip format
                if not re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.destinationMacIp.Text.lower()):
                    #showing messagebox hwen the user types wrong ip format
                    Winforms.MessageBox.Show("Please check the format of the destination IP Address", "WARNING")
                
                #checking if the DATA format is in hexadecimal
                elif (len(self.payloadData.Text) - self.payloadData.Text.count(" ") ) % 2 != 0 or not re.match("[0-9a-fA-F]", self.payloadData.Text) or self.checkHexValidity():
                    Winforms.MessageBox.Show(
                        "Please check the format of the data Hexadecimal values", "WARNING")
                    
                else:
                    #sending one packet
                    if self.onePacket.Checked:
                        self.sendIpPackets()

                    #sending multiple packets
                    elif self.multiplePackets.Checked:
                        #turning send button on
                        self.sendButtonOn()
                        #disabling receive button
                        self.receiveButton.Enabled = False
                        #disabling other components
                        self.disableComponents()
                        #setting my ip
                        self.myIpOrMac = self.myIp
                        #getting destination ip
                        self.destIpOrMac = self.destinationMacIp.Text 

                        #Starting a thread for sending multiple packets
                        self.sendingThread = Thread(ThreadStart(self.sendIpPackets))
                        self.sendingThread.SetApartmentState(ApartmentState.STA)
                        self.sendingThread.Start()
                        
            #Mac frames 
            else:

                #checking destination mac address format
                if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", self.destinationMacIp.Text.lower()):
                    #showing messagebox hwen the user types wrong MAC format
                    Winforms.MessageBox.Show("Please check the format of the destination MAC Address", "WARNING")
                
                #check if data format is in hexadecimal
                elif (len(self.payloadData.Text) - self.payloadData.Text.count(" ") ) % 2 != 0 or not re.match("[0-9a-fA-F]", self.payloadData.Text) or self.checkHexValidity():
                    #show messagebox when Data format is not hexadecimal
                    Winforms.MessageBox.Show("Please check the format of the data Hexadecimal values", "WARNING")

                else:
                    #sending one packet
                    if self.onePacket.Checked:

                        self.sendMacFrames()

                    #sending multiple packets
                    elif self.multiplePackets.Checked:
                        #turning send button on
                        self.sendButtonOn()
                        #disabling receive button
                        self.receiveButton.Enabled = False
                        #disable other components
                        self.disableComponents()
                        #setting my MAC
                        self.myIpOrMac = self.myMac
                        #getting destination MAC
                        self.destIpOrMac = self.destinationMacIp.Text 

                        #Starting a thread for sending multiple packets
                        self.sendingThread = Thread(ThreadStart(self.sendMacFrames))
                        self.sendingThread.SetApartmentState(ApartmentState.STA)
                        self.sendingThread.Start()
                        
    def receiveButtonOnClick(self, sender, args):
        """This function gets called when the user clicks on receive button.
           it first checks the selected frame the user selects and then starts a thread"""
        
            #if user selects IP packets
            if self.frameTypeSelectBox.SelectedIndex == 0:
                #checking if received button is ON or OFF
                self.checkReceivedButtonClicked()
                #assigning myIp value
                self.myIpOrMac = self.myIp
                #Starting a thread to receive packets
                self.receiveThread = Thread(ThreadStart(self.receiveIpPacketsthread))
                self.receiveThread.SetApartmentState(ApartmentState.STA)
                self.receiveThread.Start()
                
            #If user selects Mac frame
            else:
                #assigning mac address
                self.myIpOrMac = self.myMac
                #checking if received button is ON or OFF
                self.checkReceivedButtonClicked()
                #starting receive thread
                self.receiveThread = Thread(ThreadStart(self.receiveMacFramesthread))
                self.receiveThread.SetApartmentState(ApartmentState.STA)
                self.receiveThread.Start()                           

    def receiveIpPacketsthread(self):
        """This function is the receive thread function for receiving IP packets"""
       
        def onEthMsgReceived(msg):
            """This function adds source,destination and the data sent from the source machine"""
            try:
                
                if msg.get_ipv4_layer().ipv4_header.ip_address_destination == self.myIp:
                    #checking if the received message destination ip address matches the machine ip address
                    data = ""
                    for i in msg.get_udp_layer().payload[:5]:
                        #iterating over the data in the payload and converting the value to hexadecimal
                        if len(hex(int(i))) <= 3:
                            data += "0"+hex(int(i))[2:] + " "
                        else:
                            data+=hex(int(i))[2:] + " "
                    #adding source,destination and data to the richTextBox ( displaying to user)
                    self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(msg.get_ipv4_layer().ipv4_header.ip_address_source,self.myIp,data) +"\r\n"

            except:
                pass
       
        while self.receiveButtonFlag and not self.exiting:
           #while loop which keeps the thread alive until the user clicks again on the receive button
           #and the exiting bool value is True
           
           #capturing messages and triggering onEthMsgReceived function
            g_ethernet_msg.on_message_received += onEthMsgReceived
            g_ethernet_msg.start_capture()
            sleep(1) #sleep for one second 
            g_ethernet_msg.stop_capture()
            g_ethernet_msg.on_message_received -= onEthMsgReceived

        #enabling send button and other elements after the thread is terminated and receiving process finishes
        self.sendButton.Enabled = True
        self.enableComponents()
    
    def receiveMacFramesthread(self):
        """This function is the receive thread function for receiving IP packets"""

        def onEthMsgReceived(msg):
            """This function adds source,destination and the data sent from the source machine"""

            try:

                #checking if the received message destination mac address matches the machine mac address
                if msg.mac_address_destination == self.myMac:
                    #iterating over the data in the payload and converting the value to hexadecimal
                    data=""
                    for i in msg.payload[:5]:
                        data+=hex(int(i))[2:] + " "
                    #adding source,destination and data to the richTextBox                       
                    self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(msg.mac_address_source, self.myMac,data) +"\r\n"
            
            except:
                pass
                
        
        while self.receiveButtonFlag and not self.exiting:
            #while loop which keeps the thread alive until the user clicks again on the receive button
            #and the exiting bool value is True
            
            #capturing messages and triggering onEthMsgReceived function
            g_ethernet_msg.on_message_received += onEthMsgReceived
            g_ethernet_msg.start_capture()
            sleep(1)#sleep for one second 
            g_ethernet_msg.stop_capture()
            g_ethernet_msg.on_message_received -= onEthMsgReceived

        #enabling send button and other elements after the thread is terminated and receiving process finishes
        self.sendButton.Enabled = True
        self.enableComponents()
        
    def sendMacFrames(self):
        """ send thread function and also used to send one packet"""

        #creating ethernet message which holds the source and destination mac addresses as well as the payload data
        g_ethernet_msg.mac_address_source = self.myMac
        g_ethernet_msg.mac_address_destination = self.destinationMacIp.Text
        g_ethernet_msg.payload = System.Array[Byte](bytearray.fromhex(self.payloadData.Text))


        #checking if user selected one packet or multiple packets option
        if self.onePacket.Checked:
            #sending one message
            g_ethernet_msg.send()
            #adding message information to richTextBox
            self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.myMac,self.destinationMacIp.Text,self.payloadData.Text) +"\r\n"
                

        #sending multiple messages 
        elif self.multiplePackets.Checked:

            #keeping the thread alive until the user clicks again on send button again and changing exiting bool value to True
            while self.sendButtonFlag and not self.exiting:
                g_ethernet_msg.send() #sending messages every 2 seconds
                
                #adding message information to richtextbox
                self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.myMac,self.destinationMacIp.Text,self.payloadData.Text) +"\r\n"

                sleep(2) #time sleep for 2 second

            #enabling components after the thread terminates
            self.receiveButton.Enabled = True
            self.enableComponents()

    def sendIpPackets(self):
        """This function is the send thread function, used to send Ip packets (one or multiple packets)"""

        #Creating udp messages
        udp_packet = message_builder.create_udp_message()
        #adding data to the message
        udp_packet.payload = System.Array[Byte](bytearray.fromhex(self.payloadData.Text))
        #add source ip address
        udp_packet.ipv4_header.ip_address_source = self.myIp
        #adding destination ip address
        udp_packet.ipv4_header.ip_address_destination = self.destinationMacIp.Text
        # adding source and destination port numbers
        udp_packet.udp_header.port_source = 9999
        udp_packet.udp_header.port_destination = 10000

        if self.onePacket.Checked:
            #sending one packet
            udp_packet.send()
            self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.myIp,self.destinationMacIp.Text,self.payloadData.Text) +"\r\n"


        elif self.multiplePackets.Checked:
            #sending multiple packets
            #keeping the thread alive until the user clicks again on send button again and changing exiting bool value to True

            #sending packet every 2 seconds
            while self.sendButtonFlag and not self.exiting:
                udp_packet.send() 
                self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.myIp,self.destinationMacIp.Text,self.payloadData.Text) +"\r\n"
                sleep(2) 
            
            #enabling components after send thread is terminated
            self.receiveButton.Enabled = True
            self.enableComponents()

    def checkReceivedButtonClicked(self):
        "This function checks if the receive button is ON or OFF, and changes it's behaviour"

        if self.receiveButtonFlag == 0:
            #changing flag to one (ie. ON)
            self.receiveButtonFlag = 1
            #changing colors
            self.receiveButton.ForeColor = self.buttonsForeColor
            self.receiveButton.BackColor = draw.Color.FromArgb(59, 118, 1)
            #changing text
            self.receiveButton.Text = "Stop receive"
            #disabling other components
            self.disableComponents()
            self.sendButton.Enabled = False
        else:
            #changing flag to zero(ie. OFF)
            self.receiveButtonFlag = 0
            #changing color back to off color
            self.receiveButton.ForeColor = self.buttonsForeColor
            self.receiveButton.BackColor = self.buttonsBackColor
            #changing text
            self.receiveButton.Text = "Receive"           

    def SaveChangesDialog(self,sender, FormClosingEventArgs):
        """This function gets called when the user click on X button of the GUI."""
        
        exitFormResult = Winforms.MessageBox.Show("Save changes?", "Exit !", Winforms.MessageBoxButtons.YesNoCancel) 
        if exitFormResult == Winforms.DialogResult.Yes:
            self.exiting = True
            self.SaveDocument()
        elif exitFormResult == Winforms.DialogResult.No:
            self.exiting = True 
        elif exitFormResult == Winforms.DialogResult.Cancel:
            FormClosingEventArgs.Cancel = True

    def saveButtonOnClick(self, sender, args):

        self.filename = ''
        self.SaveDocument()

    def SaveDocument(self):

        filename = self.filename
        if not filename:

            if self.saveFileDialog.ShowDialog() != Winforms.DialogResult.OK:

                return

            filename = self.saveFileDialog.FileName

        filename = self.filename = filename.lower()
        self.Text = 'Python Wordpad - %s' % filename
        self.richTextBox.Select(0, 0)
        stream = File.OpenWrite(filename)


        "My IP : {0} \nMY MAC: {1}", "Info".format(self.myIp, self.myMac)
        data = "{0:<29}{1:<25}{2}".format("Source","Destination","Payload") +"\r\n"+self.richTextBox.Text
        data = System.Text.Encoding.ASCII.GetBytes(System.String(data))
        stream.Write(data, 0, data.Length)
        stream.Close()

    def clearButtonOnClick(self, sender, args):
        """This function is triggered when clear button is clicked.
            It clears all the data (received and sent packets) in the textbox"""

        self.richTextBox.Clear()

    def formHelpButtonClicked(self, sender, CancelEventArgs):
        """This function is triggered when the the user clicks on the question mark on the gui.
           It shows the ip and the mac address of the machine"""

        Winforms.MessageBox.Show("My IP : {0} \nMY MAC: {1}".format(self.myIp, self.myMac), "Info")
        CancelEventArgs.Cancel = True
        
    def disableComponents(self):
        """This function gets called when send or receive buttons turns on.
           It is used to disable some components"""

        #disabling the radio buttons
        self.onePacket.Enabled = False
        self.multiplePackets.Enabled = False
        #disabling destination ip or mac textbox
        self.destinationMacIp.Enabled = False
        #disabling payload data textbox
        self.payloadData.Enabled = False
        #disabling combobox
        self.frameTypeSelectBox.Enabled = False
        #disabling save button
        self.saveButton.Enabled = False
    
    def enableComponents(self):
        """This function gets called when send or receive buttons turns OFF.
           It is used to enable some components"""
        
        #enabling the radio buttons
        self.onePacket.Enabled = True
        self.multiplePackets.Enabled = True
        #enabling destination ip or mac textbox
        self.destinationMacIp.Enabled = True
        #enabling payload data textbox
        self.payloadData.Enabled = True
        #enabling combobox
        self.frameTypeSelectBox.Enabled = True
        #enabling save button
        self.saveButton.Enabled = True


    ##KILL EVERYTHING WHEN CLOSED
    ##COMMENT THE CODE.....
    ##REMOVE REDUNDANT CODE
    
    ##ADD self.exiting


def app_thread():

    app = PacketAnalyser()

    Winforms.Application.Run(app)

    app.Dispose()


def main():

    thread = Thread(ThreadStart(app_thread))

    thread.SetApartmentState(ApartmentState.STA)

    thread.Start()

    thread.Join()


#----  MAIN  ----#
#if __name__ == '__main__':

main()

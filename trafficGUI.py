import clr
import re
import sys

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
from time import sleep


# --Globals
receive_button_flag = 0
send_button_flag = 0

class PacketAnalyser(Winforms.Form):

    
    def __init__(self):

        self.Text = "Packet Analyzer"  # Caption Text

        self.BackColor = draw.Color.FromArgb(
            250, 250, 250)  # color of the form

        self.FormSize = draw.Size(700, 700)  # form size

        self.elementsFont = draw.Font("Lato", System.Single(12))

        self.components = System.ComponentModel.Container()

        self.MinimumSize = draw.Size(700, 700)

        self.MaximumSize = draw.Size(700, 700)

        self.create_sendButton()
        self.create_receiveButton()
        self.create_exitButton()
        self.create_saveExitButton()
        self.create_selectFrameType()
        self.create_destination_mac_ip_textbox()
        self.createSourceLabel()
        self.createDestinationLabel()
        self.createPayloadLabel()
        self.createPacketsTextBox()
        self.createOnePacketRadioButton()
        self.createMultiplePacketsRadioButton()
        self.createPayloadTextBox()
        self.createPayloadDataLabel()
        self.createMacIpLabel()
        self.create_clear_button()
        self.createTypeLabel()

        self.saveFileDialog = Winforms.SaveFileDialog()
        # self.saveFileDialog.Filter = "Text Documents|*.txt|" \"Rich Text Format|*.rtf"

        self.saveFileDialog.Title = "Save document"
        self.saveFileDialog.FileName = "Untitled"

        self.HelpButton = True
        self.MaximizeBox = False
        self.MinimizeBox = False

        self.HelpButtonClicked += self.Form_HelpButtonClicked
        self.FormClosed += self.xClicked
        

        # self.my_ip = Logging.get_ip()
        # self.my_mac = Logging.get_mac()


        self.myIpOrMac = ""
        self.destIpOrMac = ""
        self.exiting = False
  

#    def Dispose(self):
#        
#        self.Dispose()
#
#        Winforms.Form.Dispose(self)


    def create_sendButton(self):

        # Send button

        self.sendButton = Winforms.Button()

        # location of button

        self.sendButton.Location = draw.Point(20, 20)

        # button size

        self.sendButton.Size = draw.Size(150, 40)

        # adding style to send button

        self.sendButton.FlatStyle = Winforms.FlatStyle.Flat

        self.sendButton.FlatAppearance.BorderSize = 0

        # Add button text

        self.sendButton.Text = "Send"

        # Define font of button

        self.sendButton.Font = self.elementsFont

        # sendButton color

        self.sendButton.ForeColor = draw.Color.FromName("White")

        self.sendButton.BackColor = draw.Color.FromArgb(255, 68, 90, 100)

        

        self.sendButton.Click += self.send_button_on_click

        # adding button to the form

        self.Controls.Add(self.sendButton)
        
    def createSourceLabel(self):
        self.sourceLabel = Winforms.Label()
        self.sourceLabel.Location = draw.Point(30, 130)
        self.sourceLabel.Size = draw.Size(70, 20)
        self.sourceLabel.Text = "Source"
        self.sourceLabel.Font = draw.Font("Lato", System.Single(9))
        self.Controls.Add(self.sourceLabel)

    def createDestinationLabel(self):
        self.DestinationLabel = Winforms.Label()
        self.DestinationLabel.Location = draw.Point(300, 130)
        self.DestinationLabel.Size = draw.Size(70, 20)
        self.DestinationLabel.Text = "Destination"
        self.DestinationLabel.Font = draw.Font("Lato", System.Single(9))
        self.Controls.Add(self.DestinationLabel)

    def createPayloadLabel(self):
        self.payloadLabel = Winforms.Label()
        self.payloadLabel.Location = draw.Point(550, 130)
        self.payloadLabel.Size = draw.Size(70, 20)
        self.payloadLabel.Text = "Data-hex"
        self.payloadLabel.Font = draw.Font("Lato", System.Single(9))
        self.Controls.Add(self.payloadLabel)

    def create_receiveButton(self):

        # Receive button object

        self.receiveButton = Winforms.Button()
        # location of button
        self.receiveButton.Location = draw.Point(200, 20)
        # button size
        self.receiveButton.Size = draw.Size(150, 40)
        # adding style to receive button
        self.receiveButton.FlatStyle = Winforms.FlatStyle.Flat
        self.receiveButton.FlatAppearance.BorderSize = 0
        # Add button text
        self.receiveButton.Text = "Receive"
        self.receiveButton.Font = draw.Font("Lato", System.Single(12))
        # Define font of button
        # self.receiveButton.Font = self.elementsFont
        # receiveButton color
        self.receiveButton.ForeColor = draw.Color.FromName("White")
        self.receiveButton.BackColor = draw.Color.FromArgb(255, 68, 90, 100)

        self.receiveButton.Click += self.receive_button_on_click

        # adding button to the form

        self.Controls.Add(self.receiveButton)

    def createPacketsTextBox(self):

        self.filename = ''

        self.word_wrap = 1

        self.doctype = 1

        self.saveFileDialog = Winforms.SaveFileDialog()

        # self.saveFileDialog.Filter = "Text Documents|*.txt|" \

        #                          "Rich Text Format|*.rtf"

        self.saveFileDialog.Title = "Save document"

        self.saveFileDialog.FileName = "Untitled"

        self.richTextBox = Winforms.RichTextBox()

        self.richTextBox.Size = draw.Size(650, 400)

        self.richTextBox.ReadOnly = True

        self.richTextBox.TabIndex = 0

        self.richTextBox.AutoSize = 1

        self.richTextBox.ScrollBars = Winforms.RichTextBoxScrollBars.ForcedBoth

        # self.richTextBox.Font = draw.Font("Loto", 10.0)
        self.richTextBox.Font = draw.Font("Courier New", System.Single(11))

        self.richTextBox.AcceptsTab = 1

        self.richTextBox.Location = draw.Point(20, 150)

        self.Controls.Add(self.richTextBox)

    def create_exitButton(self):

        # Exit button object

        self.exitButton = Winforms.Button()

        # location of button

        self.exitButton.Location = draw.Point(400, 600)

        # button size

        self.exitButton.Size = draw.Size(120, 40)

        # adding style to Exit button

        self.exitButton.FlatStyle = Winforms.FlatStyle.Flat

        self.exitButton.FlatAppearance.BorderSize = 0

        # Add button text

        self.exitButton.Text = "Exit"

        # Define font of button

        self.exitButton.Font = self.elementsFont

        # Exit Button color

        self.exitButton.ForeColor = draw.Color.FromName("White")

        self.exitButton.BackColor = draw.Color.FromArgb(255, 68, 90, 100)

        self.exitButton.Click += self.exit_button_on_click

        # adding button to the form

        self.Controls.Add(self.exitButton)

    def create_saveExitButton(self):


        # Exit button object

        self.saveExitButton = Winforms.Button()

        # location of button

        self.saveExitButton.Location = draw.Point(550, 600)

        # button size

        self.saveExitButton.Size = draw.Size(120, 40)

        # adding style to SaveExit button

        self.saveExitButton.FlatStyle = Winforms.FlatStyle.Flat

        self.saveExitButton.FlatAppearance.BorderSize = 0

        # Add button text

        self.saveExitButton.Text = "Save / Exit"

        # Define font of button

        self.saveExitButton.Font = self.elementsFont

        # SaveExit Button color

        self.saveExitButton.ForeColor = draw.Color.FromName("White")

        self.saveExitButton.BackColor = draw.Color.FromArgb(255, 68, 90, 100)

        self.saveExitButton.Click += self.saveExit_button_on_click

        # adding button to the form

        self.Controls.Add(self.saveExitButton)

    def createMacIpLabel(self):
        self.macIpLabel = Winforms.Label()
        self.macIpLabel.Location = draw.Point(480, 52)
        self.macIpLabel.Size = draw.Size(55, 20)
        self.macIpLabel.Text = "Dest."
        self.macIpLabel.Font = draw.Font("Lato", System.Single(9))
        self.Controls.Add(self.macIpLabel)
    
    def createPayloadDataLabel(self):
        self.payloadDataLabel = Winforms.Label()
        self.payloadDataLabel.Location = draw.Point(480, 82)
        self.payloadDataLabel.Size = draw.Size(52, 20)
        self.payloadDataLabel.Text = "Data"
        self.payloadDataLabel.Font = draw.Font("Lato", System.Single(9))
        self.Controls.Add(self.payloadDataLabel)
    
    def createTypeLabel(self):
        self.typeLabel = Winforms.Label()
        self.typeLabel.Location = draw.Point(480, 22)
        self.typeLabel.Size = draw.Size(52, 20)
        self.typeLabel.Text = "Type"
        self.typeLabel.Font = draw.Font("Lato", System.Single(9))
        self.Controls.Add(self.typeLabel)

    def create_selectFrameType(self):

        self.frameTypeSelectBox = Winforms.ComboBox()
        self.frameTypeSelectBox.Location = draw.Point(520, 20)
        self.frameTypeSelectBox.Size = draw.Size(150, 100)
        self.frameTypeSelectBox.DropDownHeight = 50
        self.frameTypeSelectBox.ForeColor = draw.Color.FromName('Black')
        self.frameTypeSelectBox.FlatStyle = Winforms.FlatStyle.Flat
        self.frameTypeSelectBox.DropDownStyle = Winforms.ComboBoxStyle.DropDownList
        self.frameTypeSelectBox.Font = draw.Font("Lato", System.Single(8))
        self.frameTypeSelectBox.Items.Insert(0, "IP Packets")
        self.frameTypeSelectBox.Items.Insert(1, "MAC")
        # self.frameTypeSelectBox.Items.Insert(2, "MAC")
        self.frameTypeSelectBox.SelectedIndex = 0
        self.frameTypeSelectBox.SelectedIndexChanged += self.selectedFrameType
        # self.frameTypeSelectBox.DrawMode = Winforms.DrawMode.Normal
        self.Controls.Add(self.frameTypeSelectBox)

    def selectedFrameType(self, sender, args):
        if self.frameTypeSelectBox.SelectedIndex == 0:
            
            
            self.destination_mac_ip.Text = "Ex. 192.168.1.1"
            self.destination_mac_ip.ForeColor = draw.Color.FromName('Gray')
        
        elif self.frameTypeSelectBox.SelectedIndex == 1:
            
            
            self.destination_mac_ip.Text = "Ex. FF:FF:FF:FF:FF:FF"
            self.destination_mac_ip.ForeColor = draw.Color.FromName('Gray')


    def destinationMacIpChanged(self, sender, args):
        if self.destination_mac_ip.Text != "Ex. 192.168.1.1" and self.destination_mac_ip.Text != "Ex. FF:FF:FF:FF:FF:FF":
            self.destination_mac_ip.ForeColor = draw.Color.FromName('Black')

    def create_destination_mac_ip_textbox(self):

        self.destination_mac_ip = Winforms.TextBox()
        self.destination_mac_ip.Location = draw.Point(520, 50)
        self.destination_mac_ip.Size = draw.Size(150, 100)
        self.destination_mac_ip.ForeColor = draw.Color.FromName('Gray')
        self.destination_mac_ip.Font = draw.Font("Lato", System.Single(8))
        self.destination_mac_ip.Text = "Ex. 192.168.1.1"
        self.destination_mac_ip.GotFocus += self.destinationMacIpTextBoxOnFocus
        self.destination_mac_ip.LostFocus += self.destinationMacIpTextBoxLostFocus
        self.destination_mac_ip.TextChanged += self.destinationMacIpChanged
        self.Controls.Add(self.destination_mac_ip)


    def sendButtonOn(self):
        global send_button_flag
        send_button_flag = 1
        self.sendButton.ForeColor = draw.Color.FromName("White")
        self.sendButton.BackColor = draw.Color.FromArgb(59, 118, 1)
        self.sendButton.Text = "Stop send"
    
    def sendButtonOff(self):
        global send_button_flag
        send_button_flag = 0
        self.sendButton.ForeColor = draw.Color.FromName("White")
        self.sendButton.BackColor = draw.Color.FromArgb(255, 68, 90, 100)
        self.sendButton.Text = "Send"

        # self.thread1.Start()
        print("on")
     
    def checkHexValidity(self):
         for letter in self.payload.Text.lower():
            if letter not in "1234567890abcdef ":
                return True
                
    def destinationMacIpTextBoxOnFocus(self, sender, args):
        if self.destination_mac_ip.Text == "Ex. 192.168.1.1" or self.destination_mac_ip.Text == "Ex. FF:FF:FF:FF:FF:FF":
            self.destination_mac_ip.Text = ""

    def destinationMacIpTextBoxLostFocus(self, sender, args):
    
        if self.destination_mac_ip.Text == "":
            self.destination_mac_ip.ForeColor = draw.Color.FromName('Gray')
            
            # if self.frameTypeSelectBox.SelectedIndex == 0:
            #     self.destination_mac_ip.Text = ""
            if self.frameTypeSelectBox.SelectedIndex == 0:
                self.destination_mac_ip.Text = "Ex. 192.168.1.1"
            elif self.frameTypeSelectBox.SelectedIndex == 1:
                self.destination_mac_ip.Text = "Ex. FF:FF:FF:FF:FF:FF"
            

    def send_button_on_click(self, sender, args):

        global send_button_flag

        if send_button_flag == 1:
            self.sendButtonOff()

        else:

            if self.frameTypeSelectBox.SelectedIndex == 0:

                if not re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.destination_mac_ip.Text.lower()):

                    Winforms.MessageBox.Show(
                        "Please check the format of the destination IP Address", "WARNING")
                #int(, 16)
                
                elif (len(self.payload.Text) - self.payload.Text.count(" ") ) % 2 != 0 or not re.match("[0-9a-fA-F]", self.payload.Text) or self.checkHexValidity():
                    Winforms.MessageBox.Show(
                        "Please check the format of the data Hexadecimal values", "WARNING")
                        
                else:

                    if self.onePacket.Checked:
                        self.sendIpPackets()

                    elif self.multiplePackets.Checked:

                        self.sendButtonOn()
                        self.receiveButton.Enabled = False
                        self.disableComponents()
                        self.myIpOrMac = self.my_ip
                        self.destIpOrMac = self.destination_mac_ip.Text 
                        self.thread2 = Thread(ThreadStart(self.sendIpPackets))
                        self.thread2.SetApartmentState(ApartmentState.STA)
                        self.thread2.Start()
                        

            else:

                if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", self.destination_mac_ip.Text.lower()):

                    Winforms.MessageBox.Show(
                        "Please check the format of the destination MAC Address", "WARNING")
                
                elif (len(self.payload.Text) - self.payload.Text.count(" ") ) % 2 != 0 or not re.match("[0-9a-fA-F]", self.payload.Text) or self.checkHexValidity():
                    Winforms.MessageBox.Show(
                        "Please check the format of the data Hexadecimal values", "WARNING")

                else:

                    if self.onePacket.Checked:

                        self.sendMacFrames()

                    elif self.multiplePackets.Checked:

                        self.sendButtonOn()
                        self.receiveButton.Enabled = False
                        self.disableComponents()
                        self.myIpOrMac = self.my_mac
                        self.destIpOrMac = self.destination_mac_ip.Text 
                        self.thread2 = Thread(ThreadStart(self.sendMacFrames))
                        self.thread2.SetApartmentState(ApartmentState.STA)
                        self.thread2.Start()
                        
                                 
    def create_clear_button(self):

        # Close button object

        self.clearButton = Winforms.Button()

        # location of button

        self.clearButton.Location = draw.Point(250, 600)

        # button size

        self.clearButton.Size = draw.Size(120, 40)

        # adding style to close button

        self.clearButton.FlatStyle = Winforms.FlatStyle.Flat

        self.clearButton.FlatAppearance.BorderSize = 0

        # Add button text

        self.clearButton.Text = "Clear"

        # Define font of button

        self.clearButton.Font = self.elementsFont

        # clear Button color

        self.clearButton.ForeColor = draw.Color.FromName("White")

        self.clearButton.BackColor = draw.Color.FromArgb(255, 68, 90, 100)

        self.clearButton.Click += self.clear_button_on_click

        # adding button to the form

        self.Controls.Add(self.clearButton)

    def createOnePacketRadioButton(self):

        self.onePacket = Winforms.RadioButton()
        self.onePacket.Text = "One frame"
        self.onePacket.Location = draw.Point(30, 80)
        self.onePacket.Width = 90
        self.onePacket.Checked = True
        self.Controls.Add(self.onePacket)

    def createMultiplePacketsRadioButton(self):

        self.multiplePackets = Winforms.RadioButton()
        self.multiplePackets.Text = "Multiple frames"
        self.multiplePackets.Location = draw.Point(120, 80)
        self.multiplePackets.Width = 110
        self.multiplePackets.Checked = False
        self.Controls.Add(self.multiplePackets)

    def createPayloadTextBox(self):
        self.payload = Winforms.TextBox()

        self.payload.Location = draw.Point(520, 80)
        self.payload.MaxLength = 14

        self.payload.Size = draw.Size(150, 100)

        self.payload.ForeColor = draw.Color.FromName('Black')


        self.payload.Font = draw.Font("Lato", System.Single(8))
        self.payload.Text = "00 02 03 04 09"
        


        self.Controls.Add(self.payload)

    def receiveIpPacketsthread(self):
        
       global receive_button_flag
       
       def on_eth_msg_received(msg):
            
            try:
                
                
                if msg.get_ipv4_layer().ipv4_header.ip_address_destination == self.my_ip:

                    x=""
                    for i in msg.get_udp_layer().payload[:5]:
                        
                        if len(hex(int(i))) <= 3:
                            x += "0"+hex(int(i))[2:] + " "
                        else:
                        
                            x+=hex(int(i))[2:] + " "
                    self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(msg.get_ipv4_layer().ipv4_header.ip_address_source,self.my_ip,x) +"\r\n"

            except:
                pass
       
       while receive_button_flag and not self.exiting:
           
           g_ethernet_msg.on_message_received += on_eth_msg_received
           g_ethernet_msg.start_capture()
           sleep(1)
           g_ethernet_msg.stop_capture()
           g_ethernet_msg.on_message_received -= on_eth_msg_received

            
       self.sendButton.Enabled = True
       self.enableComponents()
    
    def receiveMacFramesthread(self):

        global receive_button_flag

        def on_eth_msg_received(msg):
            try:
                
                if msg.mac_address_destination == self.my_mac:
                    
                    x=""
                    for i in msg.payload[:5]:
                        x+=hex(int(i))[2:] + " "
                    self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(msg.mac_address_source, self.my_mac,x) +"\r\n"
            
            except:
                pass
                
        
        while receive_button_flag and not self.exiting:
            

            g_ethernet_msg.on_message_received += on_eth_msg_received
            g_ethernet_msg.start_capture()
            sleep(1)
            g_ethernet_msg.stop_capture()
            g_ethernet_msg.on_message_received -= on_eth_msg_received

        self.sendButton.Enabled = True
        self.enableComponents()
        

    def sendMacFrames(self):

        g_ethernet_msg.mac_address_source = self.my_mac
        g_ethernet_msg.mac_address_destination = self.destination_mac_ip.Text
        g_ethernet_msg.payload = System.Array[Byte](bytearray.fromhex(self.payload.Text))


        if self.onePacket.Checked:
            g_ethernet_msg.send()
            self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.my_mac,self.destination_mac_ip.Text,self.payload.Text) +"\r\n"
                


        elif self.multiplePackets.Checked:
            while send_button_flag and not self.exiting:
                g_ethernet_msg.send()
                self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.my_mac,self.destination_mac_ip.Text,self.payload.Text) +"\r\n"

                sleep(1)
                
            self.receiveButton.Enabled = True
            self.enableComponents()

    def sendIpPackets(self):
        

        udp_packet = message_builder.create_udp_message()
        udp_packet.payload = System.Array[Byte](bytearray.fromhex(self.payload.Text))
        udp_packet.ipv4_header.ip_address_source = self.my_ip
        
        udp_packet.ipv4_header.ip_address_destination = self.destination_mac_ip.Text
        udp_packet.udp_header.port_source = 9999
        udp_packet.udp_header.port_destination = 10000

        if self.onePacket.Checked:
            udp_packet.send()
            self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.my_ip,self.destination_mac_ip.Text,self.payload.Text) +"\r\n"


        elif self.multiplePackets.Checked:
            while send_button_flag and not self.exiting:
                udp_packet.send()
                self.richTextBox.Text += "{0:<29}{1:<25}{2}".format(self.my_ip,self.destination_mac_ip.Text,self.payload.Text) +"\r\n"

                sleep(2)
                
            self.receiveButton.Enabled = True
            self.enableComponents()

    def checkReceivedButtonClicked(self):

        global receive_button_flag

        if receive_button_flag == 0:
            receive_button_flag = 1
            self.receiveButton.ForeColor = draw.Color.FromName("White")
            self.receiveButton.BackColor = draw.Color.FromArgb(59, 118, 1)
            self.receiveButton.Text = "Stop receive"
            self.disableComponents()
            self.sendButton.Enabled = False
        else:
            receive_button_flag = 0
            self.receiveButton.ForeColor = draw.Color.FromName("White")
            self.receiveButton.BackColor = draw.Color.FromArgb(255, 68, 90, 100)
            self.receiveButton.Text = "Receive"

    def receive_button_on_click(self, sender, args):
        
            # if self.frameTypeSelectBox.SelectedIndex == 0:

            #     Winforms.MessageBox.Show("Please select type of packet to receive", "WARNING")

            if self.frameTypeSelectBox.SelectedIndex == 0:
                self.checkReceivedButtonClicked()
                self.myIpOrMac = self.my_ip
                
                self.thread1 = Thread(ThreadStart(self.receiveIpPacketsthread))
                self.thread1.SetApartmentState(ApartmentState.STA)
                self.thread1.Start()
                

            else:
                self.myIpOrMac = self.my_mac
                self.checkReceivedButtonClicked()
                self.thread1 = Thread(ThreadStart(self.receiveMacFramesthread))
                self.thread1.SetApartmentState(ApartmentState.STA)
                self.thread1.Start()
               
       
    def exit_button_on_click(self, sender, args):
        self.exiting = True
        self.Close()

    def SaveChangesDialog(self):
        print(self.richTextBox.Modified)
        if Winforms.MessageBox.Show("Save changes?", "Exit !", Winforms.MessageBoxButtons.OK | Winforms.MessageBoxButtons.YesNo) == Winforms.DialogResult.Yes:
           self.SaveDocument()


    def saveExit_button_on_click(self, sender, args):

        self.filename = ''
        self.SaveDocument()
        # self.Close()

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


        "My IP : {0} \nMY MAC: {1}", "Info".format(self.my_ip, self.my_mac)
        data = "{0:<29}{1:<25}{2}".format("Source","Destination","Payload") +"\r\n"+self.richTextBox.Text
        data = System.Text.Encoding.ASCII.GetBytes(System.String(data))
        stream.Write(data, 0, data.Length)
        stream.Close()
        self.Close()

    def clear_button_on_click(self, sender, args):

        self.richTextBox.Clear()

    def Form_HelpButtonClicked(self, sender, CancelEventArgs):

        Winforms.MessageBox.Show("My IP : {0} \nMY MAC: {1}".format(self.my_ip, self.my_mac), "Info")

        CancelEventArgs.Cancel = True
        
    def xClicked(self, sender, CancelEventArgs):
        self.SaveChangesDialog()
        self.exiting = True


    def disableComponents(self):
        self.onePacket.Enabled = False
        self.multiplePackets.Enabled = False
        self.destination_mac_ip.Enabled = False
        self.payload.Enabled = False
        self.frameTypeSelectBox.Enabled = False
        #self.exitButton.Enabled = False
        self.saveExitButton.Enabled = False
    
    def enableComponents(self):
        self.onePacket.Enabled = True
        self.multiplePackets.Enabled = True
        self.destination_mac_ip.Enabled = True
        self.payload.Enabled = True
        self.frameTypeSelectBox.Enabled = True
        self.exitButton.Enabled = True
        self.saveExitButton.Enabled = True




    ##KILL EVERYTHING WHEN CLOSED

    ##POLISHING THE LAYOUT.............
    ##CHECK CAMELCASING......
    ##ADD DOCSTRING......
    ##COMMENT THE CODE.....
    ##save && save on close
    ##ONE SAME FONT colors (add constants etc) FOR ALL EXCEPT DATA TABLE
    ##REMOVE REDUNDANT CODE
    ##AVOID GLOBALS


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


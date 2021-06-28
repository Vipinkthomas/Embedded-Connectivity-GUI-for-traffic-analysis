#Import
from time import sleep

def on_eth_msg_received(msg):
    """function which gets called when a message is received in the receiver machine"""

    #Checking if destination mac address of the received message equals to the receiver MAC Address-Receive Addapter (Logging)
    if msg.mac_address_destination == Logging.get_mac():
        #Printing out the received message on ANDi console
        print "Received following message {0}".format(msg)


#Capturing messages for duration of 20 seconds
g_ethernet_msg.on_message_received += on_eth_msg_received
g_ethernet_msg.start_capture()
      
sleep(20)   
    
g_ethernet_msg.stop_capture()
g_ethernet_msg.on_message_received -= on_eth_msg_received
   




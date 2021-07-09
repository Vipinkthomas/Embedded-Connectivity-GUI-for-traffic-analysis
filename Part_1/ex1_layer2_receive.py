#Import
from time import sleep

#Setting a custom mac address
custom_mac = "11:22:33:44:55:66"

def on_eth_msg_received(msg):
    #Checking if source mac address in the message equals to custom_mac
    #we can also check if deestination mac address equals to Loopback adapter Mac address
    if msg.mac_address_source == custom_mac:
        #Printing out the received message on ANDi console
        print "Received following message from {0}: {1}".format(custom_mac, msg)


#Receiving messages for 20 seconds
g_ethernet_msg.on_message_received += on_eth_msg_received
g_ethernet_msg.start_capture()

sleep(20)


g_ethernet_msg.stop_capture()
g_ethernet_msg.on_message_received -= on_eth_msg_received
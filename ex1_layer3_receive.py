#Import
from time import sleep

#creating two variables (destination and source Ip addresses) which are same to Loopback adapter IP address
destination_ip = "169.254.247.134"
source_ip = "169.254.247.134"

def on_eth_msg_received(msg):
    """Function gets called when a message received"""

    #Checking if destination ip address in the message is equal to the Loopback adapter IP address
    if msg.get_ipv4_layer().ipv4_header.ip_address_destination == destination_ip:
        #Printing out the received message on ANDi console
        print "Received following message from {0}: {1}".format(source_ip, msg)

#capturing incoming messages for 20 seconds
g_ethernet_msg.on_message_received += on_eth_msg_received
g_ethernet_msg.start_capture()

sleep(20)

g_ethernet_msg.stop_capture()
g_ethernet_msg.on_message_received -= on_eth_msg_received
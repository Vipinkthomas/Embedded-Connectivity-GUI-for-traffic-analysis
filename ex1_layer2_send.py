#Import
from time import sleep

#Setting a custom source MAC Address of the message( not necessary for Loopback)
custom_mac ="11:22:33:44:55:66"
g_ethernet_msg.mac_address_source = custom_mac
#setting destination MAC address (same machine works as a sender and a receiver- Loopback)
g_ethernet_msg.mac_address_destination = "02:00:4C:4F:4F:50"

for i in range(20):
    #Loop which will change the first byte of the payload data and send a message every 1 second for 20 seconds
    if i < 10:
        #Increasing the first byte of the payload data
        dataset = "0{0} 02 03 04 09".format(i)
    else:
        dataset = "{0} 02 03 04 09".format(i)
    
    #Adding data to payload before sending the message
    g_ethernet_msg.payload = System.Array[Byte](bytearray.fromhex(dataset))
    g_ethernet_msg.send()
    
    #time sleep for 1 second
    sleep(1)


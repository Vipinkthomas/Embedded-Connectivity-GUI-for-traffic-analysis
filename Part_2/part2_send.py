#Import
from time import sleep

#setting source mac address of the message to the mac address of the sender machine.
#Getting MAc address from Stimulation(sender) adapter
g_ethernet_msg.mac_address_source = Stimulation.get_mac()
#setting destination mac address of the message to the other machine's MAC Address ( receiver )
g_ethernet_msg.mac_address_destination = "00:13:3B:B0:10:D7"

#Loop which will change the first byte of the payload data and send a message every 1 second for 20 seconds
for i in range(20):
    
    if i < 10:
        dataset = "0{0} 02 03 04 09".format(i)
    else:
        dataset = "{0} 02 03 04 09".format(i)
              
    g_ethernet_msg.payload = System.Array[Byte](bytearray.fromhex(dataset))
    g_ethernet_msg.send()
    
    sleep(1)


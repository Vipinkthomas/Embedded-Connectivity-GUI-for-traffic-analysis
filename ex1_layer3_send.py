#Import
from time import sleep

#Creating a udp message
udpMessage = message_builder.create_udp_message()
#setting the destination and source Ip addresses of the udp message to Loopback adapter IP address
udpMessage.ipv4_header.ip_address_source = "169.254.247.134"
udpMessage.ipv4_header.ip_address_destination = "169.254.247.134"
#setting source and destination port numbers
udpMessage.udp_header.port_source = 9999
udpMessage.udp_header.port_destination = 10000

#sending a message after every second for 20 seconds ( 20 messages )
for i in range(20):
    
    if i < 10:
        #Increasing the first byte of the payload data
        dataset = "0{0} 02 03 04 09".format(i)
    else:
        dataset = "{0} 02 03 04 09".format(i)

    #Adding data to payload before sending the message
    udpMessage.payload = System.Array[Byte](bytearray.fromhex(dataset))
    udpMessage.send()
    
    sleep(1)

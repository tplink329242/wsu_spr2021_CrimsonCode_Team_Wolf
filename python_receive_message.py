import PyConBehavior

my_connection = PyConBehavior.PyConFunction()

#register your name
my_connection.register_name('john')

#create a while loop for receive message
while True:
	#str_message = my_connection.receive_msg_from_server()
	str_message = my_connection.get_server_message()
	if str_message != []:
		print(str(str_message))		
		sender_new = str_message[0]
		sender_new = sender_new['sender']
		str_message = []
			
	my_connection.sleeptime(3)
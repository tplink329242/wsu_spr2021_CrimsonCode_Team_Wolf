import PyConBehavior

my_connection = PyConBehavior.PyConFunction()

#register your name
my_connection.register_name('john')

#create a while loop for receive message
while True:
	str_message = my_connection.get_server_message()
	if str_message == []:
		pass
	else:
		print(str(str_message))	
			
	my_connection.sleeptime(3)
import PyConBehavior

my_connection = PyConBehavior.PyConFunction()



str_message = []
my_connection.register_name('david')
receiver_name = ['john']
my_connection.tell_others_msg(receiver_name, 'hello world!')
while True:
	str_message = my_connection.get_server_message()
	if str_message == []:
		pass
	else:
		print(str(str_message))
	str_file = my_connection.get_server_files()
	my_connection.sleeptime(3)
	if str_file == []:
		pass
	else:
		print(str(str_file))
		print(str_file[0]['content'])
		str_file_temp = str_file[0]
		str_file_temp = str_file_temp['content']

		my_connection.save_transfrom_files(str_file_temp)
		my_connection.__del__()


#print(str(my_connection.receive_msg_from_server()))

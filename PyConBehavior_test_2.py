import PyConBehavior
import time

my_connection = PyConBehavior.PyConFunction()

my_connection.register_name('john')

receiver_name = ['david']
time.sleep(10)
my_connection.tell_others_msg(receiver_name, 'hello world!')

while True:
	str_message = my_connection.get_server_message()
	if str_message == []:
		pass
	else:
		print(str(str_message))
		break

#my_connection.transform_file_to_other(receiver_name, 'img1.png')
#print('send success')
#my_connection.__del__()

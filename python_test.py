import PyConBehavior


#init connection
my_connection = PyConBehavior.PyConFunction()

#register your name
my_connection.register_name('david')

#init message,type is list
str_message = []

#define a receiver name
receiver_name = ['john']

#send message using connection
my_connection.tell_others_msg(receiver_name, 'hello world 1!')

#close the connection
#del my_connection
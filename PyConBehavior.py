import time
import socket
import json
import base64
import threading
import boto3

#var type
file_type_dict = {}
file_type_dict['zip'] = '1'
file_type_dict['png'] = '2'
file_type_dict['html'] = '3'
file_type_dict['json_string'] = '4'
file_type_dict['html_pic'] = '5'
file_type_dict['html_pic_large'] = '6'
file_type_dict['html_pic_attach_large'] = '7'
file_type_dict['register_name'] = '8'
file_type_dict['tell_to_somebody'] = '9'
file_type_dict['file_transfer'] = '10'


HEADER_LENGTH = 15
HEADER_LENGTH_MAIL = 20
MAX_LEN_LENGTH = 10
MAX_LEN_LENGTH_MAIL = 15
MAX_TYPE_LENGTH = 5


global_msg_str_received_list = []
global_msg_file_received_list = []


class Thread_Sub_Client (threading.Thread):
	
	def __init__(self, threadID, name, sock_connection):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.sock_connection = sock_connection

	def __del__(self):
		self.sock_connection.close()
		return 0

	def run(self):
		self.Thread_Sub_In(self.sock_connection)

	def Thread_Sub_In(self, connection):
		
		msg_full = ''
		msg_new = True
		client_name = ''

		while True:

			try:
				msg_received = connection.recv(1024).decode('utf-8')
			except:
				break
			
			if len(msg_received) > 0:
				if msg_new:

					msg_type = msg_received[:MAX_TYPE_LENGTH]
					msg_type = int(msg_type)
					if msg_type == 10:
						msg_length = int(msg_received[MAX_TYPE_LENGTH:HEADER_LENGTH_MAIL])
					else:
						msg_length = int(msg_received[MAX_TYPE_LENGTH:HEADER_LENGTH])

					#print(f'new message length :{msg_length}')
					msg_new = False

				msg_full += msg_received

			if msg_type == 9 :
				if len(msg_full) - HEADER_LENGTH == msg_length:
					#print('full msg received from server!')
					global global_msg_str_received_list
					msg_content = {}
					msg_content = json.loads(msg_full[HEADER_LENGTH:])
					global_msg_str_received_list.append(msg_content)
					msg_full = ''
					msg_new = True
					msg_type = ''

			elif msg_type == 10 :
				if len(msg_full) - HEADER_LENGTH_MAIL == msg_length:
					#print('full msg received from server!')

					global global_msg_file_received_list
					
					msg_content = {}
					msg_content = json.loads(msg_full[HEADER_LENGTH_MAIL:])
					global_msg_file_received_list.append(msg_content)
					msg_full = ''
					msg_new = True
					msg_type = ''

			else:
				if len(msg_full) - HEADER_LENGTH == msg_length:
					#print('full msg received!')

					msg_full = ''
					msg_new = True
					msg_type = ''

		return 0



class PyConFunction(object):

	def __init__(self):
		try:
			self.sock_ec2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock_ec2.connect(('localhost', 5553))
			self.sock_ec2.send(b'Ubisoft@123412341234')

			if self.sock_ec2.recv(1024).decode('utf-8') == 'welcome to ec2!' :
				thread_received = Thread_Sub_Client(1, 'received_from_server', self.sock_ec2)
				thread_received.start()

			else:
				print('wrong cred! please check your cred and try again!')
			
		except:
			print('fail to init connection to server, please check your network and try again!')
		
		self.list_image = []
		self.dict_attachments = {}
		self.reg_name = ''
		self.msg_str_received_list = []
		self.msg_file_received_list = []

	def __del__(self):
		#self.sock_ec2.close()
		self.sock_close()
		return 0

	def get_server_message(self):

		global global_msg_str_received_list
		try:
			self.msg_str_received_list = global_msg_str_received_list
						
		except:
			pass
			#print('failed to read data!')

		global_msg_str_received_list = []
		return self.msg_str_received_list

	def get_server_files(self):

		global global_msg_file_received_list
		try:
			self.msg_file_received_list = global_msg_file_received_list
		except :
			print('failed to read data!')
		
		global_msg_file_received_list = []
		return self.msg_file_received_list

	def save_transfrom_files(self, str_received_files):
	
		rec_received_files = {}
		rec_received_files = str_received_files

		#rec_received_files = json.loads(str_received_files)
	
		for attachment_temp in rec_received_files:
			attach_part = base64.b64decode(rec_received_files[attachment_temp])
			fo = open(attachment_temp, "wb")
			fo.write(attach_part)
			fo.close()
		return 0

	def sleeptime(self, delayseconds):
		time.sleep(delayseconds)
		return 0

	def msg_generate(self, content, file_type):
		code_type = 0
		if file_type == 'zip':
			code_type = file_type_dict['zip']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'png':
			code_type = file_type_dict['png']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'html':
			code_type = file_type_dict['html']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'html_pic':
			code_type = file_type_dict['html_pic']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'html_pic_large':
			code_type = file_type_dict['html_pic_large']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'html_pic_attach_large':
			code_type = file_type_dict['html_pic_attach_large']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'register_name':
			code_type = file_type_dict['register_name']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'tell_to_somebody':
			code_type = file_type_dict['tell_to_somebody']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'file_transfer':
			code_type = file_type_dict['file_transfer']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		elif file_type == 'json_string':
			code_type = file_type_dict['json_string']
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'
		else:
			code_type = 0
			code_type = f'{code_type:<{MAX_TYPE_LENGTH}}'

		if file_type == 'html_pic_large':
			
			if len(content) > 99999999999999 :
				print('file size overloading')
				return 1
			else:
				len_str = f'{len(content):<{MAX_LEN_LENGTH_MAIL}}'
				return code_type + len_str + content

		elif file_type == 'html_pic_attach_large':

			if len(content) > 99999999999999 :
				print('file size overloading')
				return 1
			else:
				len_str = f'{len(content):<{MAX_LEN_LENGTH_MAIL}}'
				return code_type + len_str + content

		elif file_type == 'file_transfer':
	
			if len(content) > 99999999999999 :
				print('file size overloading')
				return 1
			else:
				len_str = f'{len(content):<{MAX_LEN_LENGTH_MAIL}}'
				return code_type + len_str + content
				
		else:
			if len(content) > 999999999 :
				print('file size overloading')
				return 1
			else:
				len_str = f'{len(content):<{MAX_LEN_LENGTH}}'
				return code_type + len_str + content

	def add_picture_to_report(self, filename):

		try:
			with open(filename,'rb') as image1:
				image1 = image1.read()
				image1 = base64.b64encode(image1)
				image1_str = image1.decode('ascii')
				self.list_image.append(image1_str)
		except:
			print('fail to add this picture to upload queue!')
			return 1

		return 0

	def add_attachment_to_report(self, filename):
	
		try:
			with open(filename,'rb') as image1:
				image1 = image1.read()
				image1 = base64.b64encode(image1)
				image1_str = image1.decode('ascii')
				self.dict_attachments[filename] = image1_str
		except:
			print('fail to add this attachment to upload queue!')
			return 1

		return 0
	
	def send_email_with_pic_and_attach(self, content, title, receiver, object_type):
	
		send_dict = {}
		send_dict['content'] = content
		send_dict['title'] = title
		send_dict['receiver'] = receiver

		if self.list_image != [] : 
			send_dict['image'] = self.list_image

		if self.dict_attachments != {} : 
			send_dict['attachment'] = self.dict_attachments

		content = json.dumps(send_dict)
		send_body = bytes(self.msg_generate(content, object_type), 'utf-8')

		self.sock_ec2.send(send_body)

	def register_name(self, id_name):

		object_type = 'register_name'
		self.reg_name = id_name
		send_body = bytes(self.msg_generate(self.reg_name, object_type), 'utf-8')
		self.sock_ec2.send(send_body)

		return 0

	def tell_others_msg(self, name, content):
	
		object_type = 'tell_to_somebody'
		msg_dict = {}
		msg_dict['receiver'] = name
		msg_dict['msg_content'] = content

		send_content = json.dumps(msg_dict)
		send_body = bytes(self.msg_generate(send_content, object_type), 'utf-8')
		self.sock_ec2.send(send_body) 
		return 0

	def transform_file_to_other(self, receiver, filename):
	
		try:
			with open(filename,'rb') as image1:
				image1 = image1.read()
				image1 = base64.b64encode(image1)
				image1_str = image1.decode('ascii')
				send_content = {}
				send_content[filename] = image1_str
		except:
			print('fail to ready this file!')
			return 1

		object_type = 'file_transfer'
		msg_dict = {}
		msg_dict['receiver'] = receiver
		msg_dict['msg_content'] = send_content
		send_content = json.dumps(msg_dict)
		send_body = bytes(self.msg_generate(send_content, object_type), 'utf-8')

		try:
			self.sock_ec2.send(send_body)
		except:
			print('fail to send this file!')
		
		return 0

	def sock_close(self):
		self.sock_ec2.send(b'client_deactive')
		return 0

	def receive_msg_from_server(self):
		self.sleeptime(1)
		try:
			json_receive_content = self.sock_ec2.recv(1024).decode('utf-8')
		except:
			return 0

		receive_content = ''

		if len(json_receive_content) > 0:
			try:
				receive_content = json.loads(json_receive_content)
			except :
				print(str(json_receive_content))
			
			return receive_content
		else:
			return receive_content

	def connect_to_aws_sqs_and_snd_message(sqs_name, sqs_msg_body):
		sqs_sms = boto3.resource('sqs')
		queue_sms = sqs_sms.get_queue_by_name(sqs_name)
		response_sms = queue_sms.send_message(MessageBody=sqs_msg_body)
		return response_sms

	

		

	
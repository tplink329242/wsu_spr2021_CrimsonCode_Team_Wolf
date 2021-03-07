import socket
import time
import datetime
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header

import threading
import json
import base64

HEADER_LENGTH = 15
HEADER_LENGTH_MAIL = 20
MAX_LEN_LENGTH = 10
MAX_LEN_LENGTH_MAIL = 15
MAX_TYPE_LENGTH = 5

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


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 5553))
sock.listen(5)


client_dict = {}
client_list = []

threadLock = threading.Lock()


def msg_generate(content, file_type):
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



def mail_ali_send_with_title_pic_attach_and_receiver(title, content, receiver, image = [], attach = {}):
	# 发件人地址，通过控制台创建的发件人地址
	username = 'someone@wsu.edu'
	# 发件人密码，通过控制台创建的发件人密码
	password = '1234'
	# 自定义的回复地址
	replyto = ''
	# 收件人地址或是地址列表，支持多个收件人，最多30个
	#rcptto = '***,***'
	rcptto = 'receiver@wsu.edu'
	# 构建alternative结构
	#msg = MIMEMultipart('alternative')
	msg = MIMEMultipart('related')
	msg['Subject'] = Header(str(title)).encode()
	msg['From'] = '%s <%s>' % (Header('receiver@wsu.edu').encode(), username)
	msg['To'] = rcptto
	msg['Reply-to'] = replyto
	msg['Message-id'] = email.utils.make_msgid()
	msg['Date'] = email.utils.formatdate() 
	# 构建alternative的text/plain部分
	textplain = MIMEText(content, _subtype='html', _charset='UTF-8')
	msg.attach(textplain)

	list_image = []
	list_image = image
	dict_attachment = {}
	dict_attachment = attach

	count_image = 1

	if list_image != []:
		for image_temp in list_image:
			image_temp = base64.b64decode(image_temp)
			pic = MIMEImage(image_temp)
			id_str_image_content = 'image' + str(count_image)
			pic.add_header('Content-ID', id_str_image_content)
			msg.attach(pic)
			count_image = count_image + 1
	
	if dict_attachment != {}:
		for attachment_temp in dict_attachment:
			attach_part = base64.b64decode(dict_attachment[attachment_temp])
			attach_mail = MIMEApplication(attach_part)
			attach_mail.add_header('Content-Disposition', 'attachment', filename = attachment_temp)
			msg.attach(attach_mail)

	# 发送邮件
	try:
		client = smtplib.SMTP()
		#python 2.7以上版本，若需要使用SSL，可以这样创建client
		#client = smtplib.SMTP_SSL()
		#SMTP普通端口为25或80
		client.connect('smtpdm.aliyun.com', 25)
		#开启DEBUG模式
		client.set_debuglevel(0)
		client.login(username, password)
		#发件人和认证地址必须一致
		#备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
		#      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
		client.sendmail(username, receiver, msg.as_string())
		client.quit()
		print ('邮件发送成功！')
	except smtplib.SMTPConnectError as e:
		print ('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
	except smtplib.SMTPAuthenticationError as e:
		print ('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
	except smtplib.SMTPSenderRefused as e:
		print ('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
	except smtplib.SMTPRecipientsRefused as e:
		print ('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
	except smtplib.SMTPDataError as e:
		print ('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
	except smtplib.SMTPException as e:
		print ('邮件发送失败, ', e.message)
	except Exception as e:
		print ('邮件发送异常, ', str(e))
	return 0

def tell_other_msg(connection, sender, receiver, content, msgtype='tell_to_somebody'):

	receiver_list = []
	receiver_list = receiver
	send_dict ={}
	send_dict['sender'] = sender
	send_dict['content'] = content

	try:
		send_content = json.dumps(send_dict)
		send_content = msg_generate(send_content, msgtype)
	except :
		connection.send(b'unable to generate message!')	

	bytes_send_content = bytes(send_content, 'utf-8')

	for receiver_name in receiver_list:

		threadLock.acquire()
		try:
			receiver_connection = client_dict[receiver_name]
			receiver_connection.send(bytes_send_content)
		except:
			connection.send(b'failed to send this message!')				
		threadLock.release()

	return 0



def Thread_Sub_In(connection, ID_connection):

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
				print(f'new message type :{msg_received[:MAX_TYPE_LENGTH]}')
				msg_type = msg_received[:MAX_TYPE_LENGTH]
				# msg_type = str(msg_type).rstrip()
				msg_type = int(msg_type)
				#print(msg_type)
				if msg_type == 6:
					msg_length = int(msg_received[MAX_TYPE_LENGTH:HEADER_LENGTH_MAIL])
				if msg_type == 7:
					msg_length = int(msg_received[MAX_TYPE_LENGTH:HEADER_LENGTH_MAIL])
				if msg_type == 10:
					msg_length = int(msg_received[MAX_TYPE_LENGTH:HEADER_LENGTH_MAIL])
				else:
					msg_length = int(msg_received[MAX_TYPE_LENGTH:HEADER_LENGTH])

				print(f'new message length :{msg_length}')
				msg_new = False

			msg_full += msg_received

		if msg_type == 6 :
			if len(msg_full) - HEADER_LENGTH_MAIL == msg_length:
				print('full msg received!')
				
				msg_content = {}
				msg_content = json.loads(msg_full[HEADER_LENGTH_MAIL:])
				title = msg_content['title']
				content = msg_content['content']
				receiver = msg_content['receiver']
				image = msg_content['image']

				msg_full = ''
				msg_new = True
				msg_type = ''

		elif msg_type == 7 :
			msg_full_len = len(msg_full) - HEADER_LENGTH_MAIL
			if msg_full_len == msg_length:
				print('full msg received!')
				msg_content = {}
				msg_content = json.loads(msg_full[HEADER_LENGTH_MAIL:])
				title = msg_content['title']
				content = msg_content['content']
				receiver = msg_content['receiver']
				print(str(receiver))
				try:
					image = msg_content['image']
				except:
					image = []

				try:
					attachment_mail = msg_content['attachment']
				except:
					attachment_mail = {}
				
				mail_ali_send_with_title_pic_attach_and_receiver(title, content, receiver, image, attachment_mail)

				msg_full = ''
				msg_new = True
				msg_type = ''

		elif msg_type == 8 :

			if len(msg_full) - HEADER_LENGTH == msg_length:
				print('full msg received!')
				
				msg_content = msg_full[HEADER_LENGTH:]
				client_name = msg_content

				threadLock.acquire()
				try:
					client_dict[client_name] = connection
				except:
					connection.send(b'failed to reg name on this server!')
					connection.close()				
				threadLock.release()

				msg_full = ''
				msg_new = True
				msg_type = ''

		elif msg_type == 9 :

			msg_full_len = len(msg_full) - HEADER_LENGTH
			if msg_full_len == msg_length:
				print('full msg received!')
				
				msg_content = {}
				msg_content = json.loads(msg_full[HEADER_LENGTH:])

				try:
					msg_receiver = msg_content['receiver']
					msg_send_content = msg_content['msg_content']
					tell_other_msg(connection, client_name, msg_receiver, msg_send_content)
				except:
					connection.send(b'failed to deliever message!')
					connection.close()

				msg_full = ''
				msg_new = True
				msg_type = ''

		elif msg_type == 10 :

			msg_full_len = len(msg_full) - HEADER_LENGTH_MAIL
			if msg_full_len >= msg_length:
				print('full msg received!')
				
				msg_content = {}
				msg_content = json.loads(msg_full[HEADER_LENGTH:])

				try:
					msg_receiver = msg_content['receiver']
					msg_send_content = msg_content['msg_content']
					tell_other_msg(connection, client_name, msg_receiver, msg_send_content, 'file_transfer')
				except:
					connection.send(b'failed to deliever message!')
					connection.close()

				msg_full = ''
				msg_new = True
				msg_type = ''


		else:
			if len(msg_full) - HEADER_LENGTH == msg_length:
				print('full msg received!')

				if msg_type == 'html':
					print("msg")
				#elif msg_type =='5    ':
				elif msg_type == 5 :
					msg_content = {}
					msg_content = json.loads(msg_full[HEADER_LENGTH:])
					content = msg_content['content']
					receiver = msg_content['receiver']
					image1 = msg_content['image1']
					image1 = bytes(image1,'ascii')
					#image1 = image1.decode('ascii')
					image1_dec = base64.b64decode(image1)
					image2 = msg_content['image2']
					image2 = bytes(image2,'ascii')
					#image2 = image2.decode('ascii')
					image2_dec = base64.b64decode(image2)

				msg_full = ''
				msg_new = True
				msg_type = ''

	try:
		del client_dict[client_name]
	except:
		pass
	
	return 0


class Thread_Sub_Client (threading.Thread):

	def __init__(self, threadID, name, counter, connection, ID_connection):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.connection = connection
		self.ID_connection = ID_connection

	def run(self):
		print ("开启线程： " + self.name + str(self.ID_connection))
		# 获取锁，用于线程同步
		#threadLock.acquire()
		Thread_Sub_In(self.connection, self.ID_connection)
		# 释放锁，开启下一个线程
		#threadLock.release()
		print ("关闭线程： " + self.name)

while True:
	connection, addr = sock.accept()
	try:
		msg_received = connection.recv(1024).decode('utf-8')
		if msg_received == 'Ubisoft@123412341234':
			connection.send(b'welcome to ec2!')
			mythread = Thread_Sub_Client(1, 'sub_client_thred', 5, connection, connection.fileno())
			#mythread = threading.Thread(target=Thread_Sub_In, args=(connection, connection.fileno()))
            #mythread.setDeamon(True)
			mythread.start()
		else:
			connection.send(b'wrong msg! please check your msg and try again!')
			connection.close()
	except:
		pass





class User:
	def __init__(self,name,user,pas):
		self.username = user.title()
		self.password = pas
		self.name = name
		
	def checkUser(self,user):
		return self.username == user.title()
		
	def checkPass(self,pas):
		return self.password == pas
		
	def setPass(self,n_pas):
		self.password = n_pas
		
	def __str__(self):
		return 'Name: %s\nUsername: %s\nPassword: %s' %(self.name,self.username,self.password)
		
	def save(self):
		return ','.join((self.name,self.username,self.password))
		
	def __eq__(self,obj):
		return isinstance(obj,User) and self.username == obj.username
		
	def __ne__(self,obj):
		return not self == obj
		
class Accounts:
	
	def __init__(self,s_file):
		self.accts = []
		self.s_file = s_file
		try:
			with open(s_file,'r') as f:
				source = f.read().splitlines()
				for s in source:
					self.accts.append(User(*s.split(',')))
		except FileNotFoundError:
			print('File not found')
		except Exception as e:
			print('wrong data in file',e)
			
	def display_users(self):
		for no,user in zip(range(1,len(self.accts)+1),self.accts):
			print(f'{no:<2}\n',user, sep='')
	
	def save(self):
		with open(self.s_file,'w') as f:
			f.write('\n'.join(map(User.save,self.accts)))
						
	def find(self,user):
		for u in self.accts:
			if u.checkUser(user): return u
			
	def login(self):
		print('Login'.center(20,'='))
		user = self.find(input('Username: '))
		if not user:
			print('Usename does not exist\n')
		else:	
			trial = 1
			while trial < 4:
				if user.checkPass(input('Password: ')):
					print('Hi %s, login successful\n' %user.name)
					return True
				else: print('incorrect password')
				trial += 1
			print('max trial exceeded\n')
		return False
					
	def register(self):
		print('\nEnter Account details\n')
		temp = User(input('Name: '),input('Username: '),input('Password: '))
		if temp in self.accts:
			print('Username already exist')
			if input('retry (y/n): ') == 'y' :
				self.register()
		else:
			print('Account successfully registered')
			self.accts.append(temp)
			self.save()
		
	def changePass(self):
		user = self.find(input('Username: ').title())
		if not user:
			print('Account does not Exist!')
		else:
			if user.checkPass(input('Enter old password: ')):
				user.setPass(input('Enter new password: '))
				print('password changed successfully')
				self.save()
			else: print('incorrect password')		
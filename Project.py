class Item:
	'''This class represent any item to be sold in the shop
it has two constructors:
	Iteme(name,quantity,unitPrice) and
	Item(name) whic initialise everything to zero'''
	def __init__(self,name,quan,unitP):
		self.name = name
		self.quan = quan
		self.unitPrice = unitP
		
	#Overriding == operator to compare with item name
	def __eq__(self,obj):
		return isinstance(obj,Item) and obj.name == self.name
		
	def __ne__(self,obj):
		return not self == obj
		
	def setPrice(self,newP):
		self.unitPrice = newP
		
	def getPrice(self):
		return self.unitPrice
		
	def getQuantity(self):
		return self.quan
		
	def updateQuantity(self,qua):
		self.quan += qua
		
	def buy(self,quan):
		
		'''buy an item takes one parameter: quan
and return the amount of the quantity bought and update
Items quantity
'''
		amount = quan * self.unitPrice
		self.quan -= quan
		return amount
			
	def is_avail(self):
		return self.quan != 0
		
	def __str__(self):
		item = '{:<25}{:^10,d}{:>10,.2f}'.format(self.name,self.quan,self.unitPrice)
		return item
		
	def save(self):
		return '{},{:d},{:,.1f}'.format(self.name,self.quan,self.unitPrice)
#end of class Item

class SuperMarket:
	'''Main Class where each good is stored as an Item object
	It has one Constructor that takes a file path for the Items
	in the super market and creates'''
	title = ('='*60) + '\n' + 'MAL ADAMU IFE RETAIL MARKET'.center(60) + '\n'+ ('='*60)
	def __init__(self,file_path):
		self.stock_file = file_path
		self.sales_file = 'sales.csv'
		self.store = []
		self.sales = {}
		source = []
		sales = []
		try:
			with open(file_path,'r') as f:
				source = f.read().splitlines()
			with open('sales.csv') as f:
				sales = f.read().splitlines()
			for line in source:
				itm = line.split(',')
				self.store.append(Item(itm[0],int(itm[1]),float(itm[2])))
			for sale in sales:
				s = sale.split(',')
				self.sales[s[0]] = float(s[1])
		except FileNotFoundError:
			print('file not fount')
		except IndexError:
			print('file data not in required format !!')
			
	def display(self,nos=0,adm = False):
		'''Method that display Items in the supermarket, takes 2 optional param
		nos that indicate no of items to display, -ve value to pick from last, if not given all are displayed base on adm val
		adm if True print all items regardless of their quantity, false return only items with quantity != 0'''
		header = '{:^2} {:<20}{:^15}{:>12}'.format('ID','Item Name','Av. Quantity','Unit Price(N)')
		print(self.title + '\n' + header)
		f = lambda it : it.is_avail() or adm
		r = range(nos)
		l = len(self.store)
		if nos == 0: r = range(l)
		elif nos < 0: r = range(l+nos,l)
		for id,item in zip(r,self.get(r)):
			if f(item): print(f'{id:<2}',item)
		print()
		return
	
	def viewSales(self):
		print('='*30 + '\n' + 'Sales Record'.center(30))
		my_f = '{:<4}{:^10}{:>15}'
		print(my_f.format('S/N','Date','Sales/day ($)'))
		x = 1
		my_f = '{:<4}{:^10}{:>15,.2f}'
		for d, g in self.sales.items():
			print(my_f.format(x,d,g))
			x += 1
		print('Total Gain: ${:,.2f}\n{}'.format(sum(self.sales.values()),'='*30))
		
	def save(self):
		stocks = '\n'.join(map(Item.save,self.store))
		with open(self.stock_file,'w') as f:
			f.write(stocks)
		with open(self.sales_file,'w') as f:
			for k,v in self.sales.items():
				f.write(k + ',' + str(v) + '\n')

	def setItemPrices(self):
		arg = self.getChoice('Price')
		if (arg == None) or (not len(arg)):
			return
		for i,j in arg.items():
			self.store[i].setPrice(j)
		self.save()
		print('prices set successfully!\n')
		
	def addItem(self):
		print('\nenter the following values:')
		name = input('Item name: ')
		quan = int(input('initial quantity: '))
		price = float(input('unit price: '))
		temp = Item(name,quan,price)
		if not temp in self.store:
			self.store.append(temp)
			print('item added successfully')
			self.save()
		else:
			print('item already exist')
		if input('\nDo you want to add another item? (y/n) :').lower()[0] == 'y':
			self.addItem()
		
	def updateQuantities(self):
		arg = self.getChoice()
		if (arg == None) or (not len(arg)):
			return
		for i,j in arg.items():
			self.store[i].updateQuantity(j)
		print('Quantities updated successfully\n')
		self.save()
	
	def get(self,ids):
		return map(self.store.__getitem__,ids)
		
	def buy(self):
		amnts = []
		vats = []
		bonus = True
		arg = self.getChoice()
		if not arg:
			return
		keys = tuple(arg)
		for id in keys:
			q = arg[id]
			temp = self.store[id]
			if temp.unitPrice < 100:
				bonus = False
			if temp.quan < q:
				print('There are only %d pieces of %s left..\n choose how to proceed' %(temp.quan,temp.name))
				x = choice(['Buy available','Skip Item'])
				if x == 1:
					q = arg[id] = temp.quan
				else:
					arg.pop(id)
					continue
			a = temp.buy(q)
			if q < 5: vats.append(0.2*a)
			elif q > 10: vats.append(0.3*a)
			else: vats.append(0.0)
			amnts.append(a)
		if len(arg) > 10 and bonus:
			bonus = 800.00		
		price = sum(amnts) + sum(vats)
		from datetime import date as dt
		d = dt.today().strftime('%d-%m-%y')
		if d in self.sales:
			self.sales[d] += price
		else:
			self.sales[d] = price
		receipt = 'MAL ADAMU IFE RETAIL MARKET'.center(60) + '\n' + 'Cash Receipt'.center(60) + '\n\n' + 'S/N'.center(2) + ' Items bought'.center(25) + 'Quan'.center(8) + 'U.Price'.center(10) + 'Amt'.center(7) + 'V.A.T'.center(8) + '\n'
		for i,itm,q,a,v in zip(range(len(arg)),self.get(arg.keys()),arg.values(),amnts,vats):	
			receipt += str(i+1).center(2) + '{:<25}'.format(itm.name) + f'{q:^8,d}' + '{:>10,.1f}'.format(itm.unitPrice) + f'{a:>7,.1f}' + f'{v:>8,.1f}\n'
		receipt += '\nTotal VAT: %.2f\tBonus: %.2f\nTotal amount: %.2f' %(sum(vats),bonus,price)
		if input('Transaction Successful..\nDo you want receipt? (y/n): ')[0].lower() == 'y':
			print('='*60)
			print(receipt)
			print('='*60)
		self.save()

	def getChoice(self,action = 'Quantity'):
		 print('\nSupply Item ID(s) and ' + action + '(s) to continue..')
		 f = int 
		 if action != 'Quantity':
		 	f = float
		 result = {}
		 def inner_getChoice():
		 	fin = 'y'
		 	while fin == 'y':
		 		try:
		 			id = int(input('Enter item ID: '))
		 			if id in result:
		 				c = input('you already selected this item\ndo you want to change its ' + action + '? (y/n): ')
		 				if c.lower() == 'y':
		 					data = f(input('Enter new ' + action + ': '))
		 				else: continue
		 			elif id not in range(len(self.store)):
		 				print('no item with such id!')
		 				continue
		 			else:
		 				data = f(input('Enter ' + action + ': '))
		 			result[id] = data
		 		except ValueError:
		 			print('wrong input')
		 		finally:
		 			fin = input('do you need another item?..(y/n): ').lower()
		 
		 def view_choices():
		 	if not len(result):
		 		print('You didnt select any Item')
		 		return	
		 	my_f = '{:<3}{:<25}{:^10}'
		 	print('\nyou selected the following items\n')
		 	print(my_f.format('ID','Item',action))
		 	for key in result:
		 		print(my_f.format(key,self.store[key].name,result[key]))

		 def exit_function():
		 	print('\n' + 'Options'.center(10))
		 	x = choice(['Proceed','Add Items','Remove an Item','Cancel'])
		 	if x == 2:
		 		print('\nadding items...')
		 		inner_getChoice()
		 		view_choices()
		 		return exit_function()
		 	elif x == 3:
		 		try:
		 			result.pop(int(input('\nEnter id of item to remove: ')))
		 			print('item removed..\n')
		 		except ValueError:
		 			print('wrong input!')
		 		except KeyError:
		 			print('No selected item with such id!')
		 		finally:
		 			view_choices()
		 			return exit_function()	
		 	elif x == 4:
		 		print('Transaction cancelled!\n')
		 		return False
		 	return True	
		 inner_getChoice()
		 view_choices()
		 if exit_function():
		 	return result
		 
def choice(menus):
	for i in range(len(menus)):
		print(i+1,menus[i],sep='. ')
	x = -1
	while not x in range(1,len(menus)+1):
		try: x = int(input('your choice?: '))
		except ValueError: continue
	return x

#to be used for admin access
#default access u:admin, p:admin
import Accounts as Accts
	
def main():
	print('choose access')
	x = choice(['Admin','User','Exit'])
	mySuper = SuperMarket('store.csv')
	my_admins = Accts.Accounts(('users.csv'))
	a_menu = ['Display Items','Set Item Price','Update quantities','Add new Item','View Sales Record','Change Password','Add Account','Return']
	u_menu = ['Display','Buy Items','Return']
	print()
	y = -1
	if x == 1:
		if my_admins.login():
			while y != len(a_menu):
				print('ADMIN MENU'.center(30))
				y = choice(a_menu)
				if y == 1:
					try: x = int(input('no of rows:'))
					except ValueError: x = 0
					finally: mySuper.display(x,True)
				elif y == 2:
					mySuper.setItemPrices()
				elif y == 3:
					mySuper.updateQuantities()
				elif y == 4:
					mySuper.addItem()
				elif y == 5:
					mySuper.viewSales()
				elif y == 6:
					my_admins.changePass()
				elif y == 7:
					my_admins.register()
				else:print()
		else: print('\nAccess Denied\n')
		main()
	elif x == 2:
		while y != len(u_menu):
			print('USER MENU'.center(30))
			y = choice(u_menu)
			if y == 1:
				mySuper.display()
			elif y == 2:
				mySuper.buy()
			else:
				print()
				main()
	elif x == 3 :
		print('Thank You')
		return
main()
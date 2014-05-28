import random

class TreasureFactory(object):
	def __init__(self, table, flags=[]):
		self.table = table
		self.flags = flags

	def get_table(self, table_name):
		table = self.table
		for x in table_name:
			table = table[x]
		return table
	
	def roll_once(self, table_name, roll_number = False):
		try:
			#Parse down to the selected table
			table = self.table
			for x in table_name:
				table = table[x]

			#Roll on the table. If there isn't an entry for what you rolled,
			#keep adding 1 until you reach something there's an entry for or
			#or you run out of entries
			if roll_number:
				initial_roll = roll = roll_number
			else:
				initial_roll = roll = random.randint(1,sorted(table.keys())[-1])
			while roll<=sorted(table.keys())[-1]:
				try:
					return [initial_roll,table[roll],table]
				except KeyError:
					roll+=1
			return roll
		except TypeError:
			#If the treasure table is built correctly, this should only be
			#triggered if you were rolling on a table with sub-tables based
			#on set flags. This tries all of the flag combinations recursively
			#It's O(n!), so use the flags sparingly.
			for x in self.flags:
				if x not in table_name:
					attempted_roll = self.roll_once(table_name+[x])
					if attempted_roll:
						return attempted_roll
		except KeyError:
			pass
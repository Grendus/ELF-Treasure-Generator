import random
import re

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

	#parses a string such as "Bonus 25" or "2d12+3" into a randomly generated integer
	def get_number(self, number):
		try:
			return int(number)
		except ValueError:
			roll_type = self.roll_once([number])

			#If rolling on the table returns a number, return it.
			try:
				return roll_type[1]
			except ValueError:
				pass

			#if the value to parse is a table in the current schema, get the roll type value out of the response, otherwise the value to parse was the roll type value
			if roll_type:
				roll_type = roll_type[1]
			else:
				roll_type = number

			#Fun with regular expressions. This splits a string such as "1d12-2" into '1','12','-','2'
			parsed_roll = re.compile(r'(\d+)d(\d+)([+-/*//])*(\d*)').match(roll_type)

			return_value = 0
			try:
				for x in range(int(parsed_roll.group(1))):
					return_value += random.randint(1,int(parsed_roll.group(2)))
			except AttributeError:
				print(number, roll_type)

			try:
				if parsed_roll.group(3) == '+':
					return_value += int(parsed_roll.group(4))
				elif parsed_roll.group(3) == '-':
					return_value -= int(parsed_roll.group(4))
				elif parsed_roll.group(3) == '*':
					return_value *= int(parsed_roll.group(4))
				elif parsed_roll.group(3) == '/':
					return_value /= int(parsed_roll.group(4))
			except TypeError:
				pass

			return return_value
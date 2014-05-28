import random

class TreasureModel(object):
	def __init__(self, factory,start):
		self.factory = factory
		self.current_roll = ['',start,'']

	def get_current_roll(self):
		return self.current_roll

	def roll(self, item_number=[], roll_number=False):
		roll_data = self.current_roll

		for x in item_number:
			roll_data = roll_data[x+3]

		#Since we're redoing the rolls from here on out, remove all rolls dependent on this one
		#for x in range(3,len(roll_data)):
		#	del roll_data[x]

		number_of_treasures = 1

		#if the treasure is not a tuple, this will throw a TypeError.
		#if the first value of the treasure table is not an int, this will throw a ValueError
		#easier to ask forgiveness
		try:
			number_of_treasures = int(roll_data[1][0][0])
		except (ValueError, TypeError):
			if not isinstance(roll_data[1], basestring):
				dice_string = self.factory.roll_once([roll_data[1][0][0]])
				if not dice_string:
					dice_string = roll_data[1][0][1]
				num_dice, type_dice = dice_string[1].split("d")
				try:
					type_dice, bonus = type_dice.split("+")
				except ValueError:
					bonus = 0
				number_of_treasures = 0
				for x in range(int(num_dice)):
					number_of_treasures += random.randint(1,int(type_dice))+int(bonus)

		for x in range(number_of_treasures):
			if isinstance(roll_data[1], basestring):
				next_roll = self.factory.roll_once([roll_data[1]],roll_number)
			else:
				next_roll = self.factory.roll_once(roll_data[1][0][1],roll_number)
			if next_roll:
				roll_data.append(next_roll)
		return next_roll

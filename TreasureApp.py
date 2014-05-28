from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from TreasureFactory import TreasureFactory
from TreasureModel import TreasureModel
import random
import re
import ELF


class TreasureDisplay(Widget):
	treasure_table_display = ObjectProperty(None)
	treasure_name = ObjectProperty(None)
	tab_display = ObjectProperty(None)

	#todo: change to __init__
	def initialize(self, factory, table_name):
		self.factory = factory
		self.table_name = table_name
		roll = self.factory.roll_once([self.table_name])
		self.fill_display(roll)

	def fill_display(self, treasure_roll):
		self.treasure_roll = treasure_roll
		treasure_table = treasure_roll[2]

		self.treasure_name.text = self.table_name
		#Record the name of the treasure rolled
		try:
			self.treasure_table_display.add_widget(Label(text=treasure_roll[1], markup=True, font_size='20sp', height=40, size_hint=(1,None)))
		except ValueError:
			self.treasure_table_display.add_widget(Label(text=treasure_roll[1][0][1][0], markup=True, font_size='20sp', height=40, size_hint=(1,None)))

		#Display the table that was rolled on
		for x in range(1,sorted(treasure_table.keys())[-1]+1):
			treasure_text = None
			temp_x = x
			while not treasure_text:
				try:
					try:
						treasure_text = "%s: %s" % (str(x), treasure_table[temp_x][0][1][0])
					except IndexError:
						treasure_text = "%s: %s" % (str(x), treasure_table[temp_x])
				except KeyError:
					temp_x = temp_x+1
			if x == treasure_roll[0]:
				self.treasure_table_display.add_widget(Label(text="%s%s%s"%("[b]",treasure_text,"[/b]"), markup=True, height=20, size_hint=(1,None)))
			else:
				self.treasure_table_display.add_widget(Label(text=treasure_text, height=20, size_hint=(1,None)))

		#Attach the next page
		if not isinstance(treasure_roll[1], basestring):
			for x in treasure_roll[1]:
				for y in range(self.get_number(x[0])):
					self.tab_display.add_widget(Button(text=x[1][0].replace(' ','\n')))
		else:
			self.tab_display.add_widget(Button(text=treasure_roll[1].replace(' ','\n'), size_hint=(0,1)))

	def get_number(self, number):
		try:
			return int(number)
		except ValueError:
			roll_type = self.factory.roll_once([number])
			if roll_type:
				roll_type = roll_type[1]
			else:
				roll_type = number

			#Fun with regular expressions. This splits a string such as "1d12-2" into '1','12','-','2'
			parsed_roll = re.compile(r'(\d+)d(\d+)([+-/*//])*(\d*)').match(roll_type)

			return_value = 0
			print parsed_roll.groups(), parsed_roll.group(1)
			for x in range(int(parsed_roll.group(1))):
				return_value += random.randint(1,int(parsed_roll.group(2)))

			try:
				if parsed_roll.group(3) == '+':
					return_value += int(parsed_roll.group(4))
				if parsed_roll.group(3) == '-':
					return_value -= int(parsed_roll.group(4))
				if parsed_roll.group(3) == '*':
					return_value *= int(parsed_roll.group(4))
				if parsed_roll.group(3) == '/':
					return_value /= int(parsed_roll.group(4))
			except TypeError:
				pass

			return return_value

class TreasureApp(App):
	def build(self):
		self.treasure_factory = TreasureFactory(ELF.start, ["Affluent","Simple"])
		self.treasure_display = TreasureDisplay()
		self.treasure_display.initialize(self.treasure_factory, "Treasure")
		return self.treasure_display

if __name__ == "__main__":
	TreasureApp().run()
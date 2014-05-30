from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from TreasureFactory import TreasureFactory
from TreasureModel import TreasureModel
import ELF


class TreasureDisplay(Widget):
	treasure_table_display = ObjectProperty(None)
	treasure_name = ObjectProperty(None)
	tab_display = ObjectProperty(None)

	#todo: change to __init__
	#Initialize the class with the factory and table name information
	def initialize(self, factory, table_name):
		self.factory = factory
		self.table_name = table_name
		roll = self.factory.roll_once([self.table_name])
		if roll:
			self.fill_display(roll)
		else:
			self.treasure_name.text = self.table_name

	#Fill out the display with information about the roll
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

		#Define the callback function. Every time a button is clicked, remove all slides after the current one and append the slide corresponding to the button pressed.
		def callback(instance):
			current_slide = TreasureApp.carousel.current_slide
			past_current_slide = False
			removable = []
			for slide in TreasureApp.carousel.slides:
				print "iteration"
				if past_current_slide:
					removable.append(slide)
				elif slide == current_slide:
					past_current_slide = True
			for slide in removable:
				TreasureApp.carousel.remove_widget(slide)
			TreasureApp.carousel.add_widget(instance.linked_page)

		#Attach the next page. The next page is stored in the button itself. In order to give the appearance of multi-tree traversal, each button keeps track of the branch it's supposed to traverse
		#and appends it to the end when touched
		if not isinstance(treasure_roll[1], basestring):
			for x in treasure_roll[1]:
				for y in range(self.factory.get_number(x[0])):
					button = Button(text=x[1][0].replace(' ','\n'), size_hint=(0,1))
					button.bind(on_press=callback)
					button.linked_page = TreasureDisplay()
					button.linked_page.initialize(self.factory, x[1][0])
					self.tab_display.add_widget(button)
		else:
			button = Button(text=treasure_roll[1].replace(' ','\n'), size_hint=(0,1))
			button.bind(on_press=callback)
			button.linked_page = TreasureDisplay()
			button.linked_page.initialize(self.factory, treasure_roll[1])
			self.tab_display.add_widget(button)

class TreasureApp(App):
	carousel = Carousel()

	def build(self):
		self.treasure_factory = TreasureFactory(ELF.start, ["Affluent","Simple"])
		self.treasure_display = TreasureDisplay()
		self.treasure_display.initialize(self.treasure_factory, "Treasure")
		TreasureApp.carousel.add_widget(self.treasure_display)
		return TreasureApp.carousel

if __name__ == "__main__":
	TreasureApp().run()
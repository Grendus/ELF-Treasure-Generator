from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from TreasureFactory import TreasureFactory
from TreasureModel import TreasureModel
import ELF

class TreasureDisplay(Widget):
	treasure_table_display = ObjectProperty(None)
	treasure_name = ObjectProperty(None)
	def fill_display(self, treasure_roll):
		self.treasure_roll = treasure_roll
		treasure_table = treasure_roll[2]
		try:
			self.treasure_name.text = treasure_roll[1]
		except ValueError:
			print treasure_roll[1]
			self.treasure_name.text = treasure_roll[1][0][1][0]

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
class TreasureApp(App):
	def build(self):
		self.treasure_factory = TreasureFactory(ELF.start, ["Affluent","Advanced"])
		self.treasure_model = TreasureModel(self.treasure_factory, "Greater Artifact")
		self.treasure_model.roll()
		self.treasure_display = TreasureDisplay()
		self.treasure_display.fill_display(self.treasure_model.get_current_roll()[3]) 
		return self.treasure_display

if __name__ == "__main__":
	TreasureApp().run()
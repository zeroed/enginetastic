import random, sys
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import tkFont

class App:

	def __init__(self, master):
		frame = Frame(master)
		frame["height"] = 100
		frame["width"] = 100
		frame.pack()
		self.button = Button(frame, text = "QUIT", command = frame.quit)
		self.button.pack(side = LEFT)    
		self.generate_players_button = Button(frame, text = "Generate players", command = self.run_generator)
		self.generate_players_button.pack(side = LEFT)
		global listbox
		label_font = tkFont.Font(family = "Monospace", size = 10)
		self.listbox = Listbox(frame, font = label_font, width = 60)
		self.listbox.pack(side = BOTTOM)
		#entry = Entry(frame, font = label_font, width = 3)
		#entry.pack(side = BOTTOM)

	def set_variables(self):
		global races 
		races = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
		'I', 'J', 'K', 'L', 'M', 'N', 'O']
		global races_number 
		races_number = len(races)
		global colors 
		colors = ['Black', 'Blue', 'Yellow', 'Red', 
		'Purple', 'Green']
	
	def print_menu(self):
		print '::Twilight Imperium player generator::'
		print '..........'
	
	def generate_players(self):
		#print 'How many players?'
		# players_number_string = raw_input()
		players_number_string = tkSimpleDialog.askstring('title', 'How many players?')
		players_number = int (players_number_string)
		if players_number not in range(2, 7):
			print 'Wrong Number of Players'
			tkMessageBox.showwarning(
			"generate_players",
			"Wrong Number of Players: \n(%s)" %players_number_string)
			sys.exit(1)
		players = []
		for number in range(1, players_number+1):
			players.append("Player" + str(number))
		for player in players:
			picked_race = random.choice(races)
			races.remove(picked_race)
			picked_color = random.choice(colors)
			colors.remove(picked_color)
			output_text = '- ' + player + ': ' + \
				picked_race + ' - ' + picked_color
			self.listbox.insert(END, output_text)

	def run_generator(self, ):
			self.print_menu()
			self.set_variables()
			self.generate_players()

def main():
	root = Tk()
	app = App(root)
	root.title('Twilight Imperium player generator')
	root.mainloop()
	exit(0)

main()

#if __name__ == '__main__':
#	exit(0)

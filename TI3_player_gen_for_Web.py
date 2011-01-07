import random, sys

def set_variables():
	global races 
	races = [
	'Universities of Jol Nar',
	'The Naalu Collective',
	'The L1z1x Mindnet',
	'The Mentak Coalition',
	'The Barony of Letnev',
	'The Xxcha Kingdom',
	'The Yassaril Tribes',
	'The Emirates of Hacan',
	'The Sardakk N\'orr',
	'The Federation of Sol',
	'Embers of Muaat',
	'The Clan of Saar',
	'The Winnu',
	'The Yin Brotherhood',
	]
	global races_number 
	races_number = len(races)
	global colors 
	colors = ['Black', 'Blue', 'Yellow', 'Red', 
	'Purple', 'Green']

def print_menu(self):
	print '::Twilight Imperium player generator::'
	print '..........'

def generate_players_parameterized(players_number):
	if not players_number.isdigit():
		return 'Wrong Number of Players'
		sys.exit(1)
	players_number = int(players_number)
	if players_number not in range(2, 7):
		return 'Wrong Number of Players'
		sys.exit(1)
	players = []
	result_text = ''
	for number in range(1, players_number+1):
		players.append("Player" + str(number))
	for player in players:
		picked_race = random.choice(races)
		races.remove(picked_race)
		picked_color = random.choice(colors)
		colors.remove(picked_color)
		output_text = '- [' + player + ': ' + \
			picked_race + ' - ' + picked_color + ']'
		result_text = result_text + output_text + '\n'
	return result_text

def run_generator():
		print_menu()
		set_variables()
		generate_players()

def engine(players_number):
	set_variables()
	return generate_players_parameterized(players_number)

if __name__ == '__main__':
	exit(0)

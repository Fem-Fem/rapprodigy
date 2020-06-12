import random

class MarkovRap:

	def __init__(self, text, k_int):
		self.text = text
		self.k_int = k_int
		self.dictionary = ''


	def kgram(self):
		library = {}
		text_tester = self.text
		for i in range(self.k_int):
			text_tester = text_tester + self.text[i]
		for i in range(len(self.text)):
			k = i + self.k_int
			if library.get(text_tester[i:k]) == None:
				library[text_tester[i:k]] = {text_tester[k]: 1}
			else:
				if library[text_tester[i:k]].get(text_tester[k]):
					library[text_tester[i:k]][text_tester[k]] = library[text_tester[i:k]][text_tester[k]] + 1
				else:
					library[text_tester[i:k]][text_tester[k]] = 1
		self.dictionary = library


	def next_letter(self, text):
		for z in range(500):
			population = []
			weights = []
			for i in self.dictionary[text[-self.k_int:]]:
				population.append(i)
				weights.append(self.dictionary[text[-self.k_int:]][i])
			new_letter = random.choices(population, weights)
			text = text + new_letter[0]
		print(text)


	def print_info(self):
		print(self.text)
		print(self.k_int)
		print(self.dictionary)
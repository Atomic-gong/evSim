from sty import fg, bg, ef, rs, Style, RgbFg
from tqdm import tqdm
import random
import sys

logGeneration = False
showPelletBar = False
showCreatureBar = True
printAtInterval = True
interval = 1000
mutationChance = 1/1000
startingPellets = 300
startingCreatures = 400
pelletsPerIteration = 100

currentArg = sys.argv[1]
if currentArg == "t":
	logGeneration = True
elif currentArg == "f":
	logGeneration = False

currentArg = sys.argv[2]
if currentArg == "t":
	showPelletBar = True
elif currentArg == "f":
	showPelletBar = False

currentArg = sys.argv[3]
if currentArg == "t":
	showCreatureBar = True
elif currentArg == "f":
	showCreatureBar = False

currentArg = sys.argv[4]
if currentArg == "t":
	printAtInterval = True
elif currentArg == "f":
	printAtInterval = False

interval = int(sys.argv[5])
mutationChance = int(sys.argv[6])
startingPellets = int(sys.argv[7])
startingCreatures = int(sys.argv[8])
pelletsPerIteration = int(sys.argv[9])

iterations = 0

pellets = []
creatures = []

size = (100,100)

if logGeneration:
	logFile = open("Latest.log", "w")

def debug(contents):
	global logFile
	logFile.write(contents + "\n")

class pellet():
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def check(self, checklist):
		global pellets
		if (self.x,self.y) in checklist:
			pellets.remove(self)

	def __hash__(self):
		return hash((self.value, self.suit))

	def __eq__(self, other):
    # Protect against comparisons of other classes.
		if not isinstance(other, __class__):
			return NotImplemented
		return self.x == other.x and self.y == other.y

class creature():
	def __init__(self, x, y, DNA):
		self.energy = 30
		self.x = x
		self.y = y
		self.DNA = DNA #mutationchance is first 4 digits (chance/1000), colour is next 9 digits (3 per value), orders are all the characters after that e.g 0001160227157UDLR
		self.colour = (int(self.DNA[5:7]),int(self.DNA[8:10]),int(self.DNA[11:13]))
	def update(self):
		global pellets, creatures
		if (pellet(self.x,self.y) in pellets):
			#pellets.remove(next((x for x in pellets if x.x == self.x and x.y == self.y), None))
			return (self.x, self.y)
			self.energy += 10
		if self.energy < 1:
			creatures.remove(self)


def genPellets(num, bar, log):
	if bar:
		print("Generating pellets.")
		for i in tqdm(range(num)):
			if log:
				debug(f"Generated pellet #{i}")
			pellets.append(pellet(random.randint(0,size[0]), random.randint(0,size[1])))
	else:
		for i in range(num):
			if log:
				debug(f"Generated pellet #{i}")
			pellets.append(pellet(random.randint(0,size[0]), random.randint(0,size[1])))

def genCreatures(num, bar, log):
	if bar:
		print("Generating creatures.")
		for i in tqdm(range(num)):
			mutation = f"{mutationChance:4d}"
			colour = f"{random.randint(0,255):3d}{random.randint(0,255):3d}{random.randint(0,255):3d}"
			orders = "UDLR"
			DNA = f"{mutation}{colour}{orders}"
			if log:
				debug(f"Generated creature #{i}: {DNA}")
			creatures.append(creature(random.randint(0,size[0]), random.randint(0,size[1]), DNA))
	else:
		for i in range(num):
			mutation = f"{mutationChance:4d}"
			colour = f"{random.randint(0,255):3d}{random.randint(0,255):3d}{random.randint(0,255):3d}"
			orders = "UDLR"
			DNA = f"{mutation}{colour}{orders}"
			if log:
				debug(f"Generated creature #{i}: {DNA}")
			creatures.append(creature(random.randint(0,size[0]), random.randint(0,size[1]), DNA))

def render():
	renderList = []
	for i in range(size[1]+1):
		renderList.append([])
		for n in range(size[0]+1):
			renderList[i].append(" ")
	for i in pellets:
		#fg.pellet = Style(RgbFg(100,255,100))
		renderList[i.y][i.x] = fg.green+bg.black+"."+fg.rs+bg.rs
	for i in creatures:
		fg.creatureColour = Style(RgbFg(i.colour[0], i.colour[1], i.colour[2]))
		renderList[i.y][i.x] = fg.creatureColour+bg.black+"#"+fg.rs+bg.rs
	for i in renderList:
		buffer = ""
		for n in i:
			buffer = buffer + n
		print(buffer)

def iterate():
	global iterations, creatures, pelletsPerIteration, interval
	debug(f"Iteration[ {iterations} ]: {len(creatures)} creatures.")
	genPellets(pelletsPerIteration, False, False)
	iterations += 1
	posList = []
	for i in creatures:
		pos = i.update()
		if pos != False:
			posList.append(pos)
	for i in pellets:
		i.check(posList)
	if int(iterations/interval) == iterations/interval:
		render()

genPellets(startingPellets, showPelletBar, logGeneration)
genCreatures(startingCreatures, showCreatureBar, logGeneration)

while True:
	iterate()
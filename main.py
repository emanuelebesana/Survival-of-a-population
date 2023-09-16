import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import argparse
import random
import sys
import math

#python3 main.py 60 0.3 120 150 10 15 10 0   <- good parameters

#RULE OF THE PROGRAM -> UP,RIGHT,DOWN,LEFT

def get_around_point(point,length):
    """This function returns the 4 points (above,right,below,left) near a chosen point in a grid square of a 
      set size.
      For example if I pass it point=[3,4] and length=10,it returns [[3,5],[4,4],[3,3],[2,4]].  
      This is for when I want to understand the configuration around an individual. I made it so that it 
      has periodic boundary conditions.
    """ 
    return [[point[0],(point[1]+1)%length],[(point[0]+1)%length,point[1]],[point[0],(point[1]-1)%length],[(point[0]-1)%length,point[1]]]



class Environment:
    """Class for the environment, which is simply a square grid within which the positions of food and 
    poison are stored.
    Both food and poison are an array of 2-dimensional points.
    """

    def __init__(self,grid=None,cibo=None,veleno=None,numero_cibo=None,numero_veleno=None,dimensioni=None):

        if grid == None:
            self.grid = [[i,j] for i in range(dimensioni) for j in range(dimensioni)]
        else:
            self.grid = grid

        self.numero_cibo = numero_cibo

        self.numero_veleno = numero_veleno

        if cibo == None:
            self.cibo = random.sample(self.grid,self.numero_cibo)
        else:
            self.cibo = cibo

        if veleno == None:     #devo stare attento a non mettere cibo e veleno nella stessa posizione
            venom = []
            for j in range(numero_veleno):
                a = random.choice(self.grid)
                while (a in venom or a in self.cibo):
                    a = random.choice(self.grid)
                venom.append(a)
            self.veleno=venom
        else:
            self.veleno = veleno

        self.dimensioni = dimensioni

    def posizioni_cibo(self):
        return self.cibo
    def posizioni_veleno(self):
        return self.veleno
    def get_grid(self):
        return self.grid

    def get_cibo(self,point):
        """Checks whether there is food in a grid point or not.If found, returns True, vice versa False 
        """
        if point in self.cibo:
            return True
        else:
            return False
    def get_veleno(self,point):
        if point in self.veleno:
            return True
        else:
            return False

    def get_length_of_grid(self):
        return self.dimensioni

    def get_configuration(self,point):
       
        """Returns the configuration around a given point on the grid.
        The "configuration" is an array of 4 numbers, and has a 1 where there is food, 0 where there is nothing and -1 where
                there is poison.
                The numbers in the array are ordered such that they follow the order of the programme: up,right,down,left
        """
         
        config_around_point = [0,0,0,0]
        for l,j in enumerate(get_around_point(point,self.dimensioni)):
            if self.get_cibo(j) == True:
                config_around_point[l] = 1
            if self.get_veleno(j) == True:
                config_around_point[l] = -1
        return config_around_point

    def update_cibo_veleno (self,pos_individuo):
        """this list "pos_individual" is what will later be the ind.get_position.Here I check whether 
        there is food or poison in the individual's position. 
        If there is, I have to remove food or poison respectively.
        """ 
        if pos_individuo in self.cibo:
            self.cibo.remove(pos_individuo)
        if pos_individuo in self.veleno:
            self.veleno.remove(pos_individuo)

def new_cibo_veleno(self):
        """I create new food and poison.      
        It serves because at the end of each generation I generate new individuals and new food
        """ 
        self.cibo = random.sample(self.grid,self.numero_cibo)
        new_venom = []
        for j in range(self.numero_veleno):
            a = random.choice(self.grid)
            while (a in self.cibo or a in new_venom):
                a = random.choice(self.grid)
            new_venom.append(a)
        self.veleno=new_venom




mosse = ["u","r","d","l"]
class Individual:
    """Class Individual.  
    The individual is a list of 'moves' as long as the list of all possible configurations that the 
    individual may encounter.       Each configuration corresponds to one move, simply because the indices of the lists self.configurations and self.moves coincide. In this way, it was not necessary to make
       a dictionary.
    """ 

    def __init__(self,moves=None, energy=None, position=None,dimensioni=None):
        self.configurazioni = [[i,j,k,l] for i in(0,1,-1) for j in(0,1,-1) for k in (0,1,-1) for l in(0,1,-1)]
        self.dimensioni = dimensioni
        if moves == None:
            self.moves = [random.choice(mosse) for j in range(len(self.configurazioni))]
        else:
            self.moves = moves
        if energy == None:
            self.energy = 10
        else:
            self.energy = energy
        if position == None:
            self.position = [random.randint(0,self.dimensioni-1),random.randint(0,self.dimensioni-1)]
        else:
            self.position = position


def get_position(self):
    return self.position

def move_individual(self,config):
    """I move an individual.
    First I understand the configuration around it, then depending on its genome corresponding to that configuration I move it. "config" then will be environment.g et_configuration(individual.get_position())
    """ 
    possibili_posizioni = get_around_point(self.position,self.dimensioni)
    if self.moves[self.configurazioni.index(config)] == "u":
        self.position = possibili_posizioni[0]
    if self.moves[self.configurazioni.index(config)] == "r":
        self.position = possibili_posizioni[1]
    if self.moves[self.configurazioni.index(config)] == "d":
        self.position = possibili_posizioni[2]
    if self.moves[self.configurazioni.index(config)] == "l":
        self.position = possibili_posizioni[3]

    def get_energy(self):
        return self.energy
    def get_moves(self):
        return self.moves
    def add_energy(self):
        self.energy += 0
    def subtract_energy(self,a):
        self.energy -= a


    def mate(self,other):
        return Individual(moves=twopoint_crossover(self.get_moves(),other.get_moves()),energy = math.ceil((self.get_energy()+other.get_energy())/2),dimensioni=self.dimensioni)
    def mutate(self,prob):
        if random.random() < prob:
            pos = random.randint(0,len(self.moves)-1)
            self.moves[pos] = random.choice(mosse)

    def get_fitness(self):
        return self.energy


def generate_population(npop,initial_energy,dimensioni):
    population = []
    for m in range(npop):
        population.append(Individual(energy=initial_energy,dimensioni=dimensioni))
    return population


def twopoint_crossover(lista1,lista2):
    """Two-point crossover
    """
    lunghListe = len(lista1)

    randomNum1 = random.randint(0,lunghListe-1)
    randomNum2 = random.randint(0,lunghListe-1)

    a = min(randomNum1,randomNum2)
    b = max(randomNum1,randomNum2)


    figlio1 = lista1[:a]+lista2[a:b]+lista1[b:]
    figlio2 = lista2[:a]+lista1[a:b]+lista2[b:]


    return random.choice([figlio1,figlio2])


def roulette(pop):
    """Roulette sampling
    """
    max = sum(i.get_fitness() for i in pop)
    randomNum = random.uniform(0,max)
    current = 0
    for s in pop:
        current += s.get_fitness()
        if current > randomNum:
            return s

def create_new_population(pop,npop,ngen):
    """I create a new population from the previous one (which is passed as an argument).  
    The number of individuals remains fixed, and each one reproduces in proportion to its fitness
    """ 
    new_population = []
    pop = [ind for ind in pop if ind.get_fitness()>0 ]
    for j in range(npop):
        parent1,parent2 = roulette(pop),roulette(pop)
        while(parent2 == parent1):
            parent2 = roulette(pop)
        child = parent1.mate(parent2)
        new_population.append(child)
    for i in range(0,int(npop/3)):  # muto 1/3 degli individui
        new_population[i].mutate(mut_prob)
    return new_population


def move_all(individui,ambiente):
    """This function moves all individuals one step, adds or removes energy depending on whether an individual has found food or not, and then removes the food/poison if there is a
       individual.  
    """ 
    for ind in individui:
        ind.move_individual(ambiente.get_configuration(ind.get_position()))
        if ind.get_position() in ambiente.posizioni_cibo():
            ind.add_energy()
        elif ind.get_position() in ambiente.posizioni_veleno():
            ind.subtract_energy(2)
        else:
            ind.subtract_energy(1)
        ambiente.update_cibo_veleno(ind.get_position())
        if ind.get_energy()==0:
            individui.remove(ind)


def check_best_individual(individuo):
    
    """To see if an individual is learning, I can see what moves he makes for a certain configuration. For example I go to see where he moves if I pass him the configuration [1,0,0]: in this case his genome must be "u". If I pass him [1,1,0,0] either 'u' or 'r' is OK. Some configurations are irrelevant, such as [0,0,0] and [1,1,1]. I also discard configurations with three 1s and with three -1s. I use configurations with one 1 or two 1s (in which case the individual must move towards the 1s), and configurations with three -1s or two -1s (in which case he must
    avoid the -1s).
        The perfect individual has total==66
    """ 

    totale = 0
    mosse_individ = individuo.get_moves()
    configurations = [[i,j,k,l] for i in(0,1,-1) for j in(0,1,-1) for k in (0,1,-1) for l in(0,1,-1)]
    for config in configurations:
        if config.count(1)==1:
            if mosse_individ[configurations.index(config)] == mosse[config.index(1)]:
                totale+=1
        if config.count(1)==2:
            indices = [i for i,x in enumerate(config) if x==1]
            if mosse_individ[configurations.index(config)] == mosse[indices[0]] or mosse_individ[configurations.index(config)] == mosse[indices[1]]:
                totale += 1
        if config.count(-1)==3 and config.count(1)==0:
            if mosse_individ[configurations.index(config)] == mosse[config.index(0)]:
                totale += 1
        if config.count(-1)==2 and config.count(1)==0:
            indicess = [i for i,x in enumerate(config) if x==0]
            if mosse_individ[configurations.index(config)] == mosse[indicess[0]] or mosse_individ[configurations.index(config)] == mosse[indicess[1]]:
                totale += 1
    return totale



def make_drawing(pop,env,paths):

    ax.set_title("Individuals, food and venom")
    ax.set_xticks([i for i in range(dimensioni_grid)])
    ax.set_yticks([i for i in range(dimensioni_grid)])

    ax.grid(True)


    x = [ind.get_position()[0] for ind in pop]
    y = [ind.get_position()[1] for ind in pop]
    energies = [ind.get_energy() for ind in pop]

    cibox = [food[0] for food in env.posizioni_cibo()]
    ciboy = [food[1] for food in env.posizioni_cibo()]


    velenox = [venom[0] for venom in env.posizioni_veleno()]
    velenoy = [venom[1] for venom in env.posizioni_veleno()]


    ax.scatter(x,y, marker = 'o', c='blue',label="Individuals")  #individuals
    ax.scatter(cibox,ciboy,marker='s',c='red',label="Food") #food
    ax.scatter(velenox,velenoy,marker='>',c='green',label="Venom") #venom

    for x0,y0 in zip(x,y):
        ab = AnnotationBbox(getImage(paths[0],zoom=0.14), (x0,y0),frameon=False)
        ax.add_artist(ab)

    for x0,y0 in zip(velenox,velenoy):
        ab = AnnotationBbox(getImage(paths[2],zoom=0.04), (x0,y0),frameon=False)
        ax.add_artist(ab)

    for x0,y0 in zip(cibox,ciboy):
        ab = AnnotationBbox(getImage(paths[1],zoom=0.1), (x0,y0),frameon=False)
        ax.add_artist(ab)



if __name__ == '__main__':


    parser  = argparse.ArgumentParser(description ="A food-seeking-venom-avoiding  program")

    parser.add_argument('popsize', help="Population size", type=int)
    parser.add_argument('mut_prob', help="Mutation probability", type=float)
    parser.add_argument('ngen', help="Number of generations", type=int)
    parser.add_argument('ncibo',help="Number of food",type=int)
    parser.add_argument('nveleno',help="Numero of venom",type=int)
    parser.add_argument('dim',help="Grid dimensions",type=int)
    parser.add_argument('energy',help="Initial energy",type=int)
    parser.add_argument('plots',help="0 -> no plots. +1 -> plots",type=int)
    args = parser.parse_args()



    print(args)

    npop = args.popsize
    mut_prob = args.mut_prob
    ngen = args.ngen
    numero_cibo = args.ncibo
    numero_veleno = args.nveleno
    dimensioni_grid = args.dim
    initial_energy = args.energy
    plots = args.plots
    numero_passi_totale = 5    


    def getImage(path,zoom):
        return OffsetImage(plt.imread(path),zoom=zoom)

    paths = ['mario.png','mario_mush.png','mario_banana.png']


    fig,ax = plt.subplots(figsize=(10,10))


    ambiente = Environment(numero_cibo=numero_cibo,numero_veleno=numero_veleno,dimensioni = dimensioni_grid)
    population = generate_population(npop,initial_energy,dimensioni=dimensioni_grid)

    for j in range(ngen):
        if j==1:
            check = totale
        starting_fitnesses = [ind.get_fitness() for ind in population]
        print("starting fitnesses at generation ",j," ->", starting_fitnesses)
        if plots==1:
            make_drawing(population,ambiente,paths)
            ax.cla()
        for m in range(numero_passi_totale):
            move_all(population,ambiente)
            if plots==1:
                make_drawing(population,ambiente,paths)
                plt.pause(0.02)
                ax.cla()

        fitnesses = [ind.get_fitness() for ind in population]
        if all(v<=0 for v in fitnesses) == True:
            print("All individuals are dead. Generation: ", j)
            sys.exit()

        pop_check = [ind for ind in population if ind.get_fitness()>0 ]
        if len(pop_check) == 1:
            print("There remains only one individual. Generation: ", j)
            sys.exit()

        population.sort(key = lambda i : i.get_fitness(),reverse=True)
        totale = check_best_individual(population[0])
        ambiente.new_cibo_veleno()
        population = create_new_population(population,npop,ngen)

    print("The best individual finally spotted", totale, " out of 66, whereas at the beginning he spotted: ",check )
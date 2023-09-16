import unittest
import main as prog
import random

class test_get_around_point(unittest.TestCase):

    def setUp(self):
        print('before')

    def tearDown(self):
        print('after')

    def test_get_around(self):
        #check the corners. In this case already length=10
        altodx,altosx,bassodx,bassosx = [9,9],[0,9],[9,0],[0,0]
        self.assertEqual([[9,0],[0,9],[9,8],[8,9]], prog.get_around_point(altodx,10) )
        self.assertEqual([[0,0],[1,9],[0,8],[9,9]], prog.get_around_point(altosx,10) )
        self.assertEqual([[9,1],[0,0],[9,9],[8,0]], prog.get_around_point(bassodx,10) )
        self.assertEqual([[0,1],[1,0],[0,9],[9,0]], prog.get_around_point(bassosx,10) )
        #check a random point. In this case also length=10 
        randomPoint = [3,4]
        self.assertEqual([[3,5],[4,4],[3,3],[2,4]], prog.get_around_point(randomPoint,10) )



class check_Environment_class(unittest.TestCase):

    def setUp(self):
        print('before')

    def tearDown(self):
        print('after')
    
    def test_all_environment(self):
        dimensioni=10
        numero_cibo = 8 
        numero_veleno=5
        ambiente = prog.Environment(numero_cibo=numero_cibo,numero_veleno=numero_veleno,dimensioni=dimensioni)
        self.assertEqual(len(ambiente.get_grid()),dimensioni**2)
        self.assertEqual(len(ambiente.posizioni_cibo()),numero_cibo)
        #controllo che il cibo, il veleno e i punti del grid siano all'interno del range specificato da "dimensioni"
        for pnt in ambiente.get_grid():
            self.assertLessEqual(pnt[0],9)
            self.assertLessEqual(pnt[1],9)
        for food in ambiente.posizioni_cibo():
            self.assertLessEqual(food[0],9)
            self.assertLessEqual(food[1],9)
        for venom in ambiente.posizioni_veleno():
            self.assertLessEqual(venom[0],9)
            self.assertLessEqual(venom[1],9)
        

        #controllo che nelle posizioni specificate manualmente ci sia il cibo. Idem per il veleno
        cibo = [[1,1],[2,2]]
        ambiente2 = prog.Environment(cibo=cibo,numero_cibo=2,numero_veleno=0,dimensioni=dimensioni)
        self.assertTrue(ambiente2.get_cibo([1,1]))
        self.assertTrue(ambiente2.get_cibo([2,2]))
       
        veleno = [[1,1],[2,2]]
        ambientee2 = prog.Environment(veleno=veleno,numero_veleno=2,numero_cibo=0,dimensioni=dimensioni)
        self.assertTrue(ambientee2.get_veleno([1,1]))
        self.assertTrue(ambientee2.get_veleno([2,2]))
       
       
        #controllo che la configurazione attorno a un punto sia corretta
        vera_configurazione = [1,0,0,0]
        config_ambiente = ambiente2.get_configuration([1,0])
        self.assertEqual(vera_configurazione,config_ambiente)

        vera_configurazione2 = [1,0,0,1]
        config_ambiente2 = ambiente2.get_configuration([2,1])
        self.assertEqual(vera_configurazione2,config_ambiente2)

        #controllo che cambiando il cibo, tutto sia corretto
        ambiente2.update_cibo_veleno([2,2])
        self.assertEqual(len(ambiente2.posizioni_cibo()),1)


class check_Individual_class(unittest.TestCase):

    def setUp(self):
        print('before')

    def tearDown(self):
        print('after')
    
    def test_all_individual(self):
        ambiente3 = prog.Environment(numero_cibo=2,numero_veleno=0,dimensioni=10)
        individuo1 = prog.Individual(dimensioni=10)

        #controllo che l'individuo venga generato nel grid e non fuori
        posizione_individuo = individuo1.get_position()
        self.assertLessEqual(posizione_individuo[0],9)
        self.assertLessEqual(posizione_individuo[1],9)
       
        #controllo che l'individuo si muova in modo corretto
        mosse = ["u","r","d","l"]
        configs_da_dare = [[i,j,k,l] for i in(0,1,-1) for j in(0,1,-1) for k in (0,1,-1) for l in(0,1,-1)]
        mosse_preprogrammate = [random.choice(mosse) for j in range(len(configs_da_dare))]

        mosse_preprogrammate[0] = "u"
        mosse_preprogrammate[1] = "r"
        mosse_preprogrammate[2] = "d"
        mosse_preprogrammate[3] = "l"
        individuo2 = prog.Individual(moves=mosse_preprogrammate,position = [3,3],dimensioni=10)
        individuo2.move_individual(configs_da_dare[0]) #con la prima l'individuo si deve muovere in alto. Si muove in questo modo: [3,3]->[3,4]
        self.assertEqual(individuo2.get_position(),[3,4])
        individuo2.move_individual(configs_da_dare[1]) # idem destra. Si muove [3,4]->[4,4] 
        self.assertEqual(individuo2.get_position(),[4,4])
        individuo2.move_individual(configs_da_dare[2]) #idem basso. si muove [4,4] -> [4,3]
        self.assertEqual(individuo2.get_position(),[4,3])
        individuo2.move_individual(configs_da_dare[3]) #idem sx. si muove [4,3] -> [3,3]
        self.assertEqual(individuo2.get_position(),[3,3])

        #controllo che due individui si accoppino per dare un figlio con la fitness corretta 
        individuo2 = prog.Individual(dimensioni=10,energy=15)
        individuo3 = prog.Individual(dimensioni=10,energy=25)
        individuo_mateato = individuo2.mate(individuo3)
        self.assertEqual(individuo_mateato.get_energy(),20)



class check_move_all(unittest.TestCase):

    def setUp(self):
        print('before')

    def tearDown(self):
        print('after')
    
    
    def test_move_all(self):
        """I make an environment where there are two individuals. I make them move so that one pecks at the food and the other doesn't. At the end I check that one individual has increased energy, the other decreased
           and that the food in the environment is an empty list
        """ 
        dimensioni=10
        cibo_at = [[2,2]]
        mosse = ["u","r","d","l"]
        conff = [[i,j,k,l] for i in(0,1,-1) for j in(0,1,-1) for k in (0,1,-1) for l in(0,1,-1)]  
        moves1 = [random.choice(mosse) for j in range(len(conff))]
        moves1[1] = "l" #faccio in modo che all'inizio l'indivudo1 abbia intorno a se [0,0,0,1] cioè che si muova a sinistra,e li ci sia il cibo

        moves2 = [random.choice(mosse) for j in range(len(conff))] #mosse a caso. basta che l'individuo2 non becchi il cibo in una mossa


        posizione1 = [3,2] #ind1 ha il cibo a sinistra
        posizione2 = [8,8]#ind2 più lontano possibile dal cibo
        
            
        ambiente4 = prog.Environment(cibo=cibo_at,numero_cibo=1,numero_veleno=0,dimensioni=10)

        ind1 = prog.Individual(moves=moves1,energy=10,dimensioni=10,position=posizione1)
        ind2 = prog.Individual(moves=moves2,energy=10,dimensioni=10,position=posizione2)

        population = [ind1,ind2]
        prog.move_all(population,ambiente4)

        self.assertEqual(ind1.get_energy(),10)
        self.assertEqual(ind2.get_energy(),9)
        self.assertEqual(len(ambiente4.posizioni_cibo()),0)
        
        
        

unittest.main() 


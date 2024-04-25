
import random

  	   		     		  		  		    	 		 		   		 		  
import random as rand  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  




class QLearner(object):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    This is a Q learner object.  		  	   		     		  		  		    	 		 		   		 		  
		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        num_states=100,  		  	   		     		  		  		    	 		 		   		 		  
        num_actions=4,  		  	   		     		  		  		    	 		 		   		 		  
        alpha=0.2,  		  	   		     		  		  		    	 		 		   		 		  
        gamma=0.9,  		  	   		     		  		  		    	 		 		   		 		  
        rar=0.5,  		  	   		     		  		  		    	 		 		   		 		  
        radr=0.99,  		  	   		     		  		  		    	 		 		   		 		  
        dyna=0,  		  	   		     		  		  		    	 		 		   		 		  
        verbose=False,  		  	   		     		  		  		    	 		 		   		 		  
    ):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.num_actions = num_actions  		  	   		     		  		  		    	 		 		   		 		  
        self.s = 0  		  	   		     		  		  		    	 		 		   		 		  
        self.a = 0
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        self.qtable = np.zeros((num_states,num_actions))
        self.exp = []

    def author(self):
        return 'asrinivasan90'  # replace tb34 with your Georgia Tech username

    def querysetstate(self, s):

        """  		  	   		     		  		  		    	 		 		   		 		  
        Update the state without updating the Q-table  		  	   		     		  		  		    	 		 		   		 		  
		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.s = s

        if random.uniform(0.0,1.0) < self.rar:
            action = random.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.qtable[int(s)])

        self.a = action
        if self.verbose:  		  	   		     		  		  		    	 		 		   		 		  
            print(f"s = {s}, a = {action}")

        return action  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    def query(self, s_prime, r):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Update the Q table and return an action  		  	   		     		  		  		    	 		 		   		 		  
		  	   		     		  		  		    	 		 		   		 		  
        """
        print("qtable")
        print(self.s)
        print(self.a)
        print(self.qtable[999,0])
        q_value = self.qtable[int(self.s),int(self.a)]
        q_value_updated = (1-self.alpha) * q_value + self.alpha * (r + self.gamma * self.qtable[s_prime, np.argmax(self.qtable[s_prime])])
        self.qtable[int(self.s),int(self.a)] = q_value_updated
        self.exp.append([self.s,self.a,s_prime,r])
        action = self.querysetstate(s_prime)

        if self.dyna != 0:
            for i in range(0,self.dyna):
                rand_exp = np.random.choice(len(self.exp))
                s, a, sp, r = self.exp[rand_exp]
                self.qtable[s, a] = (1.0 - self.alpha) * self.qtable[s, a] + self.alpha * (r + self.gamma * self.qtable[sp, np.argmax(self.qtable[sp])])

        self.rar = self.rar * self.radr

        if self.verbose:  		  	   		     		  		  		    	 		 		   		 		  
            print(f"s = {s_prime}, a = {action}, r={r}")

        return action  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")  		  	   		     		  		  		    	 		 		   		 		  

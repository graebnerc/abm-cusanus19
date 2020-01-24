import numpy as np


class Agent:
    """Chooses a technology, depending on own preferences and nb of users.
    
    Attributes
    ----------
    neighborhood : set
        The set of agents in the neighborhood of the agent.
        Those are the agents relevant for the technology choice of this agent.
        
    tech_chose : int
        The technology chose by the agent. `None` in the beginning, then 0 or 1
    
    Methods
    --------
    
    add_neighbors
        Creates the neighborhood structure for the model; 
        Called only once by `__init__`.
        
    tec_choice
        Chooses a technology based on own preferences and nb of neighbors
        using the technologies.
        
    get_tech
        Returns the chosen technology.
    """
    
    def __init__(self):
        self.neighborhood = set()       
        self.tech_chosen = None
        
    def add_neighbors(self, set_of_new_neighbors):
        """Adds new agents to the neighborhood of the agents.
        """
        try:
            assert isinstance(set_of_new_neighbors, set), "Requires \
            set-like input, not {}".format(type(set_of_new_neighbors))
        except AssertionError:
            set_of_new_neighbors = set(set_of_new_neighbors)
            
        self.neighborhood |= set_of_new_neighbors # Adds the new neighbors
        
    def tec_choice(self):
        """Technology choice method; 
        selects and assigns a technology with probabilities 
        proportional to the current usage shares in the agent's neighborhood.
        
        First determines the share of technology 1 chosen by neighbors.
        Second, it determines the personal perference of the agent for tech 0 
        according to a uniform distribution.
        Third, if the personal preference for tech zero is larger than the 
        share of agents using tech 1, tech 0 is chosen. Otherwise tech 1 is 
        chosen.
        """
        # get share of technology 1 in the neighborhood
        techs_neighborhood = [a.get_tech() for a in self.neighborhood if \
                              a.get_tech() is not None]
        try:
            share_t1 = sum(techs_neighborhood) / len(techs_neighborhood)
        except ZeroDivisionError:
            share_t1 = None

        # Get the personal preference of the agent
        pref_tech_0 = np.random.uniform(0, 1)
        # make technology choice 
        if len(techs_neighborhood) > 0:        
            if pref_tech_0 < share_t1:
                self.tech_chosen = 1
            else:
                self.tech_chosen = 0
        else:
            if pref_tech_0 < 0.5:
                self.tech_chosen = 1
            else:
                self.tech_chosen = 0
                
    def get_tech(self):
        return self.tech_chosen

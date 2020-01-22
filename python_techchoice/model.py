import agent as agent
import numpy as np


class Model:
    """The blueprint for a single model instance.

    Attributes
    ----------
    identifier : int
        A unique identifier for this model instance.
        
    agentlist : list
        A list of the agent instances associated with the model
        
    time : int
        Current time in the model
        
    subscripts_t0 : list
        Current subscritpions for technology 0
        
    subscripts_t1
        Current subscriptions for technology 1
    
    neighborhood : str
        The neigborhood structure of the agents. Specifies who they 
        take into consideration when choosing their technology.
        
    
    Methods
    --------
    
    create_neighborhood
        Creates the neighborhood structure for the model; 
        Called only once by `__init__`.
    
    run
        Runs the model, i.e. all agents choose their technologiy sequentially.
        
    return_results
        Returns the results as a `dict`
            
    """
     
    def __init__(self, n_agents, neighborhood_str, identifier):
        """The __init__ method.

        Creates a list of agents and sets up the neighborhood structure.

        Parameters
        ----------
        n_agents : int
            Number of agents.

        neighborhood_str str
            The neighborhood structure of the agents.
            Currently, two types are supportet: 
            'full' creates a complete neighborhood in which every agent is 
            connected to every other agent.
            'ring' creates a ring, i.e. every agent has four neighbors.
  
      identifier: int
            An identifier that uniquely identifies the model instance.
            Will be reported in the results.
        """
        self.identifier = identifier
        self.agentlist = [agent.Agent() for i in range(n_agents)]
        self.time = 0
        self.subscripts_t0 = [0]
        self.subscripts_t1 = [0]
        
        assert neighborhood_str in ["ring", "full"], "No correct neighborhood \
        structure specified. Currently allowed: 'full' or 'ring', but not {}"\
        .format(neighborhood_str)
        self.neighborhood = neighborhood_str
        
        self.create_neighborhood_structure()

    def create_neighborhood_structure(self):
        """Takes the agents in the beginning and sets up neighborhood.
        
        Parameters
        -----------
        None
            
        Returns
        --------
        Nothing, only modifies the Model and the Agent instances.
        
        Raises
        -------
        
        AssertionError
            Whenever wrong neighborhood structure is provided.
       
        """
        if self.neighborhood == "ring":
            print("Creating ring neighborhood...", end="")
            for i in range(len(self.agentlist)):
                if i == 0: # for the first agent add the two last agents
                    self.agentlist[i].add_neighbors({self.agentlist[-1], 
                                  self.agentlist[-2]})
                    self.agentlist[-1].add_neighbors({self.agentlist[i]})
                    self.agentlist[-2].add_neighbors({self.agentlist[i]})
                elif i == 1: # for the second agent add first and ultimate ag
                    self.agentlist[i].add_neighbors({self.agentlist[i-1], 
                                  self.agentlist[-1]})
                    self.agentlist[i-1].add_neighbors({self.agentlist[i]})
                    self.agentlist[-1].add_neighbors({self.agentlist[i]})
                else:
                    self.agentlist[i].add_neighbors({self.agentlist[i-1],
                                  self.agentlist[i-2]})
                    self.agentlist[i-1].add_neighbors({self.agentlist[i]})
                    self.agentlist[i-2].add_neighbors({self.agentlist[i]})
            print("complete!")
                
        elif self.neighborhood == "full":
            print("Creating full neighborhood...", end="")
            for a in self.agentlist:
                a.add_neighbors(set(self.agentlist))
            print("complete!")
            
        else:
            raise SyntaxError("Should not be here, self.neighborhood wrong.")
            
    def run(self):
        """Runs the model.
        Shuffles the list of agents, then one agent after the other
        chooses her technology.
        """
        print("Start running the model!")
        np.random.shuffle(self.agentlist)
        for a in self.agentlist:
            self.time += 1
            # print(self.time, end=" ")
            a.tec_choice()
            if a.get_tech() == 0:
                self.subscripts_t0.append(self.subscripts_t0[-1]+1)
                self.subscripts_t1.append(self.subscripts_t1[-1])
            elif a.get_tech() == 1:
                self.subscripts_t1.append(self.subscripts_t1[-1]+1)
                self.subscripts_t0.append(self.subscripts_t0[-1])
            else:
                raise SyntaxError("Something is wrong, agent does not return \
                                  tech!")
                
    def return_results(self):
        """Returns the results of the model as a dictionary.
        """
        result_dict = {}
        result_dict["id"] = [self.identifier] * len(self.subscripts_t0)
        result_dict["time"] = np.arange(0, len(self.subscripts_t0), 1)
        result_dict["neighborhood"] = [self.neighborhood] * len(self.subscripts_t0)
        
        result_dict["share_t0"] = [0.0] + [self.subscripts_t0[i] \
                    / (self.subscripts_t0[i] + self.subscripts_t1[i]) for \
                    i in range(1, len(self.subscripts_t0))]
        
        result_dict["share_t1"] = [0.0] + [self.subscripts_t1[i] \
                    / (self.subscripts_t0[i] + self.subscripts_t1[i]) for \
                    i in range(1, len(self.subscripts_t1))]
        return(result_dict)

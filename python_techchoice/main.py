import model
import pandas as pd
import visualization

class Main:
    """The main class for our investigation.
    
    Creates and runs the specified number of model runs, then saves the 
    results in a feather file.
    
    Attributes
    ----------
    outcome_filename : str
        The direction and file name for the result.
        If the file does not end with '.feather' it will be added.
        
    nb_agents : int
        The number of agents used in the simulation runs
        
    neighborhood_dict : dict
        Specifies the number of runs for each neighborhood specification.
        
    nb_simulations : int
        Total nb of simulation runs 
        Equals neighborhood_dict["full"] + neighborhood_dict["ring"]
        
    results : list
        A list into which the results of the models will be stored.
    
    current_id : int
        The current id used for the next model instance.
        Every model instance gets a unique id for identification purposes.
        
    results_frame : pd.DataFrame
        A data frame created from the result dicts from the model instances
        
    Methods
    --------
    
    save_data
        Saves the results frame to the outcome_filename
    
    """
    def __init__(self, nb_agents, neighborhood_dict, outcome_filename):
        assert isinstance(outcome_filename, str), "Outcome filename must be \
        string, not {}".format(outcome_filename)
        
        self.outcome_filename = outcome_filename
        self.nb_agents = nb_agents
        self.neighborhood_dict = neighborhood_dict
        self.nb_simulations = (self.neighborhood_dict["full"] + 
                               self.neighborhood_dict["ring"])
        self.results = []
        self.current_id = 1
        for i in range(self.neighborhood_dict["full"]):
            current_model = model.Model(self.nb_agents, "full", self.current_id)
            current_model.run()
            self.results.append(pd.DataFrame(current_model.return_results()))
            self.current_id += 1
        for i in range(self.neighborhood_dict["ring"]):
            current_model = model.Model(self.nb_agents, "ring", self.current_id)
            current_model.run()
            self.results.append(pd.DataFrame(current_model.return_results()))
            self.current_id += 1
        self.results_frame = pd.concat(self.results)
        self.save_data()
          
    def save_data(self):
        print("Start saving data...", end="")
        if self.outcome_filename[-8:] != ".feather":
            self.outcome_filename += ".feather"
        self.results_frame.reset_index(drop=True).to_feather(self.outcome_filename)
        print("complete!")
        print("Outcome saved in: {}".format(self.outcome_filename))

nb_agents = 100

neigh_dict = {"full": 20, # Nb of simulation runs with complete neigborhood
              "ring": 20} # Nb of simulation runs with ring neigborhood

full_sim = Main(50, neigh_dict, "output/tech_choice_example_output")

data = 'output/tech_choice_example_output.feather'
file = "output/tech_choice_aggregated_results.pdf"
file_2 = "output/tech_choice_disaggregated_results.pdf"

visualization.make_agg_plot(data, file)
visualization.make_disagg_plot(data, file_2)

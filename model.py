from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import Adult,Child
from schedule import RandomActivationByBreed


class SickleSim(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 100
    width = 100

    initial_sickle_adult = 100
    initial_carrier_adult = 100
    initial_normal_adult = 100

    fertility_rate = 2
    life_expectancy = 70
    child_malaria_infection = 0.01
    child_malaria_death = 0.1
    adult_malaria_infection = 0.001
    adult_malaria_death = 0.05


    verbose = False  # Print-monitoring

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=100,
        width=100,
        initial_sickle_adult=100,
        initial_carrier_adult=100,
        initial_normal_adult=100,
        fertility_rate=2,
        life_expectancy=70,
        child_malaria_infection=0.01,
        child_malaria_death=0.1,
        adult_malaria_infection=0.001,
        adult_malaria_death=0.05,
        verbose = False
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.
        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sickle_adult = initial_sickle_adult
        self.initial_carrier_adult = initial_carrier_adult
        self.initial_normal_adult = initial_normal_adult,
        self.fertility_rate = fertility_rate,
        self.life_expectancy = life_expectancy,
        self.child_malaria_infection = child_malaria_infection,
        self.child_malaria_death = child_malaria_death,
        self.adult_malaria_infection = adult_malaria_infection,
        self.adult_malaria_death = adult_malaria_death,
        self.verbose = verbose

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        #Create normal adults
        for i in range(self.initial_normal_adult):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.0
            adult = Adult(self.next_id(), (x, y), self, True, genotype)
            self.grid.place_agent(adult, (x, y))
            self.schedule.add(adult)
        #Create hetero adults:
        for i in range(self.initial_normal_adult):

        #Create sickle cell adults:


        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_breed_count(Wolf),
                    self.schedule.get_breed_count(Sheep),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number wolves: ", self.schedule.get_breed_count(Wolf))
            print("Initial number sheep: ", self.schedule.get_breed_count(Sheep))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_breed_count(Wolf))
            print("Final number sheep: ", self.schedule.get_breed_count(Sheep))
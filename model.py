from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import AdultSickle, AdultNormal, AdultCarrier, ChildNormal, ChildCarrier, ChildSickle
from schedule import RandomActivationByBreed


class SickleSim(Model):

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
        "A model for simulating the competing selective forces between sickle cell anemia and malaria."
    )

    def __init__(
        self,
        height=100,
        width=100,
        initial_normal_adult=100,
        initial_sickle_adult=100,
        initial_carrier_adult=100,
        fertility_rate=2,
        life_expectancy=70,
        carrying_capacity = 3000,
        child_malaria_infection=0.01,
        child_malaria_death=0.1,
        adult_malaria_infection=0.001,
        adult_malaria_death=0.05,
        verbose=False
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
        self.initial_normal_adult = initial_normal_adult
        self.fertility_rate = fertility_rate
        self.life_expectancy = life_expectancy
        self.child_malaria_infection = child_malaria_infection
        self.child_malaria_death = child_malaria_death
        self.adult_malaria_infection = adult_malaria_infection
        self.adult_malaria_death = adult_malaria_death
        self.verbose = verbose
        self.carrying_capacity = carrying_capacity

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.data_collector = DataCollector(
            {
                "Sickle Cell Adults": lambda m: m.schedule.get_breed_count(AdultSickle),
                "Carrier Adults": lambda m: m.schedule.get_breed_count(AdultCarrier),
                "Normal Adults": lambda m: m.schedule.get_breed_count(AdultNormal),
                "Sickle Cell Children": lambda m: m.schedule.get_breed_count(ChildSickle),
                "Carrier Children": lambda m: m.schedule.get_breed_count(ChildCarrier),
                "Normal Children": lambda m: m.schedule.get_breed_count(ChildNormal),
            }
        )

        # Create normal adults
        for i in range(self.initial_normal_adult):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.0
            adult = AdultSickle(self.next_id(), (x, y), self, True, genotype)
            self.grid.place_agent(adult, (x, y))
            self.schedule.add(adult)
        # Create carrier adults:
        for i in range(self.initial_carrier_adult):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.5
            adult = AdultSickle(self.next_id(), (x, y), self, True, genotype)
            self.grid.place_agent(adult, (x, y))
            self.schedule.add(adult)

        # Create sickle cell adults:
        for i in range(self.initial_carrier_adult):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.5
            adult = AdultSickle(self.next_id(), (x, y), self, True, genotype)
            self.grid.place_agent(adult, (x, y))
            self.schedule.add(adult)

    def step(self):
        self.schedule.step()

        x1 = self.schedule.get_breed_count(ChildNormal)
        x2 = self.schedule.get_breed_count(ChildCarrier)
        x3 = self.schedule.get_breed_count(ChildSickle)
        y1 = self.schedule.get_breed_count(AdultNormal)
        y2 = self.schedule.get_breed_count(AdultCarrier)
        y3 = self.schedule.get_breed_count(AdultSickle)
        population = x1+x2+x3+y1+y2+y3

        dx1 = ((x1 ** 2)+(1/2)*x1*x2+(1/4)*(x2 ** 2))/((x1+x2+x3) ** 2)*(0.04*(1-(population/3000)))-0.015*x1
        dx2 = ((1/2)*x1*x2+(1/2)*(x2 ** 2))/((x1+x2+x3) ** 2)*(0.04*(1-(population/3000)))-(0.0013+0.02)*x2
        dx3 = ((1/4)*(x2 ** 2))/((x1+x2+x3) ** 2)*(0.04*(1-(population/3000)))-(0.0013+0.5)*x2
        dy1 = -(0.008+0.0006)*y1
        dy2 = -(0.008+0.00005+0.02)*y2
        dy3 = -(0.008+0.00005+0.5)*y3

        for i in range(abs(round(dx1))):

        for i in range(abs(round(dx2))):

        for i in range(abs(round(dx3))):

        for i in range(abs(round(dy1))):

        for i in range(abs(round(dy2))):

        for i in range(abs(round(dy3))):

        # collect data
        self.data_collector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    x1, x2, x3,
                    y1, y2, y3
                ]
            )

    def run_model(self, step_count=200):

        for i in range(step_count):
            self.step()

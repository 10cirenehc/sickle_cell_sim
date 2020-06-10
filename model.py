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
        growth_rate = (0.04*(1-(population/self.carrying_capacity)))
        if growth_rate < 0:
            growth_rate = 0

        if self.schedule.get_agent_count() > 3000:
            difference = self.schedule.get_agent_count()-3000
            y1_del = round((y1/(y1+y2))*difference)
            y2_del = round((y2/(y1+y2))*difference)
            for i in range(y1_del):
                candidate = self.random.choice(self, self.schedule.agents_by_breed[AdultNormal])
                self.grid.remove_agent(candidate)
                self.schedule.remove(candidate)
            for i in range(y2_del):
                candidate = self.random.choice(self,self.schedule.agents_by_breed[AdultCarrier])
                self.grid.remove_agent(candidate)
                self.schedule.remove(candidate)
            population = 3000
            y1 -= y1_del
            y2 -= y2_del

        dx1 = (((y1 ** 2)+(1/2)*y1*y2+(1/4)*(y2 ** 2))/((y1+y2+y3) ** 2)*growth_rate*population
               - (0.015 * x1))
        dx2 = (((1/2)*y1*y2+(1/2)*(y2 ** 2))/((y1+y2+y3) ** 2)*growth_rate*population
               - (0.0013+0.02)*x2)
        dx3 = ((1/4)*(y2 ** 2))/((y1+y2+y3) ** 2)*growth_rate*population-(0.0013+0.5)*x3
        dy1 = -(0.008+0.0006)*y1
        dy2 = -(0.008+0.00005+0.02)*y2
        dy3 = -(0.008+0.00005+0.5)*y3

        if dx1 < 0:
            delete = self.random.choices(self, self.schedule.agents_by_breed[ChildNormal], k=abs(round(dx1)))
            for a in delete:
                self.grid.remove_agent(agent=a)
                self.schedule.remove(agent=a)
        else:
            for i in range(round(dx1)):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                child = ChildNormal(self.next_id(),(x,y),self, True, genotype=0.0)
                self.grid.place_agent(child, (x, y))
                self.schedule.add(child)

        if dx2 < 0:
            delete = self.random.choices(self, self.schedule.agents_by_breed[ChildCarrier], k=abs(round(dx2)))
            for a in delete:
                self.grid.remove_agent(agent=a)
                self.schedule.remove(agent=a)
        else:
            for i in range(round(dx2)):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                child = ChildCarrier(self.next_id(), (x, y), self, True, genotype=0.5)
                self.grid.place_agent(child, (x, y))
                self.schedule.add(child)

        if dx3 < 0:
            delete = self.random.choices(self, self.schedule.agents_by_breed[ChildSickle], k=abs(round(dx3)))
            for a in delete:
                self.grid.remove_agent(agent=a)
                self.schedule.remove(agent=a)
        else:
            for i in range(round(dx3)):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                child = ChildSickle(self.next_id(), (x, y), self, True, genotype=1.0)
                self.grid.place_agent(child, (x, y))
                self.schedule.add(child)

        for i in range(abs(round(dy1))):
            delete = self.random.choice(self, self.schedule.agents_by_breed[AdultNormal])
            self.grid.remove_agent(delete)
            self.schedule.remove(delete)

        for i in range(abs(round(dy2))):
            delete = self.random.choice(self, self.schedule.agents_by_breed[AdultCarrier])
            self.grid.remove_agent(delete)
            self.schedule.remove(delete)

        for i in range(abs(round(dy3))):
            delete = self.random.choice(self, self.schedule.agents_by_breed[AdultSickle])
            self.grid.remove_agent(delete)
            self.schedule.remove(delete)



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

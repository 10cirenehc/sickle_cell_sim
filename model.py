from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import AdultSickle, AdultNormal, AdultCarrier, ChildNormal, ChildCarrier, ChildSickle
from schedule import RandomActivationByBreed


class SickleSim(Model):

    height = 70
    width = 70

    initial_sickle_adult = 100
    initial_carrier_adult = 100
    initial_normal_adult = 100

    fertility_rate = 2
    life_expectancy = 65
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
        height=70,
        width=70,
        initial_normal_adult=100,
        initial_sickle_adult=100,
        initial_carrier_adult=100,
        life_expectancy=65,
        carrying_capacity = 3000,
        verbose=False,
        malaria_prevalence=0.5,
        sickle_cell_deadliness=0.5,
        heterozygous_advantage=0.5,
    ):
        """
        Create a new Sickle Cell model with the given parameters.
        Args:
            initial_normal_adult: Number of normal adults to start with
            initial_carrier_adult: Number of carrier adults to start with
            initial_sickle_adult: Number of afflicted adults to start with
            malaria_prevalence: Coefficient of malaria prevalence
            sickle_cell_deadliness: Deadliness of sickle cell
            heterozygous_advantage: The amount of selective advantage heterozygotes have
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sickle_adult = initial_sickle_adult
        self.initial_carrier_adult = initial_carrier_adult
        self.initial_normal_adult = initial_normal_adult
        self.life_expectancy = life_expectancy
        self.verbose = verbose
        self.carrying_capacity = carrying_capacity
        self.malaria_prevalence = 2*malaria_prevalence
        self.sickle_cell_deadliness = 2*sickle_cell_deadliness
        self.heterozygous_advantage = 2-2*heterozygous_advantage

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Sickle Cell Adults": lambda m: m.schedule.get_breed_count(AdultSickle),
                "Carrier Adults": lambda m: m.schedule.get_breed_count(AdultCarrier),
                "Normal Adults": lambda m: m.schedule.get_breed_count(AdultNormal),
                "Sickle Cell Children": lambda m: m.schedule.get_breed_count(ChildSickle),
                "Carrier Children": lambda m: m.schedule.get_breed_count(ChildCarrier),
                "Normal Children": lambda m: m.schedule.get_breed_count(ChildNormal),
            }
        )

        self.adult_population = initial_normal_adult+initial_carrier_adult+initial_sickle_adult
        ages = []
        for i in range(self.adult_population):
            age = 0
            while age < 5 or age > 75:
                age = self.random.gauss(0, 30)
            ages.append(round(age))

        self.initial_normal_child = round(0.1*initial_normal_adult)
        self.initial_carrier_child = round(0.1*initial_carrier_adult)
        self.initial_sickle_child = round(0.1*initial_carrier_adult)

        # Create normal adults
        for i in range(self.initial_normal_adult):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.0
            adult = AdultNormal(self.next_id(), (x, y), self, True, genotype, ages.pop())
            self.grid.place_agent(adult, (x, y))
            self.schedule.add(adult)
        # Create carrier adults:
        for i in range(self.initial_carrier_adult):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.5
            adult = AdultCarrier(self.next_id(), (x, y), self, True, genotype, ages.pop())
            self.grid.place_agent(adult, (x, y))
            self.schedule.add(adult)

        # Create carrier adults:
        for i in range(self.initial_sickle_adult):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 1.0
            adult = AdultSickle(self.next_id(), (x, y), self, True, genotype, ages.pop())
            self.grid.place_agent(adult, (x, y))
            self.schedule.add(adult)

        # Create normal adults:
        for i in range(self.initial_normal_child):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.0
            child = ChildNormal(self.next_id(), (x, y), self, True, genotype, self.random.randint(0, 4))
            self.grid.place_agent(child, (x, y))
            self.schedule.add(child)

        # Create carrier children:
        for i in range(self.initial_carrier_child):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 0.5
            child = ChildCarrier(self.next_id(), (x, y), self, True, genotype, self.random.randint(0, 4))
            self.grid.place_agent(child, (x, y))
            self.schedule.add(child)

        # Create sickle children:
        for i in range(self.initial_sickle_child):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            genotype = 1.0
            child = ChildSickle(self.next_id(), (x, y), self, True, genotype, self.random.randint(0, 4))
            self.grid.place_agent(child, (x, y))
            self.schedule.add(child)

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
            self.delete_from_breed(AdultNormal, y1_del)
            self.delete_from_breed(AdultCarrier, y2_del)
            population = 3000
            y1 -= y1_del
            y2 -= y2_del

        dx1 = (((y1 ** 2)+(1/2)*y1*y2+(1/4)*(y2 ** 2))/((y1+y2+y3) ** 2)*growth_rate*population
               - (0.015 * self.malaria_prevalence * x1))
        dx2 = (((1/2)*y1*y2+(1/2)*(y2 ** 2))/((y1+y2+y3) ** 2)*growth_rate*population
               - ((0.0013*self.malaria_prevalence*self.heterozygous_advantage)+0.02*self.sickle_cell_deadliness)*x2)
        dx3 = ((1/4)*(y2 ** 2))/((y1+y2+y3) ** 2)*growth_rate*population-(0.0013*self.malaria_prevalence
            * self.heterozygous_advantage+0.5*self.sickle_cell_deadliness)*x3
        dy1 = -(0.008+0.0006*self.malaria_prevalence)*y1
        dy2 = -(0.008+0.00005*self.malaria_prevalence*self.heterozygous_advantage+0.02*self.sickle_cell_deadliness)*y2
        dy3 = -(0.008+0.00005*self.malaria_prevalence*self.heterozygous_advantage+0.5*self.sickle_cell_deadliness)*y3

        if dx1 < 0:
            self.delete_from_breed(ChildNormal, abs(round(dx1)))
        else:
            for i in range(round(dx1)):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                child = ChildNormal(self.next_id(),(x,y),self, True, genotype=0.0, age=0)
                self.grid.place_agent(child, (x, y))
                self.schedule.add(child)

        if dx2 < 0:
            self.delete_from_breed(ChildSickle, abs(round(dx2)))
        else:
            for i in range(round(dx2)):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                child = ChildCarrier(self.next_id(), (x, y), self, True, genotype=0.5, age=0)
                self.grid.place_agent(child, (x, y))
                self.schedule.add(child)

        if dx3 < 0:
            self.delete_from_breed(ChildSickle, abs(round(dx1)))
        else:
            for i in range(round(dx3)):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                child = ChildSickle(self.next_id(), (x, y), self, True, genotype=1.0, age=0)
                self.grid.place_agent(child, (x, y))
                self.schedule.add(child)

        self.delete_from_breed(AdultNormal, abs(round(dy1)))
        self.delete_from_breed(AdultCarrier, abs(round(dy2)))
        self.delete_from_breed(AdultSickle, abs(round(dy3)))

        # collect data
        self.datacollector.collect(self)
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

    def delete_from_breed(self, breed, count):
            agent_keys = []
            for i in range(count):
                if self.schedule.get_breed_count(breed) != 0:
                    agent_key = self.random.choice(list(self.schedule.agents_by_breed[breed].keys()))
                    if agent_key not in agent_keys:
                        agent = self.schedule.agents_by_breed[breed][agent_key]
                        self.grid.remove_agent(agent)
                        self.schedule.remove(agent)
                        agent_keys.append(agent_key)

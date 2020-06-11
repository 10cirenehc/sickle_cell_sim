from random_walk import RandomWalker


class Adult(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.
    The init is the same as the RandomWalker.
    """
    genotype = None
    age = None

    def __init__(self, unique_id, pos, model, moore, genotype = None, age = None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.genotype = genotype
        self.life_expectancy = 90
        self.age = age

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        living = True

        # Reduce energy
        self.age += 1

        # Death
        if self.age > self.life_expectancy:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False


class AdultSickle(Adult):

    genotype = None

    def __init__(self, unique_id, pos, model, moore, genotype, age = None):
        super().__init__(unique_id,pos, model, moore=moore, genotype=1.0, age = None)
        self.genotype = genotype
        self.age = age

    def step(self):
        super().step()


class AdultCarrier(Adult):

    def __init__(self, unique_id, pos, model, moore, genotype, age = None):
        super().__init__(unique_id, pos, model, moore=moore, genotype=0.5, age = None)
        self.genotype = genotype
        self.age = age

    def step(self):
        super().step()


class AdultNormal(Adult):

    def __init__(self, unique_id, pos, model, moore, genotype, age = None):
        super().__init__(unique_id, pos, model, moore=moore, genotype = 0, age = None)
        self.genotype = genotype
        self.age = age

    def step(self):
        super().step()


class Child(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    genotype = None
    age = None

    def __init__(self, unique_id, pos, model, moore, genotype=None, age=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.genotype = genotype
        self.maturation = 5
        self.age = age


class ChildSickle(Child):

    genotype = None
    age = None

    def __init__(self, unique_id, pos, model, moore, genotype=None, age=None):
        super().__init__(unique_id, pos, model, moore=moore, genotype=1.0, age=None)
        self.genotype = genotype
        self.maturation = 5
        self.age = age

    def step(self):
        self.random_move()
        self.age += 1

        if self.age >=5:
            teen = AdultSickle(
                self.model.next_id(), self.pos ,self.model, self.moore, self.genotype
            )
            self.model.grip.place_agent(teen, teen.pos)
            self.model.schedule.ad(teen)
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)


class ChildCarrier(Child):
    genotype = None
    age = None

    def __init__(self, unique_id, pos, model, moore, genotype=None, age=None):
        super().__init__(unique_id, pos, model, moore=moore, genotype=0.5, age=None)
        self.genotype = genotype
        self.maturation = 5
        self.age = age

    def step(self):
        self.random_move()
        self.age += 1

        if self.age >=5:
            teen = AdultCarrier(
                self.model.next_id(), self.pos ,self.model, self.moore, self.genotype
            )
            self.model.grip.place_agent(teen, teen.pos)
            self.model.schedule.ad(teen)
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)


class ChildNormal(Child):
    genotype = None
    age = None

    def __init__(self, unique_id, pos, model, moore, genotype=None, age=None):
        super().__init__(unique_id, pos, model, moore=moore, genotype=0.0, age=None)
        self.genotype = genotype
        self.maturation = 5
        self.age = age

    def step(self):
        self.random_move()
        self.age += 1

        if self.age >=5:
            teen = AdultNormal(
                self.model.next_id(), self.pos ,self.model, self.moore, self.genotype
            )
            self.model.grip.place_agent(teen, teen.pos)
            self.model.schedule.ad(teen)
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
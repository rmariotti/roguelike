from ecs.component import Component


class StatsComponent(Component):
    """
    Entity basic attributes.

    Each attribute describes the competence of a
    character in a broad range of skills.
    """
    def __init__(
            self, strength: int, agility: int, toughness: int,
            intelligence: int, willpower: int, charisma: int
    ):
        self.strength = strength
        """
        Represents a character's physical power (0–18). Higher strength allows
        the character to perform better in tasks requiring brute force.
        """

        self.agility = agility
        """
        Measures a character's speed, coordination, and dexterity (0–18).
        High agility improves movement precision, balance, and reaction time.
        """

        self.toughness = toughness
        """
        Indicates a character's physical resilience (0–18). 
        Higher toughness means better resistance to injury and fatigue.
        """

        self.intelligence = intelligence
        """
        Reflects a character's cognitive abilities, such as reasoning, memory, and 
        understanding complex concepts (0–18).
        """

        self.willpower = willpower
        """
        Represents mental fortitude, focus, and self-discipline (0–18). A high 
        willpower improves resistance to fear, pain, and mental manipulation.
        """

        self.charisma = charisma
        """
        Describes a character's social influence and presence (0–18). Higher 
        charisma improves persuasion, leadership and deception.
        """

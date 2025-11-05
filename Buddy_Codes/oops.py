# --- BUG ANALYSIS ---
# Use these comments to guide your debugging.

"""
Bug 1 (Abstraction): One of the abstract classes (Monster) is being instantiated directly, 
or rather, it's being instantiated without implementing all the abstract methods it inherited. 
Why does the program crash (or not crash) when goblin is created?

Hint: Python only flags this at the moment of instantiation.
"""

"""
Bug 2 (Abstraction/Instantiation): Another class (Trap) tries to instantiate, but its __init__ 
call is fundamentally flawed. Look at the arguments passed to super().__init__().

Hint: What arguments does Entity.__init__ expect? What is 'self' in this context?
"""

"""
Bug 3 (Inheritance/MRO): The Player class uses multiple inheritance (Player -> Combatant -> Entity). 
Look at how __init__ is called in both Player and Combatant. Is the Entity parent class 
ever being initialized correctly? This is a classic "Method Resolution Order" (MRO) problem. 
You might get an AttributeError in an unexpected place.

Hint: Combatant.__init__ *never* calls super().__init__(). This breaks the chain.
"""

"""
Bug 4 (Encapsulation): The Trap class, in its spring_trap method, tries to access 
a private variable (__max_hp) from another object (target). This will fail due 
to name mangling.

Hint: '__max_hp' is actually stored as '_Entity__max_hp'.
"""

"""
Bug 5 (Polymorphism/Logic): The Monster class should be able to take_damage, but it 
inherits from Combatant, which has a broken __init__. When hero.attack(goblin) is called, 
will goblin.take_damage() work as expected? It's inheriting take_damage from Entity, 
but Entity's __init__ (which sets up _current_hp) might not have been called.

Hint: This relates to Bug 3. Since Combatant.__init__ doesn't call its parent,
the Monster's '_current_hp' attribute is never created.
"""

"""
Bug 6 (Encapsulation): The Player's __repr__ method tries to print self.__max_hp. 
Will this work from within the Player class, or was that variable private 
to the Entity class?

Hint: Name mangling is class-specific. Player cannot access _Entity__max_hp 
using 'self.__max_hp'.
"""

from abc import ABC, abstractmethod
import random

class Entity(ABC):
    """
    Abstract base class from any entity in the game.
    Requires implementation of take_damage and a 'name' property.
    """
    def __init__(self, name, max_hp):
        self.name = name
        self.__max_hp = max_hp
        self._current_hp = max_hp
        print(f"(Debug: {self.name} initialized with {self.__max_hp} HP)")
    
    @property
    @abstractmethod
    def is_alive(self):
        """
        Property to check if entity is alive.
        """
        pass

    @abstractmethod
    def take_damage(self, amount):
        """
        Abstract method to take damage.
        """
        print(f"(Debug: {self.name} is taking damage)")
        self._current_hp -= amount
    
    def get_health_percentage(self):
        # Calculates health percentahe using the private __max_hp
        return  (self._current_hp / self.__max_hp) * 100

class Combatant(Entity):
    """
    Abstract base class for entities that can fight.
    Inherits from Entity and adds an abstract 'attack' method.
    """
    def __init__(self, name, max_hp, power):
        self.name = name
        self._max_hp = max_hp
        self.power = power
        # This class forgets to initialize its parent! (bug?)
    
    @abstractmethod
    def attack(self, target: Entity):
        """
        Deal damage to another entity.
        """
        pass

class Player(Combatant):
    """
    A concrete Player class.
    Inherits from Combatant.
    """
    def __init__(self, name, player_class, max_hp, power):
        self.player_class = player_class
        # Intentionally calling the grandparent's init, not the direct parent's
        Entity.__init__(self, name, max_hp)
        Combatant.__init__(self, name, max_hp, power)

    def is_alive(self):
        # Implementation of abstract property
        return self._current_hp > 0

    def take_damage(self, amount):
        # Overriding take_damage to add a message
        super().take_damage(amount)
        print(f"'{self.name} the {self.player_class}' screams in pain! HP: {self._current_hp}")
        if not self.is_alive:
            print(f"'{self.name}' has fallen.")

    def attack(self, target: Entity):
        # Implementation of abstract attack
        print(f"'{self.name} the {self.player_class}' attacks {target.name}!")
        damage = self.power + random.randint(1, 6)
        target.take_damage(damage)

    def __repr__(self):
        # A helper to print player status
        return f"[Player: {self.name}, HP: {self._current_hp}/{self.__max_hp}]"


class Monster(Combatant):
    """
    A concrete Monster class.
    This class is INCOMPLETE.
    """
    def __init__(self, name, max_hp, power, monster_type):
        super().__init__(name, max_hp, power)
        self.monster_type = monster_type

    # This class "forgets" to implement abstract methods from Entity
    # and Combatant. (Bug?)


class Trap(Entity):
    """
    A concrete Trap class.
    It's an Entity, but it's not a Combatant.
    """
    def __init__(self, name, damage):
        # This init call is wrong. (Bug?)
        super().__init__(self, name) 
        self.__damage = damage
        print(f"A dangerous {self.name} trap is set.")

    def is_alive(self):
        # A trap is always "alive" until triggered
        return self._current_hp > 0

    def take_damage(self, amount):
        # Traps can't "take" damage, they just exist.
        print(f"The {self.name} trap cannot be damaged.")

    def spring_trap(self, target: Entity):
        print(f"The {self.name} trap springs on {target.name}!")
        # Trying to access the target's private variable. (Bug?)
        if target.__max_hp > 100:
            print("The trap is extra effective!")
            target.take_damage(self.__damage * 2)
        else:
            target.take_damage(self.__damage)
        
        # Trap deactivates
        self._current_hp = 0

# --- Simulation ---

print("--- Welcome to the Buggy Dungeon ---")

try:
    # 1. Try to create a Player
    hero = Player(name="Sir Bugsalot", player_class="Knight", max_hp=150, power=20)
    print(f"Hero created: {hero.name}")

    # 2. Try to create a Monster
    goblin = Monster(name="Grumble", max_hp=50, power=10, monster_type="Goblin")
    print(f"Monster created: {goblin.name}")

    # 3. Try to create a Trap
    spike_trap = Trap(name="Spike Pit", damage=25)
    
    # 4. Let's fight!
    print("\n--- Combat Begins! ---")
    hero.attack(goblin)
    
    # 5. The trap springs
    print("\n--- Hero steps on a trap! ---")
    spike_trap.spring_trap(hero)

    # 6. Check status
    print(f"\nHero Status: {hero.get_health_percentage()}% HP")
    print(f"Monster Status: {goblin.is_alive()}")


except Exception as e:
    print(f"\n🔥🔥🔥 A CRITICAL ERROR OCCURRED 🔥🔥🔥")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")

print("---------------------------------")

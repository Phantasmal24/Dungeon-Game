from abc import ABC, abstractmethod
import random
class Entity(ABC):
    def __init__(self, name, max_hp, current_hp):
        self.name = name
        self._max_hp = max_hp
        self._current_hp = current_hp
    @property
    @abstractmethod
    def is_alive(self):
        pass
    @abstractmethod
    def take_damage(self, amount):
        pass
    def get_health_percentage(self):
        return (self._current_hp / self._max_hp) * 100

class Combatant(Entity):
    def __init__(self, name, max_hp, power):
        super().__init__(name, max_hp, max_hp)
        self._power = power
    @abstractmethod
    def attack(self, target: Entity):
        # Logic for attacking another entity
        pass

class Player(Combatant):
    def __init__(self, name, max_hp, power, player_class):
        super().__init__(name, max_hp, power)
        self.player_class = player_class
    def is_alive(self):
        return self._current_hp > 0
    def take_damage(self, amount):
        self._current_hp -= amount
        print(f"'{self.name} the {self.player_class}' screams in pain! HP: {self._current_hp}")
    def attack(self, target: Entity):
        print(f"'{self.name} the {self.player_class}' attacks {target.name}!")
        damage = self._power + random.randint(1, 6)
        target.take_damage(damage)
    
class Monster(Combatant):
    def __init__(self, name, max_hp, power, monster_type):
        super().__init__(name, max_hp, power)
        self.monster_type = monster_type
    def is_alive(self):
        return self._current_hp > 0
    def take_damage(self, amount):
        self._current_hp -= amount
        print(f"The {self.name} {self.monster_type} takes {amount} damage! HP: {self._current_hp}")
    def attack(self, target: Entity):
        print(f"The {self.name} {self.monster_type} attacks {target.name}!")
        damage = self._power + random.randint(1, 6)
        target.take_damage(damage)

class Trap(Entity):
    def __init__(self, name, max_hp, current_hp, damage):
        super().__init__(name, max_hp, current_hp)
        self._damage = damage
    def is_alive(self):
        return self._current_hp > 0
    def take_damage(self, amount):
        print("The attack has no effect on the trap!")
    def spring_trap(self, target: Entity):
        print(f"The Spike Pit springs on {target.name}!")
        target.take_damage(self._damage)
        self._current_hp = 0
    def is_alive(self):
        return self._current_hp > 0
    def take_damage(self, amount):
        super().take_damage(amount)
        # It sets its own health to 0 to deactivate it
        self._current_hp = 0
        print(f"The {self.name} trap takes {amount} damage! HP: {self._current_hp}")
        print(f"The {self.name} trap has been deactivated.")

# --- Simulation ---

print("--- Welcome to the Buggy Dungeon ---")

try:
    # 1. Try to create a Player
    hero = Player(name="Sir Bugsalot", max_hp=150, power=20, player_class="Knight")
    print(f"Hero created: {hero.name}")

    # 2. Try to create a Monster
    goblin = Monster(name="Grumble", max_hp=50, power=10, monster_type="Goblin")
    print(f"Monster created: {goblin.name}")

    # 3. Try to create a Trap
    spike_trap = Trap(name="Spike Pit", max_hp=100, current_hp=100, damage=25)
    
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
    print(f"An error occurred: {e}")
# attn_system.py
from dataclasses import dataclass, field
from typing import Dict, List
import random

@dataclass
class Project:
    name: str
    impact_type: str
    impact_unit: str
    goal: float
    funded: float = 0.0
    votes: int = 0

@dataclass
class User:
    username: str
    attn_balance: float = 0.0

@dataclass
class Treasury:
    total_funds: float = 0.0  # argent réel (sponsors/pub)
    attn_supply: float = 0.0
    attn_price: float = 0.01  # 1 $ATTN = 0.01 USD (exemple)

    def mint_attn(self, amount_usd: float) -> float:
        """Convertit les revenus en tokens $ATTN."""
        minted = amount_usd / self.attn_price
        self.attn_supply += minted
        self.total_funds += amount_usd
        return minted

    def distribute_funds(self, projects: List[Project], votes: Dict[str, int]):
        """Redistribue les fonds selon les votes."""
        total_votes = sum(votes.values())
        if total_votes == 0:
            return
        for p in projects:
            portion = votes.get(p.name, 0) / total_votes
            allocation = self.total_funds * portion
            p.funded += allocation
        self.total_funds = 0  # tout redistribué


class AttentionSystem:
    def __init__(self):
        self.treasury = Treasury()
        self.users: Dict[str, User] = {}
        self.projects: List[Project] = []

    def register_user(self, username: str):
        self.users[username] = User(username)

    def add_project(self, name, impact_type, impact_unit, goal):
        self.projects.append(Project(name, impact_type, impact_unit, goal))

    def simulate_views(self, total_views: int, revenue_per_view: float = 0.001):
        """Simule la génération de revenus grâce aux vues."""
        revenue = total_views * revenue_per_view
        minted = self.treasury.mint_attn(revenue)
        print(f"{total_views} vues → ${revenue:.2f} générés → {minted:.0f} $ATTN créés")

    def distribute_tokens(self):
        """Distribue les $ATTN aux utilisateurs selon leur activité."""
        total = len(self.users)
        for user in self.users.values():
            user.attn_balance += self.treasury.attn_supply / total
        self.treasury.attn_supply = 0

    def vote(self):
        """Chaque utilisateur vote aléatoirement pour un projet."""
        votes = {}
        for user in self.users.values():
            project = random.choice(self.projects)
            votes[project.name] = votes.get(project.name, 0) + 1
        return votes

    def report(self):
        print("\n📊 Rapport de transparence :")
        for p in self.projects:
            print(f"- {p.name}: {p.funded:.2f} USD alloués ({p.impact_type})")


if __name__ == "__main__":
    system = AttentionSystem()
    system.register_user("Alice")
    system.register_user("Bob")
    system.register_user("Clara")

    system.add_project("Reforestation locale", "🌳 arbres plantés", "arbres", goal=10000)
    system.add_project("Nettoyage de plages", "🧹 déchets retirés", "kg", goal=5000)
    system.add_project("Accès à l’eau potable", "💧 personnes aidées", "personnes", goal=2000)

    # Simulation
    system.simulate_views(total_views=1_000_000)
    system.distribute_tokens()
    votes = system.vote()
    system.treasury.distribute_funds(system.projects, votes)
    system.report()

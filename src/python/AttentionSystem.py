# attn_instagram_system.py
import requests
from dataclasses import dataclass, field
from typing import Dict, List

# === CONFIG ===
ACCESS_TOKEN = "EAATiflISEb4BP1myDFUPbghHtf3hpI2Qu3k1btKoToXcRrPy5EQbclKt0RZAAHGE9R4GHZAmtZBubjGrpZBTFnWWbtvKEXMyG80ewzgGuGm46hSQQTZAt5ApySq6B2EQ2HJA4tzewOHylUbUVsJFV0Ut6JQAFpWDAit1Q9Sh6RlnJ3daJvI5peZARdciWogRWvZC5aDW1NeSsbMZA0AuLRPjejdxmcV82oqvJ7GLjIcBrImqHwSYKnnrMdAeS0K6twVM1nydgc9ZA5ydwKwtaS5un5lNLQ8MilzRF2nFeQGJ8HrfKR5hZAUEObHhg7urN4HoHEb8I1QrSlXQZDZD"  # <-- à remplacer
ACCOUNT_ID = "10233775788193804"
INSTAGRAM_API_URL = "https://graph.facebook.com/v18.0"


@dataclass
class User:
    username: str
    attn_balance: float = 0.0


@dataclass
class Treasury:
    attn_price: float = 0.1  # 1 $ATTN = 0.1 USD
    total_usd: float = 0.0
    total_attn: float = 0.0

    def mint_attn(self, usd_amount: float):
        """Convertit un montant USD en tokens $ATTN"""
        tokens = usd_amount / self.attn_price
        self.total_usd += usd_amount
        self.total_attn += tokens
        return tokens


class AttentionSystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.treasury = Treasury()

    def register_user(self, username: str):
        self.users[username] = User(username)

    def get_instagram_metrics(self):
        print("📡 Récupération des métriques Instagram...")
        media_url = f"{INSTAGRAM_API_URL}/{ACCOUNT_ID}/media?fields=id,caption,like_count,comments_count,media_type,video_view_count&access_token={ACCESS_TOKEN}"
        response = requests.get(media_url)
        data = response.json()
        posts = data.get("data", [])

        total_views, total_likes = 0, 0
        for post in posts:
            likes = post.get("like_count", 0)
            views = post.get("video_view_count", 0)
            total_likes += likes
            total_views += views
        print(f"➡️  {len(posts)} publications analysées : {total_views} vues, {total_likes} likes.")
        return total_views, total_likes

    def get_followers(self):
        """Récupère le nombre d’abonnés du compte Instagram."""
        url = f"{INSTAGRAM_API_URL}/{ACCOUNT_ID}?fields=followers_count&access_token={ACCESS_TOKEN}"
        response = requests.get(url)
        data = response.json()
        followers = data.get("followers_count", 0)
        print(f"👥 {followers} abonnés détectés.")
        return followers

    def reward_users(self, views, likes, followers):
        print("Calcul des récompenses en $ATTN...")
        usd_from_views = views * 0.001  # 0.1 cent par vue
        usd_from_likes = likes * 0.005  # 0.5 cent par like
        usd_from_followers = followers * 0.01  # 1 cent par abonné

        total_usd = usd_from_views + usd_from_likes + usd_from_followers
        minted = self.treasury.mint_attn(total_usd)

        # Distribution équitable entre tous les utilisateurs
        for user in self.users.values():
            user.attn_balance += minted / len(self.users)

        print(f"✅ {minted:.0f} $ATTN créés et distribués.")
        print(f"  (Revenus simulés : ${total_usd:.2f})")

    def reward_donations(self, amount_donated, donor_username, allocation):
        print(f"Récompense du don de {amount_donated} USD effectué par {donor_username}...")

        # Créer les tokens en fonction du don
        minted = self.treasury.mint_attn(amount_donated)

        # Calculer la répartition des tokens
        total_allocation = sum(allocation.values())
        if total_allocation != 100:
            print("La somme des répartitions ne fait pas 100%. Elle sera normalisée.")
            # Normaliser la répartition si la somme n'est pas 100
            factor = 100 / total_allocation
            allocation = {project: amount * factor for project, amount in allocation.items()}

        # Répartir les tokens vers chaque projet selon la répartition
        for project, percentage in allocation.items():
            allocated_tokens = minted * (percentage / 100)
            print(f"{allocated_tokens:.2f} $ATTN attribués au projet {project}.")

        # On envoie les tokens au donneur si choix de se garder des tokens
        if "self" in allocation:
            user = self.users[donor_username]
            user.attn_balance += minted * (allocation["self"] / 100)
            print(f"{minted * (allocation['self'] / 100):.2f} $ATTN ajoutés à ton solde.")

        print(f"{minted:.0f} $ATTN créés et répartis.")
        print(f"  (Dons reçus : ${amount_donated:.2f})")

    def report(self):
        """Affiche les soldes des utilisateurs"""
        print("Soldes des utilisateurs :")
        for user in self.users.values():
            print(f" - {user.username}: {user.attn_balance:.2f} $ATTN")


if __name__ == "__main__":
    # Exemple de test
    system = AttentionSystem()
    system.register_user("Alice")
    system.register_user("Bob")
    system.register_user("Clara")

    # Simuler des données Instagram (ou récupérer via l'API)
    try:
        views, likes = system.get_instagram_metrics()
        followers = system.get_followers()
    except Exception:
        print("Mode simulation activé (pas de token Meta).")
        views, likes, followers = 20000, 1500, 500  # Valeurs fictives

    # Récompenses basées sur les actions
    system.reward_users(views, likes, followers)

    amount_donated = 100  # Montant du don en USD
    donor_username = "Alice"  # Nom d'utilisateur du donateur

    allocation = {
        "self": 30,  # Garder 30% des tokens pour soi
        "Reforestation": 40,  # 40% pour Reforestation
        "Eau potable": 30  # 30% pour Eau potable
    }

    # Exemple de récompenses pour les dons ou sponsors
    system.reward_donations(amount_donated, donor_username, allocation)  # Exemple de don de 1000 USD

    # Rapport final
    system.report()
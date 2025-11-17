from flask import Flask, render_template
import sys
from src.python.AttentionSystem import AttentionSystem

app = Flask(__name__)

system = AttentionSystem()

# --- Simulation / pré-remplissage (à remplacer par ta vraie logique)
system.register_user("Alice")
system.register_user("Bob")
system.register_user("Clara")
system.register_user("NeoCyber")
system.register_user("LunaTech")

# Simule des balances (pour tests)
system.users["Alice"].attn_balance = 1200
system.users["Bob"].attn_balance = 850
system.users["Clara"].attn_balance = 4500
system.users["NeoCyber"].attn_balance = 1800
system.users["LunaTech"].attn_balance = 950


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/leaderboard")
def leaderboard():
    sorted_users = sorted(system.users.values(), key=lambda u: u.attn_balance, reverse=True)
    return render_template("leaderboard.html", users=sorted_users)

# -------------------------------
# 🚀 Nouvelle page INSIGHT
# -------------------------------
@app.route("/insight")
def insight():

    ig_stats = {
        "views": 128000,
        "likes": 15600,
        "followers": 9400,
        "money": 742.50
    }

    return render_template("insight.html", stats=ig_stats)


if __name__ == "__main__":
    app.run(debug=True)

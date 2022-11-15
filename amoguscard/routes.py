from flask import flash, render_template, redirect, url_for
from amoguscard import app, db
from amoguscard.models import Card, User
from flask_login import login_required, current_user
import random

@app.route("/allcards")
def allcards():
    return render_template("allcards.html")

@login_required
@app.route("/freecard")
def freecard():
    try:
        card = Card(cardId=random.randint(0, 6), owner=current_user)

        db.session.add(card)
        db.session.commit()
    except:
        pass

    return redirect(url_for("index"))

@login_required
@app.route("/getpack")
def getpack():
    try:
        if current_user.credits >= 100:
            current_user.credits -= 100
            for i in range(10):
                card = Card(cardId=random.randint(0, 6), owner=current_user)

                db.session.add(card)
            db.session.commit()
    except:
        pass

    flash("Bought pack.")
    return redirect(url_for("index"))

@login_required
@app.route("/")
def index():
    try:
        return render_template("index.html", name=current_user.name, cardCount=len(current_user.cards), cards=current_user.cards, credits=current_user.credits)
    except:
        return redirect(url_for("login"))
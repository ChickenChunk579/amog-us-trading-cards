from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from amoguscard import app, db
from amoguscard.models import Card, TradeOffer, User

@login_required
@app.route("/trades")
def trades():
    try:
        trades = TradeOffer.query.filter_by(senderId=current_user.id)
        return render_template("trades.html", trades=trades, user=current_user)
    except:
        return redirect(url_for("login"))

@login_required
@app.route("/trade/create")
def createtrade():
    try:
        return render_template("createtrade.html")
    except:
        return redirect(url_for("login"))

@login_required
@app.route("/trade/accept")
def acceptTrade():
    try:
        trade = TradeOffer.query.get(request.args.get("id"))
        return render_template("accepttrade.html", tradeId=request.args.get("id"), card=Card.query.get(trade.cardId1))
    except:
        return redirect(url_for("login"))

@login_required
@app.route("/trade/accept", methods=["POST"])
def acceptTradePost():
    flash("Accepted trade!")

    cardIdToTrade = request.form["cardId"]
    tradeId = request.args.get("tradeId")

    TradeOffer.query.filter_by(id=tradeId).update(dict(cardId2=cardIdToTrade, isAccepted=True, recieverId=current_user.id))

    db.session.commit()

    return redirect(url_for("index"))

@login_required
@app.route("/trade/viewOffer")
def viewTradeOffer():
    trade = TradeOffer.query.get(request.args.get("tradeId"))

    return render_template("viewoffer.html", trade=trade, card=Card.query.get(trade.cardId2).cardId)

@login_required
@app.route("/trade/viewOffer", methods=["POST"])
def viewTradeOfferPost():
    trade = TradeOffer.query.get(request.args.get("id"))

    Card.query.filter_by(id=trade.cardId1).first().owner_id = trade.recieverId
    Card.query.filter_by(id=trade.cardId2).first().owner_id = trade.senderId

    db.session.commit()

    TradeOffer.query.get(trade.id).delete()

    return redirect(url_for("index"))

@login_required
@app.route("/trade/create", methods=["POST"])
def createTradePost():
    trade = TradeOffer(cardId1=request.form["cardId"], cardId2=-1, senderId=current_user.id, name=request.form["name"])

    db.session.add(trade)
    db.session.commit()

    return redirect(url_for("trades"))
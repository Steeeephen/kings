from __future__ import print_function
from flask import Flask, request, render_template, send_file, redirect, g
import random
import pickle

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def my_form():
    return render_template('test.html')

@app.route('/', methods=['POST'])
def getname():
    if request.method == "POST":
        rules = {
            1:'Waterfall',2:'You',3:'Me',4:'Whores',5:'Dive',6:'Dicks',7:'Heaven',
            8:'Mate',9:'Rhyme',10:'Never Have I Ever',11:'Rule',12:'Questionmaster',13:'King'
            }
        with open('rules', 'wb') as fp:
            pickle.dump(rules, fp)


        players = request.form['Name'].replace(" ", "").split(",")
        with open('players', 'wb') as fp:
            pickle.dump(players, fp)

        cards = list(range(1,14))*4
        random.shuffle(cards)
        with open('cards', 'wb') as fp:
            pickle.dump(cards, fp)

        with open('kings', 'wb') as fp:
            pickle.dump(0, fp)
        
        return redirect('/game')

@app.route('/game')
def ingame():
    with open('cards', 'rb') as fp:
        cards = pickle.load(fp)
    card = cards.pop()

    with open ('players', 'rb') as fp:
        players = pickle.load(fp)
    player = players[0]
    players = players[1:]
    players.append(player)


    with open('rules', 'rb') as fp:
        rules = pickle.load(fp)

    if(int(card) == 13):
        with open('kings','rb') as fp:
            kings = int(pickle.load(fp))
        kings += 1
        print(kings)
        if(kings == 4):
            return render_template("winner.html", player = player.upper())
        else:
            with open('kings', 'wb') as fp:
                pickle.dump(kings, fp)
        


    #html_write(player,card)
    
    with open('cards', 'wb') as fp:
        pickle.dump(cards, fp)
    with open('players', 'wb') as fp:
        pickle.dump(players, fp)

    return render_template('graph.html', player = player.capitalize(), rule = rules[card], card = card)

if __name__ == "__main__":
    app.run(debug = True)

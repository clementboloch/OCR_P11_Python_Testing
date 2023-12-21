import json
from flask import Flask,render_template,request,redirect,flash,url_for,abort
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

def getClub(club):
    matches = [c for c in clubs if c['name'] == club]
    if len(matches) == 0:
        abort(400, description="Bad Request: Club does not exist.")
    else:
        return matches[0]

def getCompetition(competition):
    matches = [c for c in competitions if c['name'] == competition]
    if len(matches) == 0:
        abort(400, description="Bad Request: Competition does not exist.")
    else:
        return matches[0]

@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    request_email = request.form['email']
    club_list = [club for club in clubs if club['email'] == request_email]
    if club_list:
        club = club_list[0]
        return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)
    else:
        abort(403, description="Access denied: Your email address is not one of authorised the clubs.")


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = getClub(club)
    foundCompetition = getCompetition(competition)
    if foundClub and foundCompetition:
        today = datetime.now()
        competitionDate = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
        if competitionDate >= today:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            abort(400, description="Bad Request: You cannot book places for past competitions.")
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = getCompetition(request.form['competition'])
    club = getClub(request.form['club'])
    placesRequired = int(request.form['places'])

    if placesRequired < 0:
        abort(400, description="Bad Request: You cannot buy a negative number of places.")
    elif placesRequired > int(club['points']):
        abort(403, description="Forbidden: You cannot buy more places than you have points.")
    elif placesRequired > 12:
        abort(403, description="Forbidden: You cannot buy more than 12 places.")
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = str(int(club['points'])-placesRequired)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
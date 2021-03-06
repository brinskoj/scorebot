# -*- coding: cp1252 -*-
from time import asctime, localtime, time
from twisted.internet import reactor
import inspect
import re
import random
import sys
import hashlib
import httplib
import json
import urllib, urllib2


admins = [
   # Names here
   'Killerhands',
]

NFLTeams = {
    '49ers' : 'SF',
    'sf' : 'SF',
    'niners' : 'SF',

    'bears' : 'CHI',
    'chi' : 'CHI',
    'chicago' : 'CHI',

    'bengals' : 'CIN',
    'cincinati' : 'CIN',
    'cin' : 'CIN',

    'bills' : 'BUF',
    'buffalo' : 'BUF',
    'buf' : 'BUF',

    'broncos' : 'DEN',
    'denver' : 'DEN',
    'den' : 'DEN',

    'browns' : 'CLE',
    'cleveland' : 'CLE',
    'cle' : 'CLE',

    'buccaneers' : 'TB',
    'bucs' :'TB',
    'tampabay' : 'TB',
    'tampa bay' : 'TB',
    'tb' : 'TB',

    'cardinals' :'ARZ',
    'arizona' : 'ARZ',
    'zona' : 'ARZ',
    'cards' : 'ARZ',
    'arz' : 'ARZ',

    'chargers' : 'SD',
    'san diego' : 'SD',
    'sandiego' : 'SD',
    'sd' : 'SD',

    'chiefs' : 'KC',
    'kansas city' : 'KC',
    'kansas' : 'KC',
    'kc' : 'KC',

    'colts' : 'IND',
    'indy' : 'IND',
    'indianapolis' : 'IND',
    'ind' : 'IND',

    'cowboys' : 'DAL',
    'dallas' : 'DAL',
    'dal' : 'DAL',

    'dolphins' : 'MIA',
    'miami' : 'MIA',
    'mia' : 'MIA',

    'eagles' : 'PHI',
    'phi' : 'PHI',
    'philidelphia' : 'PHI',
    'philly' : 'PHI',

    'falcons' : 'ATL',
    'atlanta' : 'ATL',
    'hotlanta' : 'ATL',
    'atl' : 'atl',

    'giants' : 'NYG',
    'nyg' : 'NYG',

    'jaguars' : 'JAC',
    'jags' : 'JAC',
    'jacksonville' : 'JAC',
    'jax' : 'JAC',

    'jets' : 'NYJ',
    'nyj' : 'NYJ',

    'lions' : 'DET',
    'detroit' : 'DET',
    'det' : 'DET',

    'packers' : 'GB',
    'green bay' :'GB',
    'greenbay' : 'GB',
    'gb' : 'GB',

    'panthers' : 'CAR',
    'carolina' : 'CAR',
    'car' : 'CAR',

    'patriots' : 'NE',
    'pats' : 'NE',
    'new england' : 'NE',
    'ne' : 'NE',

    'raiders' : 'OAK',
    'oakland' : 'OAK',
    'oak' : 'OAK',

    'rams' :'STL',
    'st louis' : 'STL',
    'stlouis' : 'STL',
    'stl' : 'STL',

    'ravens' : 'BAL',
    'baltimore' : 'BAL',
    'bal' : 'BAL',

    'redskins' : 'WAS',
    'washington' : 'WAS',
    'was' : 'WAS',

    'saints' : 'NO',
    'new orleans' : 'NO',
    'neworleans' : 'NO',
    'no' : 'NO',

    'seahawks' : 'SEA',
    'hawks' : 'SEA',
    'seattle' : 'SEA',
    'sea' : 'SEA',

    'steelers' : 'PIT',
    'stillers' : 'PIT',
    'pittsburgh' : 'PIT',
    'pitt' : 'PIT',
    'pit' : 'PIT',

    'texans' : 'HOU',
    'houston' : 'HOU',
    'hou' : 'hou',

    'titans' : 'TEN',
    'tennesee' : 'TEN',
    'ten' : 'TEN',

    'vikings' : 'MIN',
    'minnesota' : 'MIN',
    'vikes' : 'MIN',
    'min' : 'MIN',
}


NHLTeams = {
    
}
class timeBank:
    prevTime = float(0.0)


def findAction(name):
    name = findAction.pattern.sub('', name)
    for action in actions:
        if action.actionName == name:
            return action
    return None
findAction.pattern = re.compile('[\W_]+')



# Syntax: !cooldown <action> <time>
def cooldown(bot, chan, nick, msg):
    message = msg.strip().split(' ')
    if len(message) < 3:
        bot.msg(chan, '%s: Too few arguments.' % nick)
        return
    
    action,time = message[1:3]
    act = findAction(action)
    
    if not act:
        bot.msg(chan, '%s: Unknown action: %s' % (nick,action))
        return
    try:
        time = int(time)
    except:
        bot.msg(chan, '%s: Invalid time: %s', (nick, time))
        return
    
    act.cooldown = time
    bot.msg(chan, 'Cooldown set to %d seconds.' % time)




NHLGameArray = []
NBAGameArray = []
NFLGameArray = []

Games = []
liveGames = []

class Game:
    def __init__(self, color, sport, gameID, hTeam, aTeam, sHome, sAway, status, startTime, dayOfWeek, winner):
        self.color = color
        self.sport = sport
        self.id = gameID
        self.homeTeam = hTeam
        self.awayTeam = aTeam
        self.sHome = sHome
        self.sAway = sAway
        self.status = status
        self.startTime = startTime
        self.dayOfWeek = dayOfWeek
        self.winner = winner

        if self.status == 'final overtime':
            self.status = 'FINAL OT'

    def getHomeTeam(self):
        return self.homeTeam

    def getAwayTeam(self):
        return self.awayTeam

    def getWinner(self):
        return self.winner

    def getStatus(self):
        return self.status

    def getSport(self):
        return self.sport

    def __cmp__(self, other):
                if self.homeTeam == other.homeTeam and self.awayTeam == other.awayTeam:
					return True
                return False

    def __repr__(self):
        return '[%s] %s %s-%s %s %s' % (self.sport, self.homeTeam, self.sHome, self.sAway, self.awayTeam, self.status)
        



#Return games currently being played
def GetLiveGames():
    global Games
    global liveGames

    liveGames = []
    for game in Games:
        if 'live' in game.status.lower():
            liveGames.append(game)
        else:
            if (game.sport == 'NFL' and 'final' not in game.status.lower()):
                if 'pregame' not in game.status.lower():
                    liveGames.append(game)

    return liveGames


#Return
def postLiveGameStatus(bot, chan, nick, msg):
    GetLiveGames()
    global liveGames
    msg = msg.split(' ')
    if len(msg) > 2:
        return
    try:
        sport = msg[1].upper()
    except:
        sport = 'ALL'

    liveGameStr = 'Live Games: '

    if sport == 'ALL':
        for game in liveGames:
            if game.sport == 'NHL':
                status = game.dayOfWeek
            else:
                status = game.status
            liveGameStr += '%s[%s] %s %s-%s %s %s ' % (game.color, game.sport, game.homeTeam, game.sHome, game.sAway, game.awayTeam, status)
    elif sport == 'NHL':
        for game in liveGames:
            if game.sport == 'NHL':
                liveGameStr += '%s[%s] %s %s-%s %s %s ' % (game.color, game.sport, game.homeTeam, game.sHome, game.sAway, game.awayTeam, game.dayOfWeek)
    elif sport == 'NFL':
        for game in liveGames:
            if game.sport == 'NFL':
                liveGameStr += '%s[%s] %s %s-%s %s %s' % (game.color, game.sport, game.homeTeam,game.sHome, game.sAway, game.awayTeam, game.status)

    print liveGameStr
    bot.msg(chan, str(liveGameStr))


def postGameScores(bot, chan, nick, msg):
    global Games
    msg = msg.split('!')
    msg = msg.split(' ')

    if len(msg) != 2:
        bot.msg(chan, 'Wrong syntax! Use \'!<game>\'')
        return

    currentGame = msg[1].upper()
    print currentGame

    if currentGame is not 'NFL':
        if currentGame is not 'NHL':
            return

    for game in Games:
        if game.sport == currentGame:
            hTeam = game.getHomeTeam()
            aTeam = game.getAwayTeam()
            gWinner = game.getWinner()
            if 'FINAL' in game.status.upper():
                print '%s[%s] %s %s-%s %s' % (game.sport, game.homeTeam, game.sHome, game.sAway, game.awayTeam)
            else:
                if 'LIVE' in game.status:
                    print '%s[%s] %s %s-%s %s | Game Status: %s' % (game.sport, hTeam, aTeam, game.sHome, game.sAway, game.status)
                else:
                    print '%s[%s] %s %s-%s %s | Game Status: %s' % (game.sport, hTeam, game.sHome, game.sAway, aTeam, game.status)


def getNHLScores():
    #global NHLGameArray
    global Games
    replaced = False
    newGames = []

    NHLFeed = urllib2.urlopen('http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp')
    #Parse into Json
    gameStr = NHLFeed.read()
    gameJson = gameStr.strip('loadScoreboard(')
    gameJson = gameJson[:-1]
    gameJson = json.loads(gameJson)

    for game in gameJson['games']:
        htWin = game['htc']
        atWin = game['atc']
        gameStatus = game['bs']

        if 'FINAL' in gameStatus.upper():
            if htWin == '':
                winner = game['htv']
            else:
                winner = game['atv']
                
        newGame = Game(
            color = '\x0302',
            sport = 'NHL',
            gameID = game['id'], 
            hTeam = game['htv'], 
            aTeam = game['atv'],
            sHome = game['hts'],
            sAway = game['ats'],
            status = game['bs'],
            startTime = game['bs'],
            dayOfWeek = game['ts'],
            winner = winner,
             )

        for game in Games:
            if newGame == game:
                if 'FINAL' in newGame.status.upper() and 'FINAL' not in game.status.upper():
                    print 'GAME ENDED!'
                    bot.msg(chan, '[GAME UPDATE!] %s[%s] %s %s-%s %s [%s]' % (newGame.color, newGame.sport, newGame.homeTeam, newGame.sHome, newGame.sAway, newGame.awayTeam, newGame.status))
                    
                Games.remove(game)
                newGames.append(newGame)
                replaced = True
            else:
                replaced = False
                Games.remove(game)
                
        if replaced == True:
            return
        else:
            newGames.append(newGame)
            
    for newGame in newGames:
        Games.append(newGame)
    #print Games
    print 'NHL Scores Updated!'
                

        #NHLGameArray.append(newGame)

    
    #return NHLGameArray

def getNFLScores():
    global Games
    for game in Games:
        if game.sport == "NFL":
            Games.remove(game)

    NFLFeed = urllib2.urlopen('http://www.nfl.com/liveupdate/scorestrip/scorestrip.json')
    #Parse into Json
    gameStr = NFLFeed.read()
    gameJson = gameStr.split('[')
    gameJson.pop(0)
    gameJson.pop(0)

    for game in gameJson:
        game = game.split(',')
        #for stuff in game:
    #       stuff = stuff.strip('"')
            #print stuff
        #print game

    for game in gameJson:
        game = game.split(',')
        hTeam = game[4].strip('"')
        aTeam = game[6].strip('"')
        sHome = game[5].strip('"')
        sAway = game[7].strip('"')

        if sHome == '':
            sHome = 0
        if sAway == '':
            sAway = 0


        if sHome > sAway:
            winner = hTeam
        elif sHome < sAway:
            winner = aTeam
        else:
            winner = 'N/A'

        if 'final' in game[2].lower():
            status = game[2].upper().strip('"')
        else:
            status = game[2].strip('"') + ' ' + game[3].strip('"')
        newGame = Game(
            color = '\x0304',
            sport = 'NFL',
            gameID = 0, 
            hTeam = hTeam, 
            aTeam = aTeam,
            sHome = sHome,
            sAway = sAway,
            status = status,
            startTime = game[2].strip('"'),
            dayOfWeek = game[0].strip('"') + ' ' + game[1].strip('"'),
            winner = winner,
             )

        Games.append(newGame)

        #NFLGameArray.append(newGame)

    #for game in Games:
    #    if game.sport == 'NFL':
    #        print '[NFL] - %s %s-%s %s' % (game.homeTeam, game.sHome, game.sAway, game.awayTeam)
    return NFLGameArray



def returnGameStatus(bot, chan, nick, msg):
    global Games
    global NFLTeams
    global NHLTeams
    print Games

    gameFound = None
    msg = msg.split(' ')
    if len(msg) > 3:
        bot.msg(chan, 'invalid arguments. Try \'!score <team> <team>\' or \'!score <team>\'')

    if len(msg) == 3:
        teamOne = msg[1].lower()
        print 'teamOne %s' % teamOne
        teamTwo = msg[2].lower()
        print 'teamTwo %s' % teamTwo

        if teamOne in NFLTeams:
            teamOne = NFLTeams[teamOne]


        if teamTwo in NFLTeams:
            teamTwo = NFLTeams[teamTwo]


        #Still have to handle NHL teams

        for game in Games:
            if game.homeTeam.upper() == teamOne.upper() and game.awayTeam.upper() == teamTwo.upper():
                gameFound = game
                break
            if game.homeTeam.upper() == teamTwo.upper() and game.awayTeam.upper() == teamOne.upper():
                gameFound = game
                break

    if len(msg) == 2:
        teamOne = msg[1].lower()
        print 'teamOne %s' % teamOne

        if teamOne in NFLTeams:
            teamOne = NFLTeams[teamOne]

        for game in Games:
            if game.homeTeam.upper() == teamOne.upper() or game.awayTeam.upper() == teamOne.upper():
                gameFound = game
                break

    if gameFound is None:
        print "No Game Found!"
    else:
        if gameFound.sport == 'NHL' and gameFound.status != 'FINAL':
            gameString = '%s[%s] %s %s-%s %s [%s %s] ' % (gameFound.color, gameFound.sport, gameFound.homeTeam, gameFound.sHome, gameFound.sAway, gameFound.awayTeam, gameFound.dayOfWeek, gameFound.status)
        else:
            if gameFound.sport == 'NFL' and 'pregame' in gameFound.status.lower():
                gameString = '%s[%s] %s %s-%s %s [%s] ' % (gameFound.color, gameFound.sport, gameFound.homeTeam, gameFound.sHome, gameFound.sAway, gameFound.awayTeam, gameFound.dayOfWeek)
            else:
                gameString = '%s[%s] %s %s-%s %s [%s]' % (game.color, gameFound.sport, gameFound.homeTeam, gameFound.sHome, gameFound.sAway, gameFound.awayTeam, gameFound.status)
        print gameString
        bot.msg(chan, str(gameString))
        return game


def returnNextGame(bot, chan, nick, msg):
    global Games
    nextGames = []
    gameString = ''

    gameFound = None
    msg = msg.split(' ')
    if len(msg) > 3:
        bot.msg(chan, 'invalid arguments. Try \'!score <team> <team>\' or \'!score <team>\'')

    if len(msg) == 3:
        teamOne = msg[1].upper()
        print 'teamOne %s' % teamOne
        teamTwo = msg[2].upper()
        print 'teamTwo %s' % teamTwo

        for game in Games:
            if game.homeTeam.upper() == teamOne and game.awayTeam.upper() == teamTwo:
                gameFound = game
                break
            if game.homeTeam.upper() == teamTwo and game.awayTeam.upper() == teamOne:
                gameFound = game
                break
    if len(msg) == 2:
        teamOne = msg[1].upper()
        print 'teamOne %s' % teamOne

        for game in Games:
            if game.homeTeam.upper() == teamOne or game.awayTeam.upper() == teamOne:
                nextGames.append(game)
                break

    if nextGames is None:
        print "No Game Found!"
    else:
        for gameFound in nextGames:
            if gameFound.status != 'FINAL' and gameFound.status != 'LIVE':
                gameString += '%s[%s] %s %s-%s %s [%s %s] ' % (gameFound.color, gameFound.sport, gameFound.homeTeam, gameFound.sHome, gameFound.sAway, gameFound.awayTeam, gameFound.dayOfWeek, gameFound.status)
            print gameString
        bot.msg(chan, str(gameString))
            



def updateAllScores():
    global Games
    Games = []
    getNHLScores()
    #getNFLScores()
    reactor.callLater(160, updateAllScores)

updateAllScores()


def rehashCmd(bot, chan, nick, msg):
    bot.command_rehash()
    bot.msg(chan, 'Rehash\'d')


#If game in games: update game
#       If game was not finished and is now finished push 'Game Ended sequence'

            
class Action:
    pattern = re.compile('[\W_]+')
    def __init__(self, trigger='', response=[], admin=False, active=True, question=False, extAction=None, cooldown=0, whiteList=[], blackList=[], orTriggers=[], andTriggers=[]):
        self.trigger = trigger
        self.admin = admin
        self.response = response
        self.active = active
        self.question = question
        self.extAction = extAction
        self.cooldown = cooldown
        self.whiteList = whiteList
        self.blackList = blackList
        self.orTriggers = orTriggers
        self.andTriggers = andTriggers
        
        self.lastUsed = 0
        
        tmp = trigger if trigger else orTriggers[0] if orTriggers else andTriggers[0]
        self.actionName = Action.pattern.sub('', tmp.lower())
    
    def matchTrigger(self, msg):
        if self.trigger[0] == '!' and msg[0] == '!':
            return self.trigger and self.trigger in msg
        else:
            if self.trigger[0] == '!' and msg[0] != '!':
                return False
            else:
                return self.trigger and self.trigger in msg
    
    def matchATriggers(self, msg):
        if not self.andTriggers:
            return False
        
        for trigger in self.andTriggers:
            if trigger not in msg:
                return False
        return True
    
    def matchOTriggers(self, msg):
        if not self.orTriggers:
            return False
        
        for trigger in self.orTriggers:
            if trigger in msg:
                return True
        return False
    
    def shouldAct(self, nick, msg, bot):
        if self.active != bot.active:
            return False
        if self.lastUsed + self.cooldown > time():
            return False
        if self.admin and nick not in bot.admins:
            return False
        if self.whiteList and nick not in self.whiteList:
            return False
        #if nick in self.blackList or nick in globalBlackList:
        #    return False
        if self.question and '?' not in msg and not msg.startswith('!'):
            return False
        if not self.matchTrigger(msg) and not self.matchATriggers(msg) and not self.matchOTriggers(msg):
            return False
        return True
    
    def act(self, chan, nick, msg, bot):
        if not self.shouldAct(nick, msg, bot):
            return False
        
        self.lastUsed = time()
        if self.extAction:
            argc = len(inspect.getargspec(self.extAction)[0])
            if argc == 1:
                self.extAction(bot)
            elif argc == 2:
                self.extAction(bot, chan)
            elif argc == 4:
                self.extAction(bot, chan, nick, msg)
        if isinstance(self.response, str):
            bot.msg(chan, self.response.format(nick))
        else:
            for line in self.response:
                bot.msg(chan, line.format(nick))
        return True    

actions = (
    Action('!activate', ['\x01ACTION bot ACTIVATED BloodTrail '],
        admin = True,
        active = False,
        extAction = lambda bot: setattr(bot, 'active', True)),
    
    Action('!deactivate', 'bot Deactivated by {0}',
        admin = True,
        extAction = lambda bot: setattr(bot, 'active', False)),
    
    Action('!time',
        extAction = lambda bot, chan: bot.msg(chan, asctime(localtime()))),

    Action('!score',
        cooldown=10,
        extAction = returnGameStatus),

    Action('!live',
        cooldown=10,
        extAction = postLiveGameStatus),

    Action('!next',
        cooldown=10,
        extAction = returnNextGame),
    )

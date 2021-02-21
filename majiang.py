# Yet Another 2 Person Majiang, in Python 3
#
# Author: Hu, Ying-Hao (hyinghao@hotmail.com)
# This is a text based game simulation
# It will automatically play a 2 person majiang game

# Notes: make sure, only execute it under linux (ubuntu), cuz, clear cmd is used
# Have fun !


import random
import time
import os

class Majiang:
  def __init__(self, majiangType, num):
    self.majiangType = majiangType
    self.num = num
    self.hidden = True

  def __str__(self):
    if self.hidden:
      return "[]"
    else:
      return "%s%d" % (self.majiangType, self.num+1)

  def __repl__(self):
    if self.hidden:
      return "[]"
    else:
      return "%s%d" % (self.majiangType, self.num+1)

class Player:
  INIT_STATE = 0
  NORMAL_STATE = 1
  ENDING_STATE = 9

  def __init__(self, name, playerId, game):
    self.name = name
    self.playerId = playerId
    self.game = game
    self.state = Player.INIT_STATE
    self.startLineId = {0:0, 1:3}[self.playerId]
    self.holding = None

  def play(self):
    if self.holding != None:
      self.state = Player.NORMAL_STATE

    if self.state == Player.INIT_STATE:
      return self.random_pick()
    if self.state == Player.NORMAL_STATE:
      return self.next()

  def next(self):
    if self.holding != None:
      m = self.holding
      mI, mJ, mK = self.playerId, {0:0, 1:3}[self.playerId], m.num
      m2 = self.game.get_majiang(mI, mJ, mK)
      if self.playerId == 0:
        for i in range(3):
          m0 = self.game.get_majiang(self.playerId, i+1, m.num)
          self.game.set_majiang(self.playerId, i, m.num, m0)
        self.game.set_majiang(self.playerId, 3, m.num, m)
        self.holding = None
      else:
        for i in range(3):
          m0 = self.game.get_majiang(self.playerId, 3-i-1, m.num)
          self.game.set_majiang(self.playerId, 3-i, m.num, m0)
        self.game.set_majiang(self.playerId, 0, m.num, m)
        self.holding = None
     
      if m2 != None:
        nextPlayer = self.game.majiangTypes.index(m2.majiangType)
        self.game.players[nextPlayer].holding = m2
        m2.hidden = False
        return m2
      else:
        self.game.players[0].holding = None
        self.game.players[1].holding = None
        self.state = Player.INIT_STATE
        return None



  def random_pick(self):
    hiddenCount = 0 
    for i in range(9):
      m = self.game.get_majiang(self.playerId, self.startLineId, i)
      if m.hidden:
        hiddenCount += 1
    if hiddenCount == 0:
      return None

    while(True):
      p = random.randint(0, 8)
      m = self.game.get_majiang(self.playerId, self.startLineId, p)
      mI, mJ, mK = self.playerId, self.startLineId, p
      if m.hidden:
        m.hidden = False
        self.state = Player.NORMAL_STATE
        break

    nextPlayer = self.game.majiangTypes.index(m.majiangType)
    self.game.players[nextPlayer].holding = m
    self.game.set_majiang(mI, mJ, mK, None) 

    if mI == 0:
      for i in range(3):
        m0 = self.game.get_majiang(mI, i+1, mK)
        self.game.set_majiang(mI, i, mK, m0)
        self.game.set_majiang(mI, i+1, mK, None)
    else:
      for i in range(3):
        m0 = self.game.get_majiang(mI, (3-i-1), mK)
        self.game.set_majiang(mI, (3-i), mK, m0)
        self.game.set_majiang(mI, (3-i-1), mK, None)

    m.hidden = False
    return m


class Game:
  def __init__(self):
    self.players = [
      Player("Player-0",0,self), 
      Player("Player-1",1,self)
    ]
    self.majiangTypes = ["W", "T"]
    self.majiangs = self.shuffle_majiangs()
    self.currentPlayer = self.toss_coin()

  def toss_coin(self):
    return random.randint(0,1)

  def shuffle_majiangs(self):
    self.majiangs = []
    for i in range(2):
      for j in range(4):
        for k in range(9):
          self.majiangs.append(
            Majiang(self.majiangTypes[i], k)
          )
    random.shuffle(self.majiangs)
    return self.majiangs

  def which_majiang(self, m):
    if m == None:
      return -1, -1, -1

    for i in range(2):
      for j in range(4):
        for k in range(9):
          if self.get_majiang(i,j,k) == m:
            return i, j, k
    return -1, -1, -1

  def get_majiang(self, i, j, k):
    return self.majiangs[i*4*9+j*9+k]

  def set_majiang(self, i, j, k, m):
    self.majiangs[i*4*9+j*9+k] = m
    return m

  def show_game(self):
    print("Yet another 2-Person Majiang")
    print()
    placeholder = "  "
    holdings, currentPlayers = [], [] 
    for i in range(2):
      if self.currentPlayer == i:
        currentPlayers.append("*")
      else:
        currentPlayers.append(" ")

      m = self.players[i].holding
      if m == None:
        holdings.append(placeholder)
      else:
        holdings.append("holding: "+ str(m))

    print("%s [W]%s %s" %(currentPlayers[0], self.players[0].name, holdings[0]))
    for i in range(2):
      if i == 1:
        print()
      for j in range(4):
        line = []
        for k in range(9):
          m = self.get_majiang(i,j,k)
          if m == None:
            m = placeholder
          line.append(str(m))
        line = " ".join(line)
        print(line)
    print("%s [T]%s %s" %(currentPlayers[1], self.players[1].name, holdings[1]))

  def sleep(self):
    time.sleep(0.25)
    return self

  def clear(self):
    os.system("clear")
    return self

  def won(self):
    for i in range(2):
      hiddenCount = 0
      for j in range(4):
        for k in range(9):
          m = self.get_majiang(i,j,k)
          if m == None:
            hiddenCount += 1
          else:
            if m.hidden:
              hiddenCount += 1
      if hiddenCount == 0:
        return i
    return -1 # nobody win

  # The game has its own logic of play()
  def play(self):
    self.clear()
    self.show_game()
    while True:
      # check win or not 
      won = self.won()
      if won in [0,1]:
        # self.clear()
        break

      self.sleep()
      m = self.players[self.currentPlayer].play()
      mI, mJ, mK = self.which_majiang(m)
      
      if m != None:
        nextPlayer = self.majiangTypes.index(m.majiangType)
      else:
        nextPlayer = self.currentPlayer
      self.currentPlayer = nextPlayer
      self.clear()
      self.show_game()


    print("%s won! congratulations!" % self.players[won].name)
    self.sleep()


if __name__ == "__main__":
  game = Game()
  game.play()

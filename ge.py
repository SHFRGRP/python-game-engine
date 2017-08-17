"""
The Game Engine writted in Python3
Run it and read output

v1.0:
First Version
v1.1:
Improved LiveObject alive
v1.2:
Added Util.transfstr
Protected Player().lvl
Code optimization

"""

import re

debug = True


class Util:

    def transfstr(str1, self=None, frm=None, to=None):
  
     array = [self, frm, to]
     dict = {self:"self", frm:"frm", to:"to"}
     for i in array:
       if not i == None:
         if type(i) == GameObject or type(i) == LiveObject or type(i) == InteractObject or type(i) == Player:
          str1 = re.sub('{'+dict.get(i)+'.name}', i.name, str1)
          str1 = re.sub('{'+dict.get(i)+'.description}', str(i.description), str1)
         if type(i) == LiveObject or type(i) == InteractObject or type(i) == Player:
          str1 = re.sub('{'+dict.get(i)+'.health}', str(i.health), str1)
         if type(i) == InteractObject or type(i) == Player:
          str1 = re.sub('{'+dict.get(i)+'.money}', str(i.money), str1)
         if type(i) == Player:
          str1 = re.sub('{'+dict.get(i)+'.score}', str(i.score), str1)
     return str1


class GameObject:
 
  def __init__(self, name="No name", description="No description"):
    self.description = description 
    self._name = name
    
  @property
  def name(self):
    return self._name
    
  @name.setter
  def objectName(self, name):
    self._name = name
    
 # def destroy(self):
 #   while self:
 #     del self
  
class LiveObject(GameObject):

  def __init__(self, name="No name", description="No description", health=100):
    self.health = health
    self._alive = True
    super().__init__(name, description)
    
  @property
  def alive(self):
    return self._alive
  
  def addHealth(self, health):
     if self.alive:
      try:
       self.health += health
       if self.health <= 0:
        self._alive = False
      except:
       print('In-Game error: healing object not found or incorrect!')
     else:
      print('In-Game error: '+self.name+" is dead!")
      
  def kill(self):
     if self.alive:
      try:
       self.addHealth(-self.health)
       self._alive = False
      except:
       print('In-Game error: killing object not found or incorrect!')
     else:
      print("In-Game error: "+self.name+" already dead!")
  
  

class InteractObject(LiveObject):

  def __init__(self, name="No name", description="No description", health=100, money=0, listen_dictonary={'hi!':'Hello, {frm.name}!'}, can_say=True, score_to_add=0):
    self.money = money
    self.listen_dictonary = listen_dictonary
    self._score_to_add = score_to_add
    self.can_say = can_say
    super().__init__(name, description, health)
    


  def say(self, msg, to=None, msg2=" => {to.name}"):
     if self.alive:
      if self.can_say:
       try:
         if to == None:
           print(self.name+": "+msg)
         else:
             msg2 = Util.transfstr(msg2, self, None, to)
             print(self.name+": "+msg+msg2)
             to.listen(msg.lower(), self)
       except:
         print('In-Game error: listener not found or incorrect!')
      else:
       print(self.name+" can't say.")
     else:
      print('In-Game error: '+self.name+" is dead!")
      
  def listen(self, msg, frm):
     if self.alive:
      if self.can_say:
       msg = msg.lower()
       if msg in self.listen_dictonary:
         to_say = self.listen_dictonary.get(msg)
         #**********
         to_say = Util.transfstr(to_say, self, frm)
        #**********
         print(self.name+": "+to_say)
       else:
         print(self.name+": I don\'t understand you, "+frm.name)
      else:
       print(self.name+" can't say.")
     else:
      print('In-Game error: '+self.name+" is dead!")
    
  def add_listen_exp(self, to_listen, to_say):
    to_listen = to_listen.lower()
    self.listen_dictonary[to_listen] = to_say
    
  
  def add_money(self, money, frm = None, msg = '{self.name} got {money} money', msg2 = " from {frm.name}", err_msg="{frm.name} or {self.name} haven't enought money"):
     if self.alive:
      #**********
      msg = Util.transfstr(msg, self, frm)
      msg = re.sub('{money}', str(money), msg)
      #**********
      try:
        if frm==None: 
           if self.money+money >= 0:
            self.money += money
            print(msg)
            return True 
           else:
             err_msg = Util.transfstr(err_msg, self, frm)
             print(err_msg)
             return False
        else:
          if frm.money-money >= 0 and self.money+money >= 0:
            frm.money -= money 
            self.money += money
            #**********
            msg2 = Util.transfstr(msg2, self, frm)
            #**********
            print(msg+msg2)
            return True 
          else:
            err_msg = Util.transfstr(err_msg, self, frm)
            print(err_msg)
            return False 
      except:
        print('In-Game error: giver not found or incorrect!')
     else:
      print('In-Game error: '+self.name+" is dead!")
      
      
    
      

class Player(InteractObject):
  
  def __init__(self, name="No name", description="No description", health=100, money=0, listen_dictonary={'hi!':'Hello, {frm.name}!'}, lvlDict={1:0, 2:100}):
    self._lvl = 1
    self.lvlDict = lvlDict
    self.score = 0
    super().__init__(name, description, health, money, listen_dictonary)
    
  @property
  def lvl(self):
    return self._lvl
    
  def addScore(self, score):
   if self.alive:
    self.score += score
    while self.checkLVL():
     continue
   else:
    print('In-Game error: '+self.name+" is dead!")
    
  def checkLVL(self):
    if self.lvl+1 in self.lvlDict:
      if self.score >= self.lvlDict.get(self.lvl+1):
        self._lvl += 1
        print("#You have reached Level "+str(self.lvl))
        return True
      else:
        return False
    else:
       return False 
        
  
    
      
    

if __name__=="__main__" and debug:
  '''
  player = Player('Player1', "New Player", 100, 500)
  seller = InteractObject('Seller', "Shop seller", 100, 500)
  player.add_money(250, seller)
  seller.add_money(250, player)
  print(player.name)
  player.objectName = "AxReal"
  print(player.name)
  player.say('Hi!', seller, ' [Sayed to {to.name}]')
  player.add_listen_exp('Hello!', 'Hi, {frm.name}!')
  player.say('Hello!', seller)
  print("Player money: "+str(player.money))
  print("Player health: "+str(player.health))
  '''
  
  print("""
  Let's try it out!
  Create new player:
   <player = Player('Name', 'Description', health, money, listen_dictonary, level_dictonary)>
   
  All arguments have default params
  Let's create player with name MyPlayer:
   >>>player = Player('MyPlayer')
   
  """)
  player = Player('MyPlayer')
  print("""
  It's OK!
  Create new Interactive Object: 
   <man = InteractObject('Name', 'Description', health, money, listen_dictonary, can_say, score_to_add)>
   
  Let's go:
    >>>man = InteractObject('Some man')
  
  """)
  man = InteractObject('Some man')
  print("""
  OK!
  Now, we can add some money to our Player and to InteractObject:
   <some.add_money(money, from, message, message2, error_message)>
   
  Go:
    >>>player.add_money(500)
    >>>man.add_money(300, None, "{self.name} has found some money: {money}")
   
  ---Output---
  """)
 # player.kill()
  player.add_money(500)
  man.add_money(300, None, "{self.name} has found some money: {money}")
  print("""
  -----------
  
  Now, let's add some listen rules to our man:
    >>>man.add_listen_exp('Can I buy something from you?', 'Yes, you can buy some apple for 150 money')
    
  Now MyPlayer can say to Some man:
    >>>player.say('Can I buy something from you?', man)
    
  ---Output---
  """)
  man.add_listen_exp('Can I buy something from you?', 'Yes, you can buy some apple for 150 money')
  player.say('Can I buy something from you?', man)
  
  print("""
  -----------
  
  Good!
  Let's give 150 money to Some man:
    >>>man.add_money(150, player)
    
  (Method add_money with 2-nd argument as InteractObject or Player can add money to object and deduct this money from other object)
  
  ---Output---
  """)
  man.add_money(150, player)
  print("""
  -----------
  
  Now, let's print balance of Some man and MyPlayer:
    >>>print(player.name+" balance: "+str(player.money))
    >>>print(man.name+" balance: "+str(man.money))
    
  ---Output---  
  """)
  #player.addScore(500)
  print(player.name+" balance: "+str(player.money))
  print(man.name+" balance: "+str(man.money))
  print("""
  -----------
  
  Congratulations!!!
  ------------------
  It's a demonstration of my game engine. Please, leave a like and comment!
  Good Luck!
  """)
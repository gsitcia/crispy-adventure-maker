# Directions: North is 1, South is 2, East is 3, West is 4
# Defaults: Save, Load, 
conf = open('config', 'r');
conf = conf.read();
lconf = [''];
for i in range(len(conf)):
  if conf[i] != '\n':
    lconf[-1] = lconf[-1] + conf[i];
  else:
    lconf.append('');
conf = [];
for i in lconf:
  if i != '' and i[:2] != '//':
    conf.append(i);
defaults = [1,2,3,4];

rooms = {'f': {'d':'It is an empty room'}};
objects = {};
usages = {};
sel = {'room':'f', 'inventory':[]};

parsing = 1;

def words(s):
    s += ' ';
    l = [];
    z = '';
    for i in s:
      z += i;
      if i == ' ':
        l.append(z[:-1]);
        z = '';
    return(l);

def direct(d):
  if d == 'North' or d == 'north' or d == 'n':
    return 1;
  if d == 'South' or d == 'south' or d == 's':
    return 3;
  if d == 'West' or d == 'west' or d == 'e':
    return 2;
  if d == 'East' or d == 'east' or d == 'w':
    return 4;

def adrect(d):
  if d == 'n':
    return 'North';
  if d == 's':
    return 'South';
  if d == 'e':
    return 'East';
  if d == 'w':
    return 'West';
  
def save(p):
  print('save');

def load():
  print('load');

def walk(d):
  if d in rooms[sel['room']]:
    sel['room'] = rooms[sel['room']][d];
  
def examine(o):
  if o in objects:
    print(objects[o]['d']);
  
def use():
  print('use');
  
def look():
  print(rooms[sel['room']]['d']);
  q = '';
  for i in rooms[sel['room']]:
    if i != 'd':
      q += adrect(i) + ' ';
  if q == '':
    q = 'nowhere ';
  print('\nThere are exits '+q[:-1]);
  
def make(l):
  if l == []:
    print('Parsing Error');
  elif l[0] == 'room':
    rooms[l[1]] = {'d':input('Input Description: ')}
  elif l[0] == 'object':
    objects[l[1]] = {'d':input('Input Description: ')}
    if len(l) >= 3:
      objects[l[1]]['l'] = l[2]
    else:
      objects[l[1]]['l'] = sel['room'];
    if len(l) == 4:
      objects[l[1]]['h'] = l[3];
    else:
      objects[l[1]]['h'] = 0;
  elif l[0] == 'door':
    rooms[l[1]][l[2]] = l[3];
    rooms[l[3]][l[4]] = l[1];

def halp():
  print('help');

def lest(n):
  if n == 'rooms':
    for i in rooms.keys():
      print(i);
  if n == 'objects':
    for i in objects.keys():
      print(i);

def info(l = 'n'):
  if l == []:
    print('Parsing Error');
    return 0;
  elif l[0] == 'room':
    for i in rooms[l[1]]:
      print(i+': '+rooms[l[1]][i]);
  elif l[0] == 'object':
    for i in objects[l[1]]:
      print(i+': '+objects[l[1]][i]);
  elif l[0] == 'self':
    for i in sel:
      if i != 'inventory':
        print(i+': '+sel[i]);
      
def remove(l):
  if l == []:
    print('Parsing Error');
  elif l[0] == 'room':
    if l[1] in rooms.keys():
      del rooms[l[1]];
      print('Deleted');
    else:
      print('Error, that room does not exist');
  elif l[0] == 'object':
    if l[1] in objects.keys():
      del objects[l[1]];
      print('Deleted');
    else:
      print('Error, that object does not exist');
  elif l[0] == 'door':
    if l[1] in rooms[l[2]].values():
      q = [i for i in rooms[l[2]].values()];
      g = [i for i in rooms[l[2]].keys()];
      del rooms[g[q.index(l[1])]];
    if l[2] in rooms[l[1]].values():
      q = [i for i in rooms[l[1]].values()];
      g = [i for i in rooms[l[1]].keys()];
      del rooms[g[q.index(l[2])]];

def edit(l):
  if l == []:
    print('Parsing Error');
  elif l[0] == 'room':
    rooms[l[1]][l[2]] = l[3];
  elif l[0] == 'object':
    objects[l[1]][l[2]] = l[3];
  elif l[0] == 'self':
    sel[l[1]] = l[2];
    
def inv():
  for i in sel['inventory']:
    print(i);
  
def exit():
  q = input('Are you sure? ');
  if q == 'yes' or q == 'y':
    global parsing;
    parsing = 0;

def parse():
  i = input('>>> ');
  # input can start with "save" "load" "walk" "examine" "use" "look" "make" "help" "list" "remove" "exit" 
  i = words(i);
  if i[0] == 'save':
    save(i[1]);
  elif i[0] == 'load':
    load(i[1]);
  elif i[0] == 'walk':
    walk(i[1]);
  elif i[0] == 'examine':
    examine(i[1]);
  elif i[0] == 'look':
    look();
  elif i[0] == 'make':
    make(i[1:]);
  elif i[0] == 'help':
    halp();
  elif i[0] == 'list':
    lest(i[1]);
  elif i[0] == 'exit':
    exit();
  elif i[0] == 'remove':
    remove(i[1:]);
  elif i[0] == 'edit':
    edit(i[1:]);
  elif i[0] == 'info':
    info(i[1:]);
  elif i[0] == 'inventory':
    inv();
  else:
    print('Parsing Error');
  return 0;

while parsing == 1:
  parse();

rooms = {'f': {'@d':'It is an empty room'}};
objects = {};
usages = {};
sel = {'@room':'f', '@inventory':[]};

parsing = 1;

def concat(l):
  z = '';
  for i in l:
    z += i + ' ';
  return(z[:-1]);

def sant(l):
  q = [];
  for i in l:
    if i != '':
      q.append(i);
  return(q);

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

def atz(l):
  q = {'#delete':''};
  b = '#delete'
  for i in l:
    if i[0] == '@':
      q[b] = q[b][:-1];
      q[i] = '';
      b = i;
    else:
      q[b] += i + ' ';
  q[b] = q[b][:-1];
  del q['#delete'];
  return q;
  
def direct(d):
  if d == 'North' or d == 'north' or d == 'n':
    return '@n';
  if d == 'South' or d == 'south' or d == 's':
    return '@s';
  if d == 'West' or d == 'west' or d == 'e':
    return '@w';
  if d == 'East' or d == 'east' or d == 'w':
    return '@e';

def adrect(d):
  if d == '@n':
    return 'North';
  if d == '@s':
    return 'South';
  if d == '@e':
    return 'East';
  if d == '@w':
    return 'West';
  
def save(p):
  fil = open(p,'w');
  stuff = 'rooms' + concat(['\n' + i + ' ' + concat([concat([j,rooms[i][j]]) for j in rooms[i]]) for i in rooms]) + '\nobjects' + concat(['\n' + i + ' ' + concat([concat([j,objects[i][j]]) for j in objects[i]]) for i in objects]) + '\nself' + '\n@room\n' + sel['@room'] + '\n@inventory' + concat(sel['@inventory']) + '\n';
  fil.write(stuff);

def load(p):
  fil = open(p, 'r');
  raw = fil.read();
  z = '';
  div1 = [];
  for i in raw:
    if i != '\n':
      z += i;
    else:
      div1.append(z[0:]);
      z = '';
  rom = [];
  obj = [];
  sej = [];
  div = [];
  for i in div1:
    if i != '':
      div.append(i);
  flag = 'wait';
  for i in div:
    if flag == 'rooms':
      if i != 'objects':
        rom.append(i);
      else:
        flag = i;
    elif flag == 'objects':
      if i != 'self':
        obj.append(i);
      else:
        flag = i;
    elif flag == 'self':
      sej.append(i);
    elif flag == 'wait':
      if i == 'rooms':
        flag = i;
  for i in range(len(rom)):
    rom[i] = words(rom[i]);
  for i in range(len(obj)):
    obj[i] = words(obj[i]);
  global rooms;
  global objects;
  global sel;
  sel = {};
  rooms = {};
  objects = {};
  for i in range(len(rom)):
    rom[i] = sant(rom[i]);
  for i in range(len(obj)):
    obj[i] = sant(obj[i]);
  for i in rom:
    rooms[i[0]] = atz(i);
  for i in obj:
    objects[i[0]] = atz(i);
  sel = atz(sej);
  sel['@inventory'] = words(sel['@inventory']);

def walk(d):
  if direct(d) in rooms[sel['@room']]:
    sel['@room'] = rooms[sel['@room']][direct(d)];
  
def examine(o):
  if o in objects:
    print(objects[o]['@d']);
  
def use():
  print('use');
  
def look():
  print(rooms[sel['@room']]['@d']);
  q = '';
  for i in rooms[sel['@room']]:
    if i != '@d':
      q += adrect(i) + ' ';
  if q == '':
    q = 'nowhere ';
  for i in objects:
    if objects[i]['@room'] == sel['@room']:
      print(i);
  print('\nThere are exits '+q[:-1]);
  
def make(l):
  if len(l) < 2:
    print('Parsing Error');
  elif l[0] == 'room':
    rooms[l[1]] = {'@d':input('Input Description: ')}
  elif l[0] == 'object':
    objects[l[1]] = {'@d':input('Input Description: ')}
    if len(l) >= 3:
      objects[l[1]]['@room'] = l[2]
    else:
      objects[l[1]]['@room'] = sel['@room'];
    if len(l) == 4:
      objects[l[1]]['@holdable'] = l[3];
    else:
      objects[l[1]]['@holdable'] = '1';
  elif l[0] == 'door':
    rooms[l[1]]['@'+l[2]] = l[3];
    rooms[l[3]]['@'+l[4]] = l[1];

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
      if i != '@inventory':
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
  for i in sel['@inventory']:
    print(i);
  
def exit():
  q = input('Are you sure? ');
  if q == 'yes' or q == 'y':
    global parsing;
    parsing = 0;

def take(o):
  if o in objects:
    if objects[o]['@room'] == sel['@room'] and objects[o]['@holdable'] == '1':
      objects[o]['@room'] == 'inventory';
      sel['@inventory'].append(o);

def drop(o):
  if o in sel['@inventory']:
    del sel['@inventory'][o];
    objects[o]['@room'] = sel['@room'];
      
def parse():
  i = input('>>> ');
  # input can start with "save" "load" "walk" "examine" "use" "look" "make" "help" "list" "remove" "exit" 
  i = words(i);
  if len(i) == 1:
    i.append('');
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
  elif i[0] == 'take':
    take(i[1]);
  elif i[0] == 'drop':
    drop(i[1]);
  elif i[0] == 'stuff':
    print(rooms);
    print(objects);
    print(sel);
  else:
    print('Parsing Error');
  return 0;

while parsing == 1:
  parse();

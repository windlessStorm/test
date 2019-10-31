import random
import win32api
import time

max_x = win32api.GetSystemMetrics(0)
max_y = win32api.GetSystemMetrics(1)

def elastic_potential_energy(displacement, spring_constant):
  epe = 0.5 * spring_constant * (displacement**2)
  return epe

def elastic_force(displacement, spring_constant):
  return (-spring_constant) * displacement

def acceleration(mass, force):
  a = force/mass
  return a

def get_velocity(initial_velocity, acceleration, t):
  return initial_velocity + (acceleration * t)

def get_displacement(initial_velocity, acceleration, t):
  return (initial_velocity * t) + (0.5 * acceleration * (t**2))

def spring_cursor(displacement=400, spring_constant=40, mass=10, dt=0.01, dampening_coefficient=2):
  init_pos = win32api.GetCursorPos()
  cur_displacement = displacement
  new_pos_x = init_pos[0] + cur_displacement
  new_pos_y = init_pos[1]
  win32api.SetCursorPos((new_pos_x, new_pos_y))
  current_velocity = 0
  # release the springg
  while(True):
    time.sleep(dt)
    # after delta time t=0.001
    cur_force = elastic_force(cur_displacement, spring_constant) - (dampening_coefficient*current_velocity)
    cur_acceleration = cur_force/mass
    initial_velocity = current_velocity
    delta_displacement = get_displacement(initial_velocity, cur_acceleration, dt)
    cur_displacement += delta_displacement
    current_velocity = get_velocity(initial_velocity, cur_acceleration, dt)
    new_pos_x = init_pos[0] + cur_displacement
    print 'x={}, dd={}, cd = {}, a={}, f={}, v={}'.format(
      new_pos_x, delta_displacement, cur_displacement, cur_acceleration, cur_force, current_velocity)
    win32api.SetCursorPos((int(new_pos_x), new_pos_y))


def bounce(cor=0.9):
  init_pos = win32api.GetCursorPos()
  dt=0.1
  current_velocity = 0
  cur_displacement = 0
  cur_acceleration = 9.8
  new_x = init_pos[0]
  new_y = init_pos[1]
  while( True):
    time.sleep(0.01)
    initial_velocity = current_velocity
    delta_displacement = get_displacement(initial_velocity, cur_acceleration, dt)
    cur_displacement += delta_displacement
    current_velocity = get_velocity(initial_velocity, cur_acceleration, dt)
    new_y = init_pos[1] + cur_displacement

    if (int(new_y) > max_y): # collision with ground
      current_velocity *= -1
      current_velocity *= cor
      new_y = max_y
    if (int(new_y == max_y) and int(current_velocity) == 0):
      # new_y = init_pos[1]
      return
      # current_velocity = -100
      # cur_acceleration = 9.8

    print 'maxy= {}, y={}, v={},dd={},cd={}'.format(max_y, new_y,current_velocity,delta_displacement,cur_displacement)
    win32api.SetCursorPos((new_x, int(new_y)))
  

def jumpjump():
  time.sleep(1)
  randx = random.randint(0, max_x)
  randy = random.randint(0, max_y)
  win32api.SetCursorPos((randx, randy))

def dhinchak(effect=1):
  # time.sleep(0.1)
  while(True):
    cur_pos = win32api.GetCursorPos()
    new_pos_x, new_pos_y = cur_pos
    new_pos_x = cur_pos[0] + random.randint(-effect, effect)
    new_pos_y = cur_pos[1] + random.randint(-effect, effect)

    if new_pos_x >= max_x:
      new_pos_x -= effect
    if new_pos_x <= 0:
      new_pos_x += effect
    if new_pos_y >= max_y:
      new_pos_y -= effect
    if new_pos_y <= 0:
      new_pos_y += effect

    win32api.SetCursorPos((new_pos_x, new_pos_y))

def smooth_move(dest, slow=1):
  new_pos_x, new_pos_y = win32api.GetCursorPos()
  while(new_pos_x != dest[0] or new_pos_y != dest[1]):
    if dest[0] > new_pos_x:
      new_pos_x += 1
    elif dest[0] < new_pos_x:
      new_pos_x -= 1
    if dest[1] > new_pos_y:
      new_pos_y += 1
    elif dest[1] < new_pos_y:
      new_pos_y -= 1
    time.sleep(0.001*slow)
    win32api.SetCursorPos((new_pos_x, new_pos_y))

def eucladian_dist(pointa, pointb):
  import math
  return math.sqrt((pointa[0]-pointb[0])**2 + (pointa[1]-pointb[1])**2 )

def ilovecorners():
  while(True):
    time.sleep(1)
    cur_pos = win32api.GetCursorPos()
    topldiff = int(eucladian_dist(cur_pos, (0,0)))
    toprdiff = int(eucladian_dist(cur_pos, (max_x,0)))
    botldiff = int(eucladian_dist(cur_pos, (0,max_y)))
    botrtdiff = int(eucladian_dist(cur_pos, (max_x,max_y)))

    lowest_diff = min(topldiff, toprdiff, botldiff, botrtdiff)

    if lowest_diff == topldiff:
      smooth_move((0,0))
    elif lowest_diff == toprdiff:
      smooth_move((max_x,0))
    elif lowest_diff == botldiff:
      smooth_move((0,max_y))
    elif lowest_diff == botrtdiff:
      smooth_move((max_x,max_y))
  
def ilovewalls():
  while(True):
    time.sleep(1)
    cur_pos = win32api.GetCursorPos()
    updiff = cur_pos[1]
    downdiff = max_y - cur_pos[1]
    leftdiff = cur_pos[0]
    rightdiff = max_x - cur_pos[0]

    lowest_diff = min(updiff, downdiff, leftdiff, rightdiff)

    if lowest_diff == updiff:
      smooth_move((cur_pos[0],0))
    elif lowest_diff == downdiff:
      smooth_move((cur_pos[0], max_y))
    elif lowest_diff == leftdiff:
      smooth_move((0, cur_pos[1]))
    elif lowest_diff == rightdiff:
      smooth_move((max_x, cur_pos[1]))
  
def circle_eq_get_y(x, radius, center_x, center_y):
  import math
  y = math.sqrt( radius**2 - ((x - center_x)**2 ) ) + center_y
  return y

def merrygoround(radius=max_y/3):
  cur_pos = win32api.GetCursorPos()
  center_x, center_y = cur_pos
  if max_x <= center_x + radius:
    center_x -= radius
  if 0 >= center_x - radius:
    center_x += radius
  if 0 >= center_y - radius:
    center_y += radius
  if max_y <= center_y + radius:
    center_y -= radius

  new_x = center_x
  new_y = center_y + radius
  rotate = 1

  while(True):
    # time.sleep(1)
    print new_x, new_y
    smooth_move((new_x, new_y))
    if new_y < center_y:
      rotate = -1
    elif new_y > center_y:
      rotate = 1
    else:
      rotate = rotate * -1
    new_x += rotate
    new_y = int(circle_eq_get_y(new_x, radius, center_x, center_y))
    if rotate < 0:
      new_y = (2 * center_y) - new_y




# ilovewalls()

# ilovecorners()

# merrygoround(200)

# dhinchak()

# spring_cursor(displacement=400, spring_constant=40, mass=10, dt=0.01, dampening_coefficient=2)
# spring_cursor(600, 60, 10, 0.01, 2)

bounce(0.7)
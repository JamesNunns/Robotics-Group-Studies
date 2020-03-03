#!/usr/bin/env python
# Imports
import sys
import math
import time
import pyglet
import pymunk
import random
from pymunk.pyglet_util import DrawOptions
import numpy as np
import matplotlib.pyplot as plt

options = DrawOptions()  # Initialise DrawOptions for Pymunk

# Physical dimensions of swing
rod1_length = 400
rod2_length = 50
rod3_length = 20
seat_length = 30
torso_length = 100
legs_length = 60

# Q-Learning parameters
alpha = 0.3
gamma = 0.9
epsilon = 0.1

episodes = 5000


#####################
### PYMUNK
#####################


class Angle:
    '''
    The 'Angle' class which converts an angle in degrees to
    absolute world positions for the swing simulation.
    '''
    def __init__(self, theta: int = 0):
        self._theta = theta * math.pi / 180

        # Relative dimensions
        self.rod1 = (-rod1_length * math.sin(self._theta),
                     -rod1_length * math.cos(self._theta))
        self.rod2 = (-rod2_length * math.sin(self._theta),
                     -rod2_length * math.cos(self._theta))
        self.rod3 = (-rod3_length * math.sin(self._theta),
                     -rod3_length * math.cos(self._theta))
        self.seat = ((-seat_length * math.cos(self._theta),
                      seat_length * math.sin(self._theta)),
                     (seat_length * math.cos(self._theta),
                      -seat_length * math.sin(self._theta)))
        self.feet = (-legs_length * math.cos(self._theta),
                     legs_length * math.sin(self._theta))

        # Absolute dimensions
        self.point1 = (600 - rod1_length * math.sin(self._theta),
                       695 - rod1_length * math.cos(self._theta))
        self.point2 = (self.point1[0] - rod2_length * math.sin(self._theta),
                       self.point1[1] - rod2_length * math.cos(self._theta))
        self.point3 = (self.point2[0] - rod3_length * math.sin(self._theta),
                       self.point2[1] - rod3_length * math.cos(self._theta))
        self.point4 = (self.point3[0] - seat_length * math.sin(self._theta),
                       self.point3[1] - seat_length * math.cos(self._theta))
        self.point5 = (self.point4[0] - legs_length * math.sin(self._theta),
                       self.point4[1] - legs_length * math.cos(self._theta))


class Swing:
    '''
    The 'Swing' class which generates a swing in a pymunk space
    at a given angle.
    '''
    def __init__(self, space: pymunk.Space, theta: int = 0):
        self.space = space

        # Define initial angle
        angle = Angle(theta)

        # Define bodies
        self.top = pymunk.Body(50, 10000, pymunk.Body.STATIC)
        self.bottom = pymunk.Body(50, 10000, pymunk.Body.STATIC)
        self.rod1 = pymunk.Body(5, 10000)
        self.rod2 = pymunk.Body(5, 10000)
        self.rod3 = pymunk.Body(5, 10000)
        self.seat = pymunk.Body(10, 10000)
        self.torso = pymunk.Body(10, 10000)
        self.legs = pymunk.Body(10, 10000)
        self.head = pymunk.Body(5, 10000)

        # Create shapes
        self.top_shape = pymunk.Poly.create_box(self.top, size=(1200, 50))
        self.bottom_shape = pymunk.Poly.create_box(self.bottom, size=(1200, 50))
        self.rod1_shape = pymunk.Segment(self.rod1, (0, 0), angle.rod1, radius=3)
        self.rod2_shape = pymunk.Segment(self.rod2, (0, 0), angle.rod2, radius=3)
        self.rod3_shape = pymunk.Segment(self.rod3, (0, 0), angle.rod3, radius=3)
        self.seat_shape = pymunk.Segment(self.seat, angle.seat[0], angle.seat[1], radius=5)
        self.torso_shape = pymunk.Poly.create_box(self.torso, size=(10, torso_length))
        self.legs_shape = pymunk.Poly.create_box(self.legs, size=(10, legs_length))
        self.head_shape = pymunk.Circle(self.head, radius=20)

        # Set layer of shapes (disables collisions between bodies)
        self.rod1_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        self.rod2_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        self.rod3_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        self.seat_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        self.torso_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        self.legs_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        self.head_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)

        # Set positions of bodies
        self.top.position = (600, 720)
        self.bottom.position = (600, 0)
        self.rod1.position = (600, 695)
        self.rod2.position = angle.point1
        self.rod3.position = angle.point2
        self.seat.position = angle.point4
        self.torso.position = (angle.point4[0] + angle.seat[1][0] +
                               (torso_length / 2) * math.sin(angle._theta), angle.point4[1] +
                               angle.seat[1][1] + (torso_length / 2) * math.cos(angle._theta))
        self.torso._set_angle(-angle._theta)
        self.legs.position = (angle.point4[0] + angle.seat[0][0] -
                              (legs_length / 2) * math.sin(angle._theta), angle.point4[1] +
                              angle.seat[0][1] - (legs_length / 2) * math.cos(angle._theta))
        self.legs._set_angle(-angle._theta)
        self.head.position = (angle.point4[0] + angle.seat[1][0] +
                              (torso_length - 10) * math.sin(angle._theta), angle.point4[1] +
                              angle.seat[1][1] + (torso_length - 10) * math.cos(angle._theta))

        # Create pivot joints for bodies
        self.pivot1 = pymunk.PivotJoint(self.top, self.rod1, (600, 695))
        self.pivot2 = pymunk.PivotJoint(self.rod1, self.rod2, angle.point1)
        self.pivot3 = pymunk.PivotJoint(self.rod2, self.rod3, angle.point2)
        self.pivot4 = pymunk.PivotJoint(self.rod3, self.seat, angle.point4)
        self.pivot5 = pymunk.PinJoint(self.rod3, self.seat, anchor_a=angle.rod3, anchor_b=angle.seat[0])
        self.pivot6 = pymunk.PinJoint(self.rod3, self.seat, anchor_a=angle.rod3, anchor_b=angle.seat[1])
        self.pivot7 = pymunk.PivotJoint(self.torso, self.seat, (angle.point4[0] + angle.seat[1][0], angle.point4[1] + angle.seat[1][1]))
        self.pivot8 = pymunk.PivotJoint(self.seat, self.legs, (angle.point4[0] + angle.seat[0][0], angle.point4[1] + angle.seat[0][1]))
        self.pivot9 = pymunk.PivotJoint(self.head, self.torso, self.head.position)
        self.gear1 = pymunk.GearJoint(self.torso, self.seat, angle._theta, 1.0)
        self.gear2 = pymunk.GearJoint(self.seat, self.legs, -angle._theta, 1.0)

        # Prevent pivots from exerting infinite force
        self.pivot1.max_force = 1000000
        self.pivot2.max_force = 1000000
        self.pivot3.max_force = 1000000
        self.pivot4.max_force = 1000000

        # Add damping (not yet working)
        # damping1 = pymunk.DampedSpring(self.top, self.rod1, anchor_a=(-600,-25),
        #                                anchor_b=(0,-rod1_length / 2),
        #                                rest_length=100, stiffness=5, damping=3)
        # damping2 = pymunk.DampedSpring(self.top, self.rod1, anchor_a=(600,-25),
        #                                anchor_b=(0,-rod1_length / 2),
        #                                rest_length=100, stiffness=5, damping=3)

        # Disable collisions between rods
        self.pivot1.collide_bodies = False
        self.pivot2.collide_bodies = False
        self.pivot3.collide_bodies = False
        self.pivot4.collide_bodies = False
        self.pivot7.collide_bodies = False
        self.pivot8.collide_bodies = False
        self.pivot9.collide_bodies = False

        # Add bodies and pivots to space
        self.space.add(self.top, self.top_shape, self.bottom, self.bottom_shape,
                       self.rod1, self.rod1_shape, self.rod2, self.rod2_shape,
                       self.rod3, self.rod3_shape, self.seat, self.seat_shape,
                       self.torso, self.torso_shape, self.legs, self.legs_shape,
                       self.head, self.head_shape, self.pivot1, self.pivot2,
                       self.pivot3, self.pivot4, self.pivot5, self.pivot6,
                       self.pivot7, self.pivot8, self.pivot9, self.gear1,
                       self.gear2)

    def delete(self):
        self.space.remove(self.top, self.top_shape, self.bottom, self.bottom_shape,
                          self.rod1, self.rod1_shape, self.rod2, self.rod2_shape,
                          self.rod3, self.rod3_shape, self.seat, self.seat_shape,
                          self.torso, self.torso_shape, self.legs, self.legs_shape,
                          self.head, self.head_shape, self.pivot1, self.pivot2,
                          self.pivot3, self.pivot4, self.pivot5, self.pivot6,
                          self.pivot7, self.pivot8, self.pivot9, self.gear1,
                          self.gear2)


#####################
#### PYGLET
#####################

class Window(pyglet.window.Window):
    '''
    The 'Window' class which represents a pyglet window for our swing
    simulation.
    '''
    def __init__(self, width: int = 1200, height: int = 720,
                 title: str = "Simulation", timeout: int = -1,
                 theta: int = 30, q_table: np.array = np.zeros((21,5))):
        '''
        Initialise the Pyglet window / create Pymunk space / generate
        swing and robot.
        '''
        super().__init__(width, height, title, resizable=False)  # Init Pyglet window

        self.space = pymunk.Space()  # Init Pymunk space for 2D physics engine
        self.space.gravity = 0, -1000  # Set gravity of space

        # Class attributes
        self._width = width
        self._height = height
        self._title = title
        self._timeout = timeout
        self._theta = theta
        self.q_table = q_table

        self.episode = 0
        self.movements = 0
        self.stills = 0
        self.randoms = 0
        self.total = 0
        self.reset()  # Start simulation

    def reset(self):
        '''
        Reset swing.
        '''
        try:
            np.savetxt('q_table.csv', self.q_table, delimiter=',')  # Save updated q_table
            plt.matshow(self.q_table)  # Generate image from matrix of q_table
            plt.savefig('q_table.png', bbox_inches='tight', dpi=56)  # Save image for displaying on Pyglet window
            plt.figure()
            plt.plot(np.linspace(0, self.time, len(self.angle_history)), self.angle_history)
            plt.savefig('history.png', bbox_inches='tight', dpi=56)
            plt.close('all')
        except:
            pass

        # Variables
        self.episode += 1
        self.velocity = 0
        self.angle = self._theta  # Current angle
        self.angle_history = [self.angle, self.angle]  # Angle history (for plotting over time)
        self.time = 0  # Simulation time

        try: self.swing.delete()
        except: pass
        self.swing = Swing(self.space, self._theta)  # Generate the swing/robot
        self.state = 0 # Current state of the system
        self.image = pyglet.image.load('q_table.png') # Initialise Q-table image
        try: self.history = pyglet.image.load('history.png')
        except: self.history = None

    def on_mouse_press(self, x, y, button, modifiers):
        '''
        Event for mouse press inside the Pyglet window.
        '''
        b = pymunk.Body(10, 10)  # Declare a black body
        b_shape = pymunk.Circle(b, 10)  # Create a circle shape
        b.position = x, y  # Set body position to coordinates of mouse press
        self.space.add(b, b_shape)  # Add body / cirle shape to space
        print(x, y)  # Print coordinates of mouse press

    def on_draw(self):
        '''
        Method called each time the screen is drawn (i.e. each frame).
        '''
        self.clear()  # Clear screen
        self.space.debug_draw(options)  # Draw space objects (Pymunk bodies, shapes, pivots, gears etc.)
        episode = pyglet.text.Label("Episode " + str(self.episode),
                                 font_name='Helvetica',
                                 font_size=32, x=1050, y=650,
                                 anchor_x='center', anchor_y='center')  # Create label of current time
        episode.draw()  # Draw time label
        time = pyglet.text.Label(str(round(self.time, 1)) + "s",
                                 font_name='Helvetica',
                                 font_size=24, x=1050, y=600,
                                 anchor_x='center', anchor_y='center')  # Create label of current time
        time.draw()  # Draw time label
        angle = pyglet.text.Label(str(round(self.angle, 1)) + "°",
                                  font_name='Helvetica',
                                  font_size=24, x=1050, y=560,
                                  anchor_x='center', anchor_y='center')  # Create label of current angle
        angle.draw()  # Draw angle label
        velocity = pyglet.text.Label(str(round(self.velocity, 1)) + "°/s",
                                 font_name='Helvetica',
                                 font_size=24, x=1050, y=520,
                                 anchor_x='center', anchor_y='center')  # Create label of current time
        velocity.draw()  # Draw time label
        state = pyglet.text.Label(str(round(self.state, 1)) + "",
                                 font_name='Helvetica',
                                 font_size=24, x=1050, y=480,
                                 anchor_x='center', anchor_y='center')  # Create label of current time
        state.draw()  # Draw time label
        q_s = pyglet.text.Label(str(self.movements) + "/" + str(self.stills) + "/" + str(self.randoms) + "/" + str(self.total),
                                 font_name='Helvetica',
                                 font_size=24, x=1050, y=440,
                                 anchor_x='center', anchor_y='center')  # Create label of current time
        q_s.draw()  # Draw time label
        state = pyglet.text.Label("Previous Episode:",
                            font_name='Helvetica',
                            font_size=16, x=1000, y=250,
                            anchor_x='center', anchor_y='center')  # Create label of current time
        state.draw()  # Draw time label
        self.image.blit(0, 0)  # Draw image
        try: self.history.blit(890, 0)  # Draw history
        except: pass

    def update(self, dt):
        '''
        Method called by Pyglet clock scheduler that updates
        the screen at the specified frame rate.
        '''
        self.space.step(dt)  # Move Pymunk space forward one time step
        self.time += dt  # Add time step to total time
        
        velocity = (self.angle_history[-2] - self.angle_history[-1]) * 60  # Calculate velocity of main rod

        if random.uniform(0, 1) < epsilon:
            self.randoms += 1
            action = random.randint(0, 4)  # Explore action space
        else:
            action = np.argmax(q_table[self.state])  # Exploit learned values

        self.total += 1

        next_state, reward = self.env_step(action, velocity)  # Determine new state

        # print(next_state, reward)

        old_value = self.q_table[self.state, action]  # Get old q_table value
        next_max = np.max(self.q_table[next_state])  # Find next max q_table values
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)  # Use Q-learning formula to calculateh how to change old values
        q_table[self.state, action] = new_value  # Append new value to q_table

        self.state = next_state  # Update current state

        self.angle_history.append(self.swing.rod1._get_angle() * (180 / math.pi) - self._theta)  # Add angle to angle history
        self.angle = int(self.swing.rod1._get_angle() * (180 / math.pi) - self._theta)  # Set current angle correctly
        self.velocity = velocity  # Save current velocity

        if self.time > self._timeout and not self._timeout == -1: self.reset()  # Exit window if time exceeds timeout

    def env_step(self, action: int, velocity: float):
        '''
        Run one step in the Q-learning algorithm.
        '''
        if action == 0: self.swing.gear2._set_phase(-self._theta * math.pi / 180 - 1.2) # Extend legs
        elif action == 1: self.swing.gear2._set_phase(-self._theta * math.pi / 180 + 0.8) # Retract legs
        elif action == 2: self.swing.gear1._set_phase(self._theta * math.pi / 180 - 0.2) # Extend torso
        elif action == 3: self.swing.gear1._set_phase(self._theta * math.pi / 180 + 0.6) # Retract torso

        try: angle = int(self.swing.rod1._get_angle() * (180 / math.pi) - self._theta) # Calculate current rod angle
        except: angle = -90 # If angle is outside of bounds

        if angle > 90: angle = 90 # If above 90, set to 90
        if angle < -90: angle = -90 # If below 90, set to -90

        if self.swing.pivot3.impulse > 12000 and self.time > 5: # If robot pulls too hard on rod then add a penalty
            penalty = self.swing.pivot3.impulse # Set penalty to the impulse exerted on the rod
            print("Penalty given: " + str(round(penalty, 1)))
            self.time = self._timeout
        elif action == 4: # If action is to do nothing...
            penalty = 0 # ...no penalty
            self.stills += 1
        else:
            penalty = 50
            self.movements += 1
        
        state = int((round(self.velocity, -1) / 10) + 10)
        if state > 20: state = 20  # Put cap on
        if state < 0: state = 0  # velocities

        if (self.velocity < 0 and velocity > 0) or (self.velocity > 0 and velocity < 0): # If velocity has changed sign (aka at apex), determine reward
            reward = angle**2
        else:
            reward = 0

        return state, reward - penalty  # Return (state, reward)

#####################
#### MAIN
#####################


if __name__ == "__main__":
    try:
        try:
            q_table = np.loadtxt('q_table.csv', delimiter=',') # Get saved q_table
        except:
            np.savetxt('q_table.csv', np.zeros((21,5)), delimiter=',') # For resetting q_table
            q_table = np.loadtxt('q_table.csv', delimiter=',') # Get saved q_table

        window = Window(theta=0, timeout=500, q_table=q_table)  # Generate window from q_table
        pyglet.clock.schedule_interval(window.update, 1.0/60)  # Schedule update method to run 60 times a second (FPS of window)
        pyglet.app.run()  # Run pyglet window

    except KeyboardInterrupt:  # Ctrl-C pressed
        print("Simulation closing...")
        sys.exit()  # Exit program
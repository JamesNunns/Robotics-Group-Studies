#!/usr/bin/env python
# Imports
import math
import time
import pyglet
import pymunk
import random
from pymunk.pyglet_util import DrawOptions
import numpy as np
import matplotlib.pyplot as plt

options = DrawOptions()  # Initialise DrawOptions for Pymunk
key = pyglet.window.key

# Physical dimensions of swing
rod1_length = 400
rod2_length = 50
rod3_length = 20
seat_length = 30
torso_length = 100
legs_length = 60

#####################
### PYMUNK
#####################

window = pyglet.window.Window(1200, 720, "Simulation", resizable=False)

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
    def __init__(self, space: pymunk.Space = pymunk.Space(), theta: int = 0):
        '''
        Initialise the pymunk space and angle and create swing / robot
        '''
        print("Generating Pymunk wrapper...", end=" ", flush=True)

        self.space = space
        self.space.gravity = 0, -1000  # Set gravity of space
        self.space.damping = 0.9
        self.theta = theta
        self.timeout = 500
        self.title = "Simulation"

        self.prev_obs = []
        self.model = None

        self.create()

        print("Done!")
    
    def create(self):
        '''
        Generate swing and robot and add to space.
        '''
        self.actions = [0, 0, 0, 0, 0]
        self.velocity = 0
        self.angle = 0
        self.time = 0
        
        # Define initial angle
        angle = Angle(self.theta)
        self.max_angle = 0

        # Define bodies
        self.top = pymunk.Body(50, 10000, pymunk.Body.STATIC)
        self.bottom = pymunk.Body(50, 10000, pymunk.Body.STATIC)
        self.rod1 = pymunk.Body(10, 10000)
        self.rod2 = pymunk.Body(10, 10000)
        self.rod3 = pymunk.Body(10, 10000)
        self.seat = pymunk.Body(15, 10000)
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
        # self.arms = pymunk.DampedSpring(self.torso, self.rod3, anchor_a=(0,0), anchor_b=(0,0), rest_length=25, stiffness=100, damping=0.5)
        self.gear1 = pymunk.RotaryLimitJoint(self.torso, self.seat, -0.1, 0.5)
        self.gear2 = pymunk.RotaryLimitJoint(self.seat, self.legs, -1.2, 0.9)

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
        '''
        Delete all bodies of the swing in the space.
        '''
        self.space.remove(self.top, self.top_shape, self.bottom, self.bottom_shape,
                          self.rod1, self.rod1_shape, self.rod2, self.rod2_shape,
                          self.rod3, self.rod3_shape, self.seat, self.seat_shape,
                          self.torso, self.torso_shape, self.legs, self.legs_shape,
                          self.head, self.head_shape, self.pivot1, self.pivot2,
                          self.pivot3, self.pivot4, self.pivot5, self.pivot6,
                          self.pivot7, self.pivot8, self.pivot9, self.gear1,
                          self.gear2)
    
    def reset(self):
        '''
        Reset the simulation.
        '''
        self.delete()
        self.create()
        return [self.angle, self.velocity]
    
    def step(self, action: int, dt: float = 1.0/60):
        '''
        Step one time period in the simulation.
        '''
        penalty = 100
        if action == 0:  # Legs out
            self.legs._set_torque(1000000)
        if action == 1:  # Legs in
            self.legs._set_torque(-1000000)
        if action == 2:  # Torso out
            self.torso._set_torque(1000000)
        if action == 3:  # Torso in
            self.torso._set_torque(-1000000)
        if action == 4: # Do nothing
            penalty = 0

        self.actions[action] += 1
        self.space.step(dt)
        self.time += dt

        velocity = self.velocity
        angle = self.angle
        self.velocity = ((self.rod1._get_angle() * (180 / math.pi) - self.theta) - self.angle) / dt
        self.angle = self.rod1._get_angle() * (180 / math.pi) - self.theta

        reward = 0
        if ((velocity < 0 and self.velocity > 0) or (velocity > 0 and self.velocity < 0)) or ((angle < 0 and self.angle > 0) or (angle > 0 and self.angle < 0)):
            reward = 2 * self.angle**2 + self.velocity**2

        observation = [self.angle, self.velocity]
        if self.time > self.timeout: done = True
        else: done = False

        if self.angle > self.max_angle: self.max_angle = self.angle

        # if self.pivot3.impulse > 8000:
        #     penalty = self.pivot3.impulse
        # else:
        #     penalty = 50

        return (observation, reward - penalty, done, {})
    
    def update(self, model):
        '''
        Update the simulation.
        '''
        if len(self.prev_obs) == 0:
            action = random.randrange(0,4)
        else:
            self.prev_obs = np.reshape(self.prev_obs, [1, 2])
            try:
                action = np.argmax(self.model.predict(self.prev_obs.reshape(-1, len(self.prev_obs)))[0])
            except:
                action = np.argmax(self.model.serial_activate(self.prev_obs))

        new_observation, reward, done, _ = self.step(action)
        self.prev_obs = np.array(new_observation)
        window.clear()
        self.space.debug_draw(options)

        if done: window.close()

        # Draw text
        title = pyglet.text.Label(self.title,
                                  font_name='Helvetica',
                                  font_size=32, x=1065, y=660,
                                  anchor_x='center', anchor_y='center')  # Create label of current angle
        title.draw()  # Draw angle label
        time = pyglet.text.Label("Time: " + str(round(self.time, 1)) + "s",
                                 font_name='Helvetica',
                                 font_size=24, x=990, y=610,
                                 anchor_x='left', anchor_y='center')  # Create label of current time
        time.draw()  # Draw time label
        angle = pyglet.text.Label("Angle: " + str(round(self.angle, 1)) + "°",
                                  font_name='Helvetica',
                                  font_size=24, x=990, y=580,
                                  anchor_x='left', anchor_y='center')  # Create label of current angle
        angle.draw()  # Draw angle label
        velocity = pyglet.text.Label("Velocity: " + str(round(self.velocity, 1)) + "°/s",
                                  font_name='Helvetica',
                                  font_size=24, x=950, y=550,
                                  anchor_x='left', anchor_y='center')  # Create label of current angle
        velocity.draw()  # Draw angle label

    def render(self, model, title: str = "Simulation", timeout: int = 20):
        '''
        Render environment based on neural network model.
        '''
        print("Rendering simulation...", end=" ", flush=True)

        self.model = model
        self.title = title
        self.timeout = timeout
        self.reset()
        pyglet.clock.schedule_interval(self.update, 1.0/60)
        pyglet.app.run()

        print("Done!\n")
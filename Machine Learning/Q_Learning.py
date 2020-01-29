#!/usr/bin/env python
import math
import time
import random
import pyglet
import pymunk
import sys
from pymunk.pyglet_util import DrawOptions
import numpy as np
import matplotlib.pyplot as plt

options = DrawOptions()

# Physical dimensions of swing
rod1_length = 400
rod2_length = 50
rod3_length = 20
seat_length = 30
legs_length = 30

force = 100000

# Q-Learning parameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

episodes = 5000

class Angle:
    '''
    The 'Angle' class which converts an angle in degrees to absolute world positions for the swing simulation.
    '''
    def __init__(self, theta: int = 0):
        self.theta = theta * math.pi / 180

        self.rod1 = (-rod1_length * math.sin(self.theta), -rod1_length * math.cos(self.theta))
        self.rod2 = (-rod2_length * math.sin(self.theta), -rod2_length * math.cos(self.theta))
        self.rod3 = (-rod3_length * math.sin(self.theta), -rod3_length * math.cos(self.theta))
        self.seat = ((-seat_length * math.cos(self.theta), seat_length * math.sin(self.theta)), (seat_length * math.cos(self.theta), -seat_length * math.sin(self.theta)))
        self.feet = (-legs_length * math.cos(self.theta), legs_length * math.sin(self.theta))

        self.point1 = (600 - rod1_length * math.sin(self.theta), 695 - rod1_length * math.cos(self.theta))
        self.point2 = (self.point1[0] - rod2_length * math.sin(self.theta), self.point1[1] - rod2_length * math.cos(self.theta))
        self.point3 = (self.point2[0] - rod3_length * math.sin(self.theta), self.point2[1] - rod3_length * math.cos(self.theta))
        self.point4 = (self.point3[0] - seat_length * math.sin(self.theta), self.point3[1] - seat_length * math.cos(self.theta))
        self.point5 = (self.point4[0] - legs_length * math.sin(self.theta), self.point4[1] - legs_length * math.cos(self.theta))

class Swing:
    '''
    The 'Swing' class which generates a swing in a pymunk space at a given angle.
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
        self.torso = pymunk.Body(20, 10000)
        self.legs = pymunk.Body(20, 10000)
        self.head = pymunk.Body(10, 10000)

        # Create shapes
        top_shape = pymunk.Poly.create_box(self.top, size=(1200,50))
        bottom_shape = pymunk.Poly.create_box(self.bottom, size=(1200,50))
        rod1_shape = pymunk.Segment(self.rod1, (0,0), angle.rod1, radius=3)
        rod2_shape = pymunk.Segment(self.rod2, (0,0), angle.rod2, radius=3)
        rod3_shape = pymunk.Segment(self.rod3, (0,0), angle.rod3, radius=3)
        seat_shape = pymunk.Segment(self.seat, angle.seat[0], angle.seat[1], radius=5)
        torso_shape = pymunk.Poly.create_box(self.torso, size=(10,100))
        legs_shape = pymunk.Poly.create_box(self.legs, size=(10,50))
        head_shape = pymunk.Circle(self.head, radius=20)

        # Set layer of shapes
        rod1_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        rod2_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        rod3_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        seat_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        torso_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)
        legs_shape.filter = pymunk.ShapeFilter(categories=0b100, mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b100)

        # Set positions of bodies
        self.top.position = (600, 720)
        self.bottom.position = (600, 0)
        self.rod1.position = (600, 695)
        self.rod2.position = angle.point1
        self.rod3.position = angle.point2
        self.seat.position = angle.point4
        self.torso.position = (angle.point4[0] + angle.seat[1][0] + 50 * math.sin(angle.theta), angle.point4[1] + angle.seat[1][1] + 50 * math.cos(angle.theta))
        self.torso._set_angle(-angle.theta)
        self.legs.position = (angle.point4[0] + angle.seat[0][0] - 25 * math.sin(angle.theta), angle.point4[1] + angle.seat[0][1] - 25 * math.cos(angle.theta))
        self.legs._set_angle(-angle.theta)
        self.head.position = (angle.point4[0] + angle.seat[1][0] + 90 * math.sin(angle.theta), angle.point4[1] + angle.seat[1][1] + 90 * math.cos(angle.theta))

        # Create pivot joints for bodies
        self.pivot1 = pymunk.PivotJoint(self.top, self.rod1, (600, 695))
        self.pivot2 = pymunk.PivotJoint(self.rod1, self.rod2, angle.point1)
        self.pivot3 = pymunk.PivotJoint(self.rod2, self.rod3, angle.point2)
        self.pivot4 = pymunk.PivotJoint(self.rod3, self.seat, angle.point4)
        self.pivot5 = pymunk.PinJoint(self.rod3, self.seat, anchor_a=angle.rod3, anchor_b=angle.seat[0])
        self.pivot6 = pymunk.PinJoint(self.rod3, self.seat, anchor_a=angle.rod3, anchor_b=angle.seat[1])

        self.pivot7 = pymunk.PivotJoint(self.torso, self.seat, (angle.point4[0] + angle.seat[1][0], angle.point4[1] + angle.seat[1][1]))
        self.pivot8 = pymunk.PivotJoint(self.seat, self.legs, (angle.point4[0] + angle.seat[0][0], angle.point4[1] + angle.seat[0][1]))
        self.gear1 = pymunk.GearJoint(self.torso, self.seat, angle.theta, 1.0)
        self.gear2 = pymunk.GearJoint(self.seat, self.legs, -angle.theta, 1.0)

        self.pivot9 = pymunk.PivotJoint(self.head, self.torso, self.head.position)
        # pin = pymunk.DampedSpring(self.rod3, self.torso, anchor_a=(0,0), anchor_b=(0,0), rest_length=100, stiffness=5, damping=0.1)#, min=20, max=100)

        # Add damping
        # damping1 = pymunk.DampedSpring(self.top, self.rod1, anchor_a=(-600,-25), anchor_b=(0,-rod1_length / 2), rest_length=100, stiffness=5, damping=3)
        # damping2 = pymunk.DampedSpring(self.top, self.rod1, anchor_a=(600,-25), anchor_b=(0,-rod1_length / 2), rest_length=100, stiffness=5, damping=3)

        # Disable collisions between rods
        self.pivot1.collide_bodies = False
        self.pivot2.collide_bodies = False
        self.pivot3.collide_bodies = False
        self.pivot4.collide_bodies = False

        self.pivot7.collide_bodies = False
        self.pivot8.collide_bodies = False
        self.pivot9.collide_bodies = False

        # Add bodies and pivots to space
        self.space.add(self.top, top_shape, self.bottom, bottom_shape, self.rod1, rod1_shape, self.rod2, rod2_shape, self.rod3, rod3_shape, self.seat, seat_shape, self.torso, torso_shape, self.legs, legs_shape, self.head, head_shape, self.pivot1, self.pivot2, self.pivot3, self.pivot4, self.pivot5, self.pivot6, self.pivot7, self.pivot8, self.pivot9, self.gear1, self.gear2)

    def delete(self):
        self.space.remove(self.top, top_shape, self.bottom, bottom_shape, self.rod1, rod1_shape, self.rod2, rod2_shape, self.rod3, rod3_shape, self.seat, seat_shape, self.torso, torso_shape, self.legs, legs_shape, self.head, head_shape, pivot1, pivot2, pivot3, pivot4, pivot5, pivot6, pivot7, pivot8, pivot9, self.gear1, self.gear2)



class Window(pyglet.window.Window):
    '''
    The 'Window' class which represents a pyglet window for our swing simulation.
    '''
    def __init__(self, width: int = 1200, height: int = 720, title: str = "Simulation", q_table: np.array = np.zeros((181,5)), timeout: int = 20):
        super().__init__(width, height, title, resizable=False)

        self.space = pymunk.Space()
        self.space.gravity = 0, -1000

        self._width = width
        self._height = height
        self._title = title
        self.q_table = q_table
        self._timeout = timeout

        self.theta = 20
        
        self.angle = self.theta
        self.angle_history = []
        self.time = 0

        self.state = self.reset()
        
        self.epochs, self.penalties, self.reward = 0, 0, 0
        done = False

        self.image = pyglet.image.load('q_table.png')
    
    def reset(self):
        self.swing = Swing(self.space, self.theta)
        # self.swing.rod1._set_angle(math.pi / 2)
        # self.swing.rod2.apply_force_at_local_point((force * math.cos(self.angle),force * math.sin(self.angle)), (0,0))
        return 0
    
    def env_step(self, action: int):
        if action == 0: self.swing.gear2._set_phase(-self.theta * math.pi / 180 - 1.2)
        elif action == 1: self.swing.gear2._set_phase(-self.theta * math.pi / 180 + 0.8)
        elif action == 2: self.swing.gear1._set_phase(self.theta * math.pi / 180 - 0.2)
        elif action == 3: self.swing.gear1._set_phase(self.theta * math.pi / 180 + 0.6)

        try: angle = int(self.swing.rod1._get_angle() * (180 / math.pi) - self.theta)
        except: angle = -90

        if angle > 90: angle = 90
        if angle < -90: angle = -90

        if self.swing.pivot3.impulse > 8000:
            penalty = self.swing.pivot3.impulse
            print("Penalty given: " + str(round(self.swing.pivot3.impulse, 1)))
        elif action == 4:
            penalty = 0
        else:
            penalty = 1
        return angle + 90, abs(angle) - penalty
        
    def on_mouse_press(self, x, y, button, modifiers):
        b = pymunk.Body(10, 10)
        b_shape = pymunk.Circle(b, 10)
        b.position = x, y
        self.space.add(b, b_shape)
        print(x,y)
        
        # self.robot = Robot(self.space, (x,y))

        if button == pyglet.window.mouse.LEFT:
            self.swing.gear2._set_phase((self.theta - 90) * math.pi / 180 - 1.2)
            self.swing.rod2.apply_force_at_local_point((force * math.cos(self.angle),force * math.sin(self.angle)), (0,0))
        if button == pyglet.window.mouse.RIGHT:
            self.swing.gear2._set_phase((self.theta - 90) * math.pi / 180 + 0.8)
            self.swing.rod2.apply_force_at_local_point((-force * math.cos(self.angle),force * math.sin(self.angle)), (0,0))

    def on_draw(self):
        self.clear()
        self.space.debug_draw(options)
        time = pyglet.text.Label(str(round(self.time, 1)) + "s",
                          font_name='Helvetica',
                          font_size=36,
                          x=1130, y=660,
                          anchor_x='center', anchor_y='center')
        time.draw()
        angle = pyglet.text.Label(str(round(self.angle, 1)) + "°",
                          font_name='Helvetica',
                          font_size=36,
                          x=1130, y=610,
                          anchor_x='center', anchor_y='center')
        angle.draw()
        self.image.blit(0, 0)
    
    def update(self, dt):
        self.space.step(dt)
        self.time += dt
        self.angle_history.append(self.swing.rod1._get_angle())

        # print(self.swing.pivot3.impulse)

        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, 4) # Explore action space
        else:
            action = np.argmax(q_table[self.state]) # Exploit learned values
        
        next_state, reward = self.env_step(action)

        old_value = self.q_table[self.state, action]
        next_max = np.max(self.q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[self.state, action] = new_value

        self.state = next_state
        self.epochs += 1

        # if self.swing.rod1._get_angle() > 0 and self.swing.rod1._get_angle() < self.angle:
        #     self.swing.gear2._set_phase(-1.2)
        #     self.swing.gear1._set_phase(0.6)
        #     print("Kicking forward")
        # elif self.swing.rod1._get_angle() < 0 and self.swing.rod1._get_angle() > self.angle:
        #     self.swing.gear2._set_phase(0.8)
        #     self.swing.gear1._set_phase(-0.2)
        #     print("Kicking backward")

        self.angle = int(self.swing.rod1._get_angle() * (180 / math.pi) - self.theta)
        if self.time > self._timeout: self.exit_callback(dt)
    
    def exit_callback(self, dt):
        self.close()

if __name__ == "__main__":
	try:
		np.savetxt('q_table.csv', np.zeros((181,5)), delimiter=',') # For resetting q_table
		q_table = np.loadtxt('q_table.csv', delimiter=',')

		for i in range(1, episodes):
			print("----- Episode " + str(i) + " -----")

			plt.matshow(q_table)
			plt.savefig('q_table.png', bbox_inches='tight', dpi=56)

			window = Window(q_table=q_table, timeout=20)
			pyglet.clock.schedule_interval(window.update, 1.0/60)
			pyglet.app.run()

			np.savetxt('q_table.csv', q_table, delimiter=',')


		# Initialise window
		window = Window(q_table=q_table)

		# Start pyglet window
		start = time.time()
		pyglet.clock.schedule_interval(window.update, 1.0/60)
		pyglet.app.run()
		stop = time.time()

		t = np.linspace(0, stop-start, len(window.angle_history))

		plt.plot(t, window.angle_history)
		plt.title("Angle over time")
		plt.xlabel("Time")
		plt.ylabel("Angle")
		plt.grid()
		plt.legend()
		plt.show()

	except KeyboardInterrupt:
		print("Simulation closing...")
		sys.exit()
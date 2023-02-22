#! /usr/bin/env python3

import rospy

from vc_robot.msg import command
from geometry_msgs.msg import Twist


pub = None

def callBackHandle(message):
	print(f"[Command Received] -> {message.command}")

	commands = {
	'front'  : ['front', 'f', 'forward'],
	'back'   : ['back' , 'b', 'backward'],
	'left'   : ['left' , 'l', 'leftward' , 'left turn' , 'turn left'],
	'right'  : ['right', 'r', 'rightward', 'right turn', 'turn right'],
	'stop'   : ['stop' , 's', 'halt']
	}

	linear_speed = 1
	angular_speed = 1

	outMessage = Twist()
	outMessage.linear.y = 0
	outMessage.linear.z = 0
	outMessage.angular.x = 0
	outMessage.angular.y = 0
	linear_x = 0
	angular_z = 0


	# Move Forward
	if message.command in commands['front']:
		linear_x = linear_speed
		angular_z = 0

	# Move Backward
	elif message.command in commands['back']:
		linear_x = -linear_speed
		angular_z = 0
		
	# Stop Motion
	elif message.command in commands['stop']:
		linear_x = 0
		angular_z = 0

	# Left Turn 
	elif message.command in commands['left']:
		linear_x = 0
		angular_z = -angular_speed

	# Right Turn
	elif message.command in commands['right']:
		linear_x = 0
		angular_z = angular_speed
		
	outMessage.linear.x = linear_x
	outMessage.angular.z = angular_z
	pub.publish(outMessage)


def main():
	global pub
	rospy.init_node('reading_command')

	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	sub = rospy.Subscriber('/vc_robot/command_as_text', command, callBackHandle)
	rospy.spin()

if __name__ == '__main__':
	print("Code Started.")
	main()

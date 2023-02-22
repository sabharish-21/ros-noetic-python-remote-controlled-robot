#! /usr/bin/env python3

from vc_robot.msg import command
import termios
import rospy
import tty
import sys

def getKey(settings):
	tty.setraw(sys.stdin.fileno())
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def main():
	rospy.init_node('kp_to_text')
	pub = rospy.Publisher('/vc_robot/command_as_text', command, queue_size=1)
	message = command()
	settings = termios.tcgetattr(sys.stdin)
	
	
	while True:
		try:
			key = getKey(settings)
			if key in ['w', 'W']:
				message.command = 'front'

			elif key in ['a', 'A']:
				message.command = 'left'

			elif key in ['s', 'S']:
				message.command = 'back'

			elif key in ['d', 'D']:
				message.command = 'right'
			
			elif key in ['q', 'Q']:
				print('Bye...')
				break

			else:
				message.command = 'stop'

			pub.publish(message)
		
		except KeyboardInterrupt:
			print("Okay Bye...")
			break

		except Exception as e:
			print(e)
			break

if __name__ == '__main__':
	print("""
		The Commands to control the robot :
		\t\t 1] Move Front	-> w / W
		\t\t 2] Turn Left	-> a / A
		\t\t 3] Move Back	-> s / S
		\t\t 4] Turn Right	-> d / D
		\t\t 5] Quit	-> q / Q
		\t\t 6] Stop	-> Any Other Key
		""")
	print("\nSelect the terminal and press the keys...\n")
	main()

#! /usr/bin/env python3

from vc_robot.msg import command
import rospy

commands =  [
		'front', 'f', 'forward',
		'back' , 'b', 'backward', 
		'left' , 'l', 'leftward' , 'left turn' , 'turn left', 
		'right', 'r', 'rightward', 'right turn', 'turn right', 
		'stop' , 's', 'halt',
		'quit' , 'q', 
	]

def main():
	global commands
	rospy.init_node('cli_to_text')
	pub = rospy.Publisher('/vc_robot/command_as_text', command, queue_size=1)
	message = command()
	
	while True:
		try:
			text = str(input("Enter your command -> ")).strip().lower()
			if text not in commands:
				print(f"[Command Not Recognised]")
				continue
				
			if text in ['quit', 'q']:
				print("Bye...")
				break
				
			message.command = text.lower().strip()
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
		\t\t 1] Move Front	-> front | f | forward
		\t\t 2] Turn Left	-> left  | l | leftward  | left turn   | turn left
		\t\t 3] Move Back	-> back  | b | backward
		\t\t 4] Turn Right	-> right | r | rightward | right turn  | turn tight
		\t\t 5] Quit	-> q | quit
		\t\t 6] Stop	-> s | stop
		""")
	main()

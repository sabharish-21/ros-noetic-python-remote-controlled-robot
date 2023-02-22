#! /usr/bin/env python3

from vc_robot.msg import command
import speech_recognition as sr
import rospy

pub = None
recognizer = sr.Recognizer()
microPhone = sr.Microphone()

commands =  [
		'front', 'f', 'forward',
		'back' , 'b', 'backward', 
		'left' , 'l', 'leftward' , 'left turn' , 'turn left', 
		'right', 'r', 'rightward', 'right turn', 'turn right', 
		'stop' , 's', 'halt',
		'quit' , 'q', 
	]


def main():
	global pub, commands
	rospy.init_node('vocie_to_text')
	pub = rospy.Publisher('/vc_robot/command_as_text', command, queue_size=1)
	message = command()

	try:
		with microPhone as source:
			recognizer.adjust_for_ambient_noise(source, duration=5)
			recognizer.energy_threshold

		while True:
			print('Press "Enter" to start listening ..')
			input("")
			print("[Listining Now]")
	  
			with microPhone as source:
				audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
			print("[Got you, Trying to Recognize]")
	  
			try:
				text = str(recognizer.recognize_google(audio)).lower().strip()
				
				if text not in commands:
					print(f"[Command Not Recognised]")
					continue

				if text in ['quit', 'q']:
					print("Bye...")
					break

				print("Command Recognized - {}".format(text))
				message.command = text
				pub.publish(message)
		
			except Exception as e:
				print(e)
				break

	except KeyboardInterrupt:
		print("Okay Bye...")

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

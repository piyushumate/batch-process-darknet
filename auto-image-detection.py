
#input - input_folder, output_folder


import pexpect
import sys
import os
import subprocess
base_copy_command = 'cp darknet/predictions.png '

def get_files(directory):
	return os.listdir(directory)

def move_output(input, output, file):
	a = file.split('.')
	a[1] = 'png'
	file = '.'.join(a)
	copy_command = base_copy_command + output + '/' + file
	x = subprocess.check_output([copy_command], shell=True)
	#add try catch


def main(arguments):
	command = './darknet detector test cfg/voc.data cfg/tiny-yolo-voc.cfg weights/tiny-yolo-voc.weights'
	if len(arguments) < 3:
		return 'Invalid number of arguments'
	input , output = arguments[1], arguments[2]
	files = get_files(input)
	child = pexpect.spawn(command, cwd='darknet')
	for index, file in enumerate(files):
		print 'processing -> ' ,file	
		child.expect ('Enter Image Path:')
		if index > 0:
			#print  child.before (parse this result)
			move_output(input, output, files[index-1])
		child.sendline('../'+input+'/'+file)
	#move the last one
	move_output(input, output,files[len(files)-1])
	
main(sys.argv)


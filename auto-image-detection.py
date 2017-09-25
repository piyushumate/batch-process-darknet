
#input - input_folder, output_folder


import pexpect
import sys
import os
import subprocess
import re
import ast
import csv
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

def write_file(filename, dic):
	f = open(filename + '.csv', 'a')
	try:
    		writer = csv.writer(f)
		writer.writerow( (dic['T'],dic['B'],dic['L'],dic['R'],dic['C']) )
	finally:
    		f.close()

 
def process_output(output, output_type):
	if output_type == 'bounded_box':
		output_stream = output.split('\n')		
		for os in output_stream:
			m = re.match("\{'(.*)'\}.*$", os)
			if m:
				config_dict = ast.literal_eval(m.group())
				write_file('tiny_yolo', config_dict)
def get_bounded_boxes(files, input, output, child):
	for index, file in enumerate(files):
		child.expect ('Enter Image Path:')
		if index > 0:
			process_output(child.before, 'bounded_box')
		child.sendline('../'+input+'/'+file)
	child.expect('Enter Image Path:')
	child.sendline('END')
	process_output(child.before, 'bounded_box')

def bulk_detect_and_copy(files, input, output, child):
	for index, file in enumerate(files):
		print 'processing ->', file
		child.expect ('Enter Image Path:')
		if index > 0: 
			move_output(input, output, files[index-1])
		child.sendline('../'+input+'/'+file)
	child.expect('Enter Image Path:')
	child.sendline('END')
	move_output(input, output,files[len(files)-1])


def main(arguments):
	if len(arguments) < 4:
		print 'Invalid number of arguments'
		return
	mode = int(arguments[3])
	input , output = arguments[1], arguments[2]
	files = get_files(input)
	command = './darknet detector test cfg/voc.data cfg/tiny-yolo-voc.cfg weights/tiny-yolo-voc.weights'
	child = pexpect.spawn(command, cwd='darknet')
	
	if mode == 1:
		bulk_detect_and_copy(files, input, output, child)
	elif mode == 2:
		get_bounded_boxes(files, input, output, child)
main(sys.argv)

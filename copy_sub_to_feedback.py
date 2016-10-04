import os
import sys
import subprocess
import shutil


def get_all_files(dir_attachments):


	files = []
	
	for file in os.scandir(dir_attachments):
		if file.is_file():
			files.append([file.name,file.path])
			print('file')
		else:
			files.extend(get_all_files(file.path))
			print('dir:' + file.name)

	return files



if len(sys.argv) == 2:
	print("Please privde the nyu class folder and tmp dir")
	sys.exit(1)


root_dir =  sys.argv[1]
tmp_dir = sys.argv[2]



for student_dir in  (os.scandir(root_dir)):


	if student_dir.is_file():
		continue

	fist_name = student_dir.name.split(',')[0].replace(' ', '')
	#print('>>' + fist_name + '<<')
	feedback_dir = student_dir.path + os.path.sep + 'Feedback Attachment(s)'
	#os.chdir(student_dir.path)

	found_file_with_comments = False
	found = False

	

	dir_feedback_attachments = []
	dir_attachments =  student_dir.path + os.path.sep + 'Submission attachment(s)'
	
	fp_comments = open(student_dir.path + os.path.sep + 'comments.txt', 'w')

	for file in os.scandir(dir_attachments):

		list_of_files = []
		if file.is_file():
			list_of_files.append([file.name,file.path])
			print('file:' +file.name)
		else:
			list_of_files.extend(get_all_files(file.path))
			print('dir:' + file.name)


		

		for item in list_of_files:

			file_name = item[0]
			file_path = item[1]

			fp = open(file_path)

			comments_begin = False
			code_begin = False

			line_comments = []
		
			for line in fp:
				#print(line)
				if line.find('#nr83') != -1:
					#print('sdda')
					comments_begin = True
					found_file_with_comments = True
					#print(line)
					found = True
					#line_comments.append('<p>')
					continue



				if line.find('###EnD') != -1:
					comments_begin = False
					#line_comments.append('</p>')
					continue


				if line.find('###code_begin') != -1:
					code_begin = True
					found_file_with_comments = True
					#print(line)
					found = True

					line_comments.append('<span style="color:#008000;">')

					line_comments.append('<pre>')
					continue

				if line.find('###code_end') != -1:
					code_begin = False
					line_comments.append('</pre>')
					line_comments.append('</span>')

					continue

				if comments_begin or code_begin:
					if(code_begin):

						line_comments.append(line)
					else:
						line_comments.append('<p>' + line.strip().replace('#', '') + '</p>')
					#print (line)
					
			if(len(line_comments)) != 0:

				line_comments.insert(0, '<b>' + file_name + '</b>')


				shutil.copy(file_path, feedback_dir)
				dir_feedback_attachments.append(file_name)
			#shutil.copyfile(each_file.path, tmp_dir + os.path.sep + fist_name + each_file.name )
		

		
			
				

			for line in line_comments:
				fp_comments.write(line)

	fp_comments.close()

	if len (dir_feedback_attachments) != 0:
		print(dir_feedback_attachments)

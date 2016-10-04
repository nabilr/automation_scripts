import os
import sys
import subprocess
import shutil
import zipfile
from subprocess import Popen, PIPE, STDOUT


def get_all_files(dir_attachments):


	files = []
	
	for file in os.scandir(dir_attachments):
		if file.is_file():
			if file.name[0] == '.':
				continue
			files.append([file.name, file.path])
			#print('file')
		else:
			#print('aaa' , file.name.lower()[0])
			if(file.name.lower() != 'common' and file.name.lower()[0] != '.'):
				files.extend(get_all_files(file.path))
				#rint('sdsd' + file.name)
			#print('dir:' + file.name)

	return files





def zipfile_extract_all(root_dir):

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
		
		#fp_comments = open(student_dir.path + os.path.sep + 'comments.txt', 'w')


		list_of_files = get_all_files(dir_attachments)

		
			

		for item in list_of_files:

			
			#print(item)
			if(zipfile.is_zipfile(item[1])):
				zp = zipfile.ZipFile(item[1])
				zp.extractall(path=dir_attachments)
				print (item)
						
				#if(len(line_comments)) != 0:

				#	line_comments.insert(0, '<b>' + file_name + '</b>')


				#	shutil.copy(file_path, feedback_dir)
				#	dir_feedback_attachments.append(file_name)
				#shutil.copyfile(each_file.path, tmp_dir + os.path.sep + fist_name + each_file.name )
			

			
				
					

				#for line in line_comments:
				#	fp_comments.write(line)

		#fp_comments.close()

		#if len (dir_feedback_attachments) != 0:
		#	print(dir_feedback_attachments)



def convert_all_files_to_pdf(root_dir):

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
		
		#fp_comments = open(student_dir.path + os.path.sep + 'comments.txt', 'w')


		list_of_files = get_all_files(dir_attachments)
		
			

		text_files = []
		jpeg_fles = []
		pdf_files = []

		for item in list_of_files:

			args = ['file', item[1]]
			p = subprocess.Popen(args, stdout=PIPE) 
			file_type = p.stdout.read().decode("utf-8").split(':')[1].split(',')[0].lower()
			if 'text' in file_type:
				print('text file')
				text_files.append(item)
			elif 'jpeg' in file_type:
				jpeg_fles.append(item)
				print('jpeg file') 
			elif 'html' in file_type:
				print('html file') 
				text_files.append(item)
			elif 'pdf' in file_type:
				pdf_files.append(item)
				print('pdf file')
			elif 'macintosh' in file_type:
				print('macintosh file')
			elif 'zip' in file_type:
				print('zip file')
			else:
				print(item[1], file_type + 'daaaaa')

		if len(jpeg_fles) > 0:
			#print(jpeg_fles)

			args = ['convert']

			for i in jpeg_fles:
				args.append(i[1])
			
			args.append(feedback_dir + os.path.sep + 'final1.pdf')

			print(args)
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()
			

		if len(text_files) > 0:
			#print(jpeg_fles)
			#enscript -p file.ps file.txt
			#ps2pdf file.ps file.pdf
			


			tmp_dir = dir_attachments + os.path.sep + 'tmp'
			args = ['mkdir', '-p', tmp_dir ]
			p =subprocess.Popen(args, stdout=PIPE) 
			p.communicate()


			for i in range(0, len(text_files)):

				original_file = text_files[i][1]
				copy_file = tmp_dir + os.path.sep + text_files[i][0] + '.txt'
				print(original_file)
				shutil.copyfile(original_file, copy_file)
				text_files[i][1] = copy_file


			args = ['enscript', '-p', feedback_dir + os.path.sep + 'final2.ps']

			for i in text_files:
				args.append(i[1])

			#args.extend(text_files)
			print(args)
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()

			args = ['rm', '-r', tmp_dir ]
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()

			#print(p.stdout.read())	


			#args = ['enscript', '-B']
			#args.extend(text_files)
			#args.extend(['-o', feedback_dir + os.path.sep + 'final2.ps'])
			#print(args)
			#p = subprocess.Popen(args, stdout=PIPE) 
			#print(p.stdout.read())	


			#args = ['pandoc']
			#args.extend(text_files)
			#args.extend( ['-o', feedback_dir + os.path.sep + 'final2.pdf'])
			#print(args)
			#p = subprocess.Popen(args, stdout=PIPE) 
			#print(p.stdout.read())	

			#args = ['ps2pdf',  'convert -density 300',  '-sPAPERSIZE=a4' ]
			args = ['ps2pdf']
			args.append(feedback_dir + os.path.sep + 'final2.ps')
			args.append(feedback_dir + os.path.sep + 'final2.pdf')
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()

			#args = ['ps2pdf', feedback_dir + os.path.sep +'final2.ps', feedback_dir + os.path.sep + 'final2.pdf']

		
			print(args)
			args = ['rm', feedback_dir + os.path.sep + 'final2.ps' ]
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()


			

			args = ['pdfunite', feedback_dir + os.path.sep + 'final2.pdf',  feedback_dir + os.path.sep + 'final1.pdf' , ]

			for i in pdf_files:
				args.append(i[1])

			args.append( feedback_dir + os.path.sep + 'final.pdf')
			print(args)
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()



			args = ['pdftk',  feedback_dir + os.path.sep + 'final.pdf',  'burst',  'output' , feedback_dir + os.path.sep  + 'output_%02d.pdf',  'compress']


			print(args)
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()






			#print(args)
			args = ['rm', feedback_dir + os.path.sep + 'final1.pdf' ,  feedback_dir + os.path.sep + 'final2.pdf' ]
			args.append(feedback_dir + os.path.sep + 'doc_data.txt' )
			args.append(feedback_dir + os.path.sep + 'final.pdf')
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()


			#/usr/bin/pdfjam --no-tidy  --outfile f.pdf --paper a4paper -- output_01.pdf

			count= 0

			a4_paper_list = []

			flist = []
			for f in  (os.scandir(feedback_dir)):


				if 'output' in f.name:

					flist.append(f.path)



			print(flist)
			flist.sort()
			print(flist)
			for f in flist:

				a4_paper= feedback_dir + os.path.sep+'f'+str(count)+'.pdf'

				a4_paper_list.append(a4_paper)
				args = ['pdfjam', '--outfile', a4_paper  , '--paper',  'a4paper', '--' , f]
				p = subprocess.Popen(args, stdout=PIPE) 
				p.communicate()

				p = subprocess.Popen(['rm', f], stdout=PIPE) 
				p.communicate()
				count += 1
					


			args = ['pdfjam', '--outfile',  feedback_dir + os.path.sep + 'final.pdf'  , '--paper',  'a4paper', '--' ]

			#args = ['pdfunite']
			args.extend(a4_paper_list)
			#args.append(feedback_dir + os.path.sep + 'final.pdf')
			p = subprocess.Popen(args, stdout=PIPE) 
			p.communicate()

			#for f in a4_paper_list:
			#	p = subprocess.Popen(['rm', f], stdout=PIPE) 

			#	p.communicate()











if len(sys.argv) == 2:
	print("Please privde the nyu class folder and tmp dir")
	sys.exit(1)


root_dir =  sys.argv[1]
tmp_dir = sys.argv[2]
zipfile_extract_all(root_dir)
convert_all_files_to_pdf(root_dir)

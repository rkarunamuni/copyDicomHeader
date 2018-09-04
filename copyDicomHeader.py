
import sys
import os
import pydicom
import subprocess
import pdb
import argparse 

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("template", help = "DICOM file to be used as template")
	parser.add_argument("destination", help = "destination DICOM file or directory whose header should be modified")
	parser.add_argument('-sd', '--scan_directories', help = "scan directories of destination directory", action = "store_true")
	args= parser.parse_args()

	templateDICOM = os.path.abspath(args.template)
	if not os.path.isfile(templateDICOM):
		sys.exit('template DICOM file not found')
	# try reading the DICOM header of the tempalte DICOM
	try:
		dsTemplate = pydicom.dcmread(templateDICOM)
	except:
		sys.exit('template DICOM cannot be read')

	tags = ['PatientName', 'PatientID', 'PatientBirthDate', 'PatientBirthTime', 'PatientSex']


	sourcePath = os.path.abspath(args.destination)
	# check if source is directory or file
	if os.path.isdir(sourcePath):
		if not args.scan_directories:
			for filenames in os.listdir(sourcePath):
				try: 
					dsSource = pydicom.dcmread(os.path.join(sourcePath, filenames))
					for tag in tags:
						os.system('dcmodify -m "%s=%s" "%s" -nb -imt' % (tag,dsTemplate.data_element(tag).value,os.path.join(sourcePath, filenames)))
						print('Successfully modified - %s - %s' % (os.path.join(sourcePath, filenames) ,tag))
				except:
					continue
		else:
			for root,_,filenames in os.walk(sourcePath):
				for filename in filenames:
					try:
						dsSource = pydicom.dcmread(os.path.join(root, filename))
						for tag in tags:
							os.system('dcmodify -m "%s=%s" "%s" -nb -imt' % (tag,dsTemplate.data_element(tag).value,os.path.join(root, filename)))
							print('Successfully modified - %s - %s' % (os.path.join(root, filename) ,tag))
					except:
						continue
	elif os.path.isfile(sourcePath):
		try:
			dsSource = pydicom.dcmread(sourcePath)
			for tag in tags:
				os.system('dcmodify -m "%s=%s" "%s" -nb -imt' % (tag,dsTemplate.data_element(tag).value, sourcePath))
				print('Sucessfully modified - %s' % sourcePath)
		except:
			sys.exit('DICOM file to be modified cannot be read')		
	else:
		sys.exit('Unrecognized DICOM/directory of DICOMs to modify') 



if __name__ == '__main__':
	main()

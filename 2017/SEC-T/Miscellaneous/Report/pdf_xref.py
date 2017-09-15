#!/usr/bin/python

import sys

def CheckXrefTable(verbose):

	# Check for input PDF argument
	if len(sys.argv) != 2:
		print "Usage: $ ./pdf_xref.py pdf_file"
		exit()

	# Open pdf file for reading
	with open(sys.argv[1], 'r') as pdf:

		# List to hold xref entires
		xref_table = []

		# Read in xref table. AKA: xref -> trailer
		read = False
		for line in pdf:
		    if line.strip() == "xref":
		        read = True
		    elif "trailer" in line.strip():
		        read = False
		    elif read:
		    	xref_table.append(line)

		# First entry = ( Number of first object, number of entries)
		temp = xref_table[0].split(" ")
		number_of_first_object = temp[0]
		number_of_entires = int(temp[1][:-1])

		# Remove first entry
		xref_table = xref_table[1:]

		# Check number of entires
		if len(xref_table) != number_of_entires:
			print "ERROR: Number of entires in xref table doesn't match. Found = "+str(len(xref_table))+" Expected: "+str(number_of_entires)

		# Check each entry is 20 bytes long
		for entry in xref_table:
			if len(entry) != 20:
				print "ERROR: Not all entries have a length of 20. Entry: "+str(xref_table.index(entry))

		# Match all entires to an object based off byte offset
		# and match generation number
		found_objects = [] # [(id, gen)]
		for entry in xref_table:
			if xref_table.index(entry) != 0:

				offset = int(entry.split(" ")[0])
				if verbose: print "Xref object byte offset: "+str(offset)

				generation_number_str = (entry.split(" ")[1]).strip('0')
				if verbose: print "Xref object generation number: "+generation_number_str

				pdf.seek(offset,0)

				temp = pdf.read(len(str(number_of_entires))+len(generation_number_str)+1).split(" ")
				if verbose: print "Information at offset: "+" ".join(temp)

				found_object_id = temp[0]
				if verbose: print "Found object id: "+found_object_id

				found_generation_number = temp[1]
				if verbose: print "Found object generation number: "+found_generation_number

				if generation_number_str != found_generation_number:
					if generation_number_str != "":
						print "ERROR: Generation numbers dont match. Expected: "+generation_number_str+" Found: "+found_generation_number

				found_objects.append((found_object_id,found_generation_number))
			

		if len(found_objects)+1 != int(number_of_entires):
			print "ERROR: Wrong number of objects matched to xref table. Found = "+str(len(found_objects))+" Expected: "+str(number_of_entires)

		# Check that each object number is an INT and the first is %PF
		for num in found_objects:
				try:
					int(num[0])
				except:
					print "ERROR: Found object is not an int. "+num


def flag_finder():
	# Open pdf file for reading
	with open(sys.argv[1], 'r') as pdf:

		# List to hold xref entires
		xref_table = []

		# Read in xref table. AKA: xref -> trailer
		read = False
		for line in pdf:
		    if line.strip() == "xref":
		        read = True
		    elif "trailer" in line.strip():
		        read = False
		    elif read:
		    	xref_table.append(line)		
	
		print "".join([c for c in [a[3:].decode('hex') for a in [e.split(" ")[1] for e in xref_table[1:]][1:]][::-1] if c != "\x00"])		
		

if __name__ == "__main__":
	CheckXrefTable(False)
	flag_finder()
	
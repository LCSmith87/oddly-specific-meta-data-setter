#!/usr/bin/env python
#

# import modules used here
import sys, argparse, os, json, shutil, pyexiv2


# opens up the text file, reads it, and makes a 
# copy of the photo directory
def get_text_file(filepath):
	print "-" * 50
	print "Getting Text File"
	print "-" * 50
	f = os.path.abspath(filepath)
	directory = os.path.dirname(f)
	r = open(f, 'r')
	a = r.read()
	print "-" * 50
	print "Getting Text File - Completed"
	print "-" * 50
	print "-" * 50
	print "Copying Directory"
	print "-" * 50
	shutil.copytree(directory, directory + "_new-metadata")
	print "-" * 50
	print "Copying Directory - Completed"
	print "-" * 50
	append_meta_data(a,directory)

# Loops through data and strips out unnecessary stuff
# Compiles a list of file names, titles, and captions
# Opens up an image and writes the corresponding data
# to its XMP and IPTC metadata
def append_meta_data(data_to_parse, directory):
	print "-" * 50
	print "Copying Files and Appending MetaData"
	print "-" * 50
	new_data = ""

	for item in data_to_parse.split("\n"):
		if "Photo name:" in item:
			new_data = item.strip().replace("Photo name: ", "")
			img_name = directory + "_new-metadata" + "\\" + new_data
			metadata = pyexiv2.ImageMetadata(img_name)
			metadata.read()
		if "Photo title:" in item:
			new_data = item.strip().replace("Photo title: ", "")
			key = "Xmp.dc.title"
			value = new_data
			metadata[key] = pyexiv2.XmpTag(key, value)
		if "Photo caption:" in item:
			new_data = item.strip().replace("Photo caption: ", "") + "\n\n"
		if "For more see" in item:
			new_data += item.strip().replace(".html", ".html?cmpid=CampaignID")
			key_caption = "Iptc.Application2.Caption"
			value_caption = [new_data]
			metadata[key_caption] = pyexiv2.IptcTag(key_caption, value_caption)
			metadata.write()

	print "-" * 50
	print "Completed"
	print "-" * 50

# Gather our code in a main() function
def main(args):
	print " " * 200
	print "-" * 200
	print "Welcome to Levi's Wonderfully Amazing MetaData Appender Thingy"
	print "-" * 200
	print " " * 200
	get_text_file(sys.argv[2])

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )

  parser.add_argument(
                      "-f",
                      "--file",
                      help="Pass a filepath with the properly formatted file to set Title, Description metadata to images in list",
                      action="store")
  parser.add_argument(
                      "-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  
  main(args)

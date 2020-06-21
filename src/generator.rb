#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "parser.rb"


def make_yml(site_name, dir, src_dir, files)
	yml = File.open(dir + "mkdocs.yml", "w")
	labels = get_labels(rm_tab(get_blocks(src_dir + "*.ark")))

	# yaml config file writing
	## define site name
	yml.write("site_name: ")
	yml.write(site_name + NewLine)
	## add pages
	yml.write("nav:")
	yml.write(NewLine)
	labels.each { |e|
		label = ""
		e.each_char { |c|
			next if c == OBracket || c == OPar || c == CPar || c == NewLine 
			if c == CBracket
				label << ": "
				next
			end

			label << c
		}

		yml.write(' ')
		yml.write(Each + ' ')
		yml.write(label + ".md")
		yml.write(NewLine)
	}

	## end of write config file
	yml.close
end

def make_md(files, doc_dir)
	md_dir = doc_dir + "docs/"
	take = false

	if !Dir.exist?(md_dir)
		Dir.mkdir(md_dir)
	else
		old = Dir.glob(md_dir + "*.md")
		old.each { |e|
			File.delete(e)
		}
	end

	files.each_index { |i|
		md_name = ""
		files[i].keys[0].each_char { |c|
			take = true if c == CBracket
			next if c == CBracket
			md_name << c if take
		}

		take = false
		md_name << ".md"
		md = File.open(md_dir + md_name, "w")
		md.write(files[i][files[i].keys[0]])
		md.close
	}
end

def get_doc_dir(site_name)
	return "docs/" + site_name + '/'
end

def gen(site_name, source_dir)
	files = parser(source_dir)
	doc_dir = get_doc_dir(site_name)

	puts("INFO	-  Constructing of the site for documentation")
	if !Dir.exist?(doc_dir) 
		Dir.mkdir(doc_dir)
	end

	make_yml(site_name, doc_dir, source_dir, files)
	make_md(files, doc_dir)
end
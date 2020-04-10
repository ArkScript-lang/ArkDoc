#!/usr/bin/env ruby -wKU
$LOAD_PATH << "src"
require "generator.rb"


def start
	command = ARGF.argv[0]
	site_name = ARGF.argv[1]
	doc_dir = get_doc_dir(site_name)

	if command == "gen"
		gen(site_name)
		Dir.chdir(doc_dir)
		puts %x{mkdocs build}
	else
		puts("No valid command typed")
	end
end

if ARGF.argv.size >= 2
	start
else
	puts("Usage : ruby start.rb COMMAND [SITE_NAME]")
end

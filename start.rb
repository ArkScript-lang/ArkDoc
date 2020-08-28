#!/usr/bin/env ruby -wKU
$LOAD_PATH << "src"
require "generator.rb"


def help
    puts("Usage : ruby start.rb [Option] Command [Option]")
    puts("Options :")
    puts("-h : print help message")
    puts("Command :")
    puts("gen [Site name] : generate the site")
    puts("Generation option :")
    puts("-S [Source directory] : set the source files directory")
end

def start
    site_name = ""
    doc_dir = ""
    source_dir = "ark/"

    # Options
    case ARGF.argv[0]
    when "-h"
        help
        return 0
    when "gen"
        if ARGF.argv[1] == "-S"
            source_dir = ARGF.argv[2]
            site_name = ARGF.argv[3]
            doc_dir = get_doc_dir(site_name)
        else
            site_name = ARGF.argv[1]
            doc_dir = get_doc_dir(site_name)
        end

        gen(site_name, source_dir)
        Dir.chdir(doc_dir)
        puts %x{mkdocs build}
    else
        puts("Invalid command or option")
    end
end

if ARGF.argv.size >= 1
    start
else
    help
end
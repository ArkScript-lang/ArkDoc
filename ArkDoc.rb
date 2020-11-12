#!/usr/bin/env ruby -wKU
$LOAD_PATH << "src"
require "Generator.rb"


def help
    puts("Usage : ruby ArkDoc.rb Command [Option] ...")
    puts("Commands :")
    puts("-H, --help : print help message")
    puts("-G, --generate [Site name] : generate the site")
    puts("-M, --md [Site name] : generate the markdown files")
    puts("-B, --build [Site name] : generate site using .md files")
    puts("Options :")
    puts("Generation option :")
    puts("-S, --source [Source directory] : set the source files directory")
end

def start
    doc_name = ""
    source_dir = ""
    generator = Generator.new

    # Options
    case ARGF.argv[0]
    when "-H", "--help"
        help
        return 0
    when "-G", "--generate"
        if ARGF.argv[1] == "-S" || ARGF.argv[1] == "--source"
            source_dir = ARGF.argv[2]
            doc_name = ARGF.argv[3]
        else
            doc_name = ARGF.argv[2]
        end

        generator.generate(doc_name, source_dir)
        Dir.chdir("..")
        puts(%x{mkdocs build})
    when "-M", "--md"
        if ARGF.argv[1] == "-S" || ARGF.argv[1] == "--source"
            source_dir = ARGF.argv[2]
            doc_name = ARGF.argv[3]
        else
            doc_name = ARGF.argv[2]
        end

        generator.generate(doc_name, source_dir)
        Dir.chdir("..")
    when "-B", "--build"
        puts(%x{mkdocs build})
    else
        puts("Invalid command or option")
        return 1
    end
end

if ARGF.argv.size >= 1
    start
else
    help
end
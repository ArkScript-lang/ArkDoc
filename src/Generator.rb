#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "Parser.rb"


class Generator
    attr_accessor :doc_name

    def initialize
        @parser = Parser.new
        @docs_path = "docs/"
    end

    def make_yml(doc_name, src_dir = "")
        puts(Dir.pwd)
        if !Dir.exist?(@docs_path)
            Dir.mkdir(@docs_path)
        end

        doc_path = @docs_path + doc_name
        if !Dir.exist?(doc_path)
            Dir.mkdir(doc_path)
        end
        Dir.chdir(doc_path)

        @parser.lexer.ark_path = src_dir if src_dir != ""
        @parser.parse
        labels = @parser.parsed.keys

        yml = File.open("mkdocs.yml", 'w')

        # yaml config file writing
        ## define site name
        yml.write("site_name: ")
        yml.write(doc_name + NewLine)
        ## add pages
        yml.write("nav:")
        yml.write(NewLine)
        labels.each { |label|
            yml.write(' ')
            yml.write(Each + ' ')
            yml.write(label.capitalize + ':')
            yml.write(' ')
            yml.write(label + ".md")
            yml.write(NewLine)
        }

        ## end of write config file
        yml.close
    end

    def make_md
        md_dir = "docs/"

        if !Dir.exist?(md_dir)
            Dir.mkdir(md_dir)
            Dir.chdir(md_dir)
        else
            Dir.chdir(md_dir)
            old = Dir.glob("./*.md")
            old.each { |e|
                File.delete(e)
            }
        end

        for file in @parser.parsed.keys
            md = File.open(file + ".md", 'w')
            md << @parser.parsed[file]
            md.close
        end
    end

    def generate(site_name, source_path = "")
        puts("INFO  -  Constructing of the site for documentation")

        make_yml(site_name, source_path)
        make_md
    end
end
#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "Parser.rb"


class Generator
    attr_accessor :doc_name

    def initialize
        @parser = Parser.new
        @docs_path = "docs/"
    end

    def index(doc_name, md_dir)
        index_md = File.open( md_dir + "index.md", 'w')

        index_md.write("# #{doc_name}")
        index_md.write(NewLine)
        index_md.write("##")
        index_md.write("Pages")
        @parser.parsed.keys.each { |key|
            index_md.write(NewLine)
            index_md.write(Page + "[#{key}]" + "(#{key}.md)")
            index_md.write("")
            index_md.write(NewLine)
        }

        index_md.close
    #end

    def make_yml(doc_name, src_dir = "")
        Dir.mkdir(@docs_path) if !Dir.exist?(@docs_path)
        doc_path = @docs_path + doc_name
        Dir.mkdir(doc_path) if !Dir.exist?(doc_path)

        @parser.lexer.ark_path = src_dir if src_dir != ""
        @parser.parse
        labels = @parser.parsed.keys

        yml = File.open(doc_path + '/' + "mkdocs.yml", 'w')

        # yaml config file writing
        # define site name
        yml.write("site_name: ")
        yml.write(doc_name + NewLine)
        # add pages
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

        # end of write config file
        yml.close

        return doc_path
    end

    def make_md(doc_name)
        md_dir = "docs/" + doc_name + '/' + "docs/"

        if !Dir.exist?(md_dir)
            Dir.mkdir(md_dir)
        else
            old = Dir.glob(md_dir + "/*.md")
            old.each { |e|
                File.delete(e)
            }
        end

        for file in @parser.parsed.keys
            md = File.open(md_dir + file + ".md", 'w')
            md << @parser.parsed[file]
            md.close
        end
    end

    def generate(site_name, source_path = "")
        path_to_doc = make_yml(site_name, source_path)
        make_md(site_name)

        return path_to_doc
    end
end
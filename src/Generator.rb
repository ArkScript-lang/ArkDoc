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
        index_md.write(NewLine)
        @parser.parsed.keys.sort.each { |key|
            index_md.write(NewLine)
            index_md.write(Page + "[#{key.capitalize}]" + "(#{key}.md)")
            index_md.write("")
            index_md.write(NewLine)
        }

        index_md.close
    end

    def make_yml(doc_name, src_dir = "")
        Dir.mkdir(@docs_path) if !Dir.exist?(@docs_path)
        doc_path = @docs_path + doc_name
        Dir.mkdir(doc_path) if !Dir.exist?(doc_path)

        @parser.lexer.ark_path = src_dir if src_dir != ""
        @parser.parse
        labels = @parser.parsed.keys.sort

        yml = File.open(doc_path + '/' + "mkdocs.yml", 'w')

        # yaml config file writing
        # define site name
        yml.write("site_name: ")
        yml.write(doc_name + NewLine)
        # add pages
        yml.write("nav:")
        yml.write(NewLine)

        # home page
        yml.write(Separator)
        yml.write(Each + Separator)
        yml.write("Home:")
        yml.write(Separator)
        yml.write("index.md")
        yml.write(NewLine)

        labels.each { |label|
            yml.write(Separator)
            yml.write(Each + Separator)
            yml.write(label.capitalize + ':')
            yml.write(Separator)
            yml.write(label + ".md")
            yml.write(NewLine)
        }

        # theming
        yml.write(ThemeTag)
        yml.write(NewLine)
        yml.write(Separator)
        yml.write(Separator)
        yml.write(ThemeNameTag)
        yml.write(Separator)
        yml.write("null")
        yml.write(NewLine)
        yml.write(Separator)
        yml.write(Separator)
        yml.write(ThemeDirTag)
        yml.write(Separator)
        yml.write(ThemeDir)
        yml.write(DarkTheme)

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

        # home page
        index(doc_name, md_dir)
        for file in @parser.parsed.keys
            md = File.open(md_dir + file + ".md", 'w')
            md << @parser.parsed[file]
            md.close
        end
    end

    def generate(site_name, source_path = "")
        path_to_doc = make_yml(site_name, source_path)
        puts("ArkDoc - Generation of configuration file")
        make_md(site_name)
        puts("ArkDoc - Generation of Markdown files")

        return path_to_doc
    end
end
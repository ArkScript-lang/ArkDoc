#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "Extend.rb"
require "Format.rb"

class Lexer
    attr_reader :tokens
    attr_accessor :ark_path
    DocBlock = ["###", "##"]
    Code = ["=begin", "=end"]
    Keywords = ["@meta", "@brief", "@param", "@author", "@details"]

    def Key(key) Keywords[key].upcase; end

    def Value(key, line) (line.refine)[Keywords[key].size..-1].lstrip; end

    def initialize
        @ark_path = "../../ark/"
        @tokens = []
    end

    def tokenize
        files_paths = Dir.new(@ark_path)

        files_paths.each_child do |file_path|
            lines = file_ary(File.open(@ark_path + file_path, 'r'))
            file = {}.compare_by_identity
            i = 0

            # doc block
            doc_block = false
            # code example
            code = false
            code_str = ""

            while i < lines.size
                if lines[i].strip == DocBlock[0] && !doc_block
                    puts("begin : #{i + 1}")
                    doc_block = true
                elsif lines[i].strip == DocBlock[1] && doc_block
                    puts("end : #{i + 1}")
                    doc_block = false
                end

                if doc_block
                    # code example token
                    if lines[i].include?(Code[0]) && !code
                        code = true
                    elsif lines[i].include?(Code[1]) && code
                        file["CODE"] = code_str
                        code_str = ""
                        code = false
                    end

                    if code
                        code_str << lines[i].refine if !lines[i].include?(Code[0])
                        i += 1
                        next
                    end

                    # keywords tokens
                    if lines[i].include?(Keywords[0]) # meta
                        if (has_desc = Value(0, lines[i]).index(" ")) != nil
                            meta = Value(0, lines[i]).insert(has_desc, "-").split("-")
                            # for now support only titles and pages overview
                            meta[0] = (meta[0] << NewLine) # title
                            meta[1] = meta[1].lstrip
                            file["TITLE"] = meta[0]
                            file["OVERVIEW"] = meta[1]
                        else
                            meta = Value(0, lines[i])
                            file["TITLE"] = meta
                        end
                        i += 1
                    elsif lines[i].include?(Keywords[1]) # brief
                        file["FUN"] = fun(lines, i)
                        file[Key(1)] = Value(1, lines[i])
                        i += 1
                    elsif lines[i].include?(Keywords[2]) # param
                        file[Key(2)] = Value(2, lines[i])
                        i += 1
                    elsif lines[i].include?(Keywords[3]) # author
                        file[Key(3)] = Value(3, lines[i])
                        i += 1
                    elsif lines[i].include?(Keywords[4]) # details
                        file[Key(4)] = Value(4, lines[i])
                        i += 1
                    else
                        i += 1
                    end
                else
                    i += 1
                end

            end

            @tokens << file
        end

        rm_empty
    end

    private
    def file_ary(file)
        ary = []

        file.each do |line|
            ary << line
        end

        return ary
    end

    def fun(lines, cur_line)
        i = cur_line

        while i < lines.size
            if lines[i].include?("let") && lines[i].include?("fun") && !lines[i].include?('#')
                return lines[i]
            end

            i += 1
        end

        return nil
    end

    def rm_empty
        tmp = []

        @tokens.each do |e|
            next if e == {}
            tmp << e
        end

        @tokens = tmp
    end
end
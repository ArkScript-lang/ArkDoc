#!/usr/bin/env ruby -wKU
#$LOAD_PATH << '.'
#require "Common.rb"

class Lexer
    attr_reader :tokens
    BlockBegin = "####"
    BlockEnd = "###"
    Keywords = ["@meta", "@title", "@desc", "@brief", "@details", "@param", "@author", "---"]

    def initialize
        @ark_path = "../ark/"
        @tokens = []
    end

    def tokenize
        files_paths = Dir.new(@ark_path)

        files_paths.each_child do |file_path|
            tmp = File.new(@ark_path + file_path)
            tmp_tokens = {}.compare_by_identity
            block = false
            #code = false

            tmp.each do |line|
                chunk = cl_line(line)
                #cache = {} # must add in tmp_tokens and clean after function proto generation finished

                # block only
                if chunk.strip == BlockBegin && block == false
                    block = true
                elsif chunk.strip == BlockEnd && block == true
                    block = false
                end

                #puts("chunk 1 :#{chunk}")
                if block
                    #puts("chunk 2 :#{chunk}")
                    chunk = uncomment(chunk)
                    if identifier = chunk[/\A(@[a-z]\w*)/, 1]
                        if Keywords.include?(identifier)
                            #if identifier == KEYWORDS[3]
                            #    next
                            #end

                            id = identifier.lstrip.upcase.delete('@')
                            value = (chunk[identifier.size..-1]).lstrip
                            tmp_tokens[id] = value
                        end
                    end
                end
            end

            @tokens << tmp_tokens
        end
    end

    private
    def cl_line(line)
        cleared_line = line.lstrip

        return cleared_line
    end

    def uncomment(line)
        uncline = line.lstrip.delete('#')

        return uncline
    end

    # generate function prototype
    def prototype_gen(line)
        return protype
    end
end

l = Lexer.new
l.tokenize
#puts(l.tokens)
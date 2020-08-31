#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "common.rb"

class Lexer
    attr_reader :tokens
    BLOCK_BEGIN = "####"
    BLOCK_END = "###"
    KEYWORDS = ["@meta", "@title", "@desc", "@brief", "@details", "@param", "@author", "---"]

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

            tmp.each do |line|
                chunk = cl_line(line)

                if block
                    chunk = uncomment(chunk)

                    if identifier = chunk[/\A(@[a-z]\w*)/, 1]
                        if KEYWORDS.include?(identifier)
                            id = identifier.lstrip.upcase.delete('@')
                            value = (chunk[identifier.size..-1]).delete_at(0)
                            tmp_tokens[id] = value
                        end
                    end
                end

                if chunk.strip == BLOCK_BEGIN && block == false
                    block = true
                elsif chunk.strip == BLOCK_END && block == true
                    block = false
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
        uncline = line.delete('#').lstrip

        return uncline
    end
end
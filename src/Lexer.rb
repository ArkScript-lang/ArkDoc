#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "common.rb"

class Lexer
    attr_reader :tokens, :block
    BLOCK_BEGIN = "####"
    BLOCK_END = "###"
    KEYWORDS = ["@meta", "@title", "@desc", "@brief", "@details", "@param", "@author", "---"]

    def initialize
        @ark_path = "../ark/"
        @tokens = {}.compare_by_identity
    end

    def tokenize
        files_paths = Dir.new(@ark_path)

        files_paths.each_child do |file_path|
            tmp = File.new(@ark_path + file_path)

            tmp.each do |line|
                chunk = cl_line(line)

                if identifier = chunk[/\A(@[a-z]\w*)/, 1]
                    if KEYWORDS.include?(identifier)
                        id = identifier.lstrip.upcase.delete('@')
                        value = (chunk[identifier.size..-1]).delete_at(0)

                        @tokens[id] = value
                    end
                end
            end
        end
    end

    private
    def cl_line(line)
        cleared_line = line.delete('#').lstrip

        return cleared_line
    end
end

l = Lexer.new
puts("===TOKENS===")
l.tokenize
puts(l.tokens)
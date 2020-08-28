#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "common.rb"

class Lexer
    attr_reader :tokens, :block
    BLOCK_BEGIN = "####"
    BLOCK_END = "###"
    KEYWORDS = ["@meta", "@title", "@desc", "@brief", "@details", "@code", "@endcode", "@param", "@author"]

    def initialize(ark_path)
        @ark_path = ark_path
        @files = []
        @block = block
        @tokens = {}
    end

    def tokenize
        i = 0
        block_ary = @block.lines

        while i < block_ary.size
            chunk = block_ary[i]

            if identifier = chunk[/\A(@[a-z]\w*)/, 1]
                if KEYWORDS.include?(identifier)
                    id = identifier.lstrip.upcase.to_sym
                    value = (chunk[identifier.size..-1]).delete_at(0)

                    @tokens[id] = value
                end
            end

            i += 1
        end
    end

    private
    def uncomment
        @block = @block.delete('#')
    end

    def get_files
        ark_path.each { |e|
            @files << File.new(e)
        }
    end

    def get_blocks(str_src)
        
    end
end

l = Lexer.new()
puts("===TOKENS===")
l.tokenize
print(l.tokens)
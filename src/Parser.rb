#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "Lexer.rb"

class Parser

    def initialize
        @lexer = Lexer.new
    end
end
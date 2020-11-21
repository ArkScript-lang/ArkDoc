#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "Lexer.rb"

class Parser
    attr_reader :parsed, :lexer
    def Value(token, key) @lexer.tokens[token][key]; end

    def initialize
        @lexer = Lexer.new
        @parsed = {}
    end

    def parse
        @lexer.tokenize
        i = 0

        while i < @lexer.tokens.size
            file = ""

            for key in @lexer.tokens[i].keys
                case key
                when "TITLE"
                    file = Value(i, key).strip
                    @parsed[file] = ""
                    @parsed[file] << Title
                    @parsed[file] << Value(i, key)
                    next
                when "OVERVIEW"
                    @parsed[file] << NewLine
                    @parsed[file] << Value(i, key)
                    @parsed[file] << NewLine
                when "FUN"
                    @parsed[file] << Function
                    @parsed[file] << function(Value(i, key))
                    @parsed[file] << NewLine
                when "@BRIEF"
                    @parsed[file] << Value(i, key)
                    @parsed[file] << NewLine
                when "@PARAM"
                    param = m_param(Value(i, key))
                    @parsed[file] << Bold
                    @parsed[file] << param[0]
                    @parsed[file] << Bold
                    @parsed[file] << param[1]
                    @parsed[file] << NewLine
                when "CODE"
                    @parsed[file] << Code << NewLine
                    @parsed[file] << Value(i, key)
                    @parsed[file] << Code << NewLine
                when "@AUTHOR"
                    @parsed[file] << "Author : "
                    @parsed[file] << author(Value(i, key))
                    @parsed[file] << NewLine
                when "@DETAILS"
                    @parsed[file] << Details
                    @parsed[file] << Value(i, key).strip
                    @parsed[file] << Details
                    @parsed[file] << NewLine << NewLine
                end
            end

            i += 1
        end
    end

    private
    def fun_format(fun)
        func = fun.gsub("let", "").gsub("fun", "")
        buf = ""

        func.each_char do |chr|
            next if chr == Parenthesis[0] || chr == Parenthesis[1]
            buf << chr
        end

        buf = buf.lstrip.rstrip
        buf.insert(0, Parenthesis[0])
        buf.insert(-1, Parenthesis[1])

        return buf
    end

    def function(token)
        par = 0
        fun = ""

        token.each_char do |chr|
            fun << chr
            break if par == 4
            par += 1 if chr == Parenthesis[0] || chr == Parenthesis[1]
        end

        fun = fun_format(fun)

        return fun
    end

    def author(token)
        name = ""
        i = 0
        slash = 0
        link = ""

        while i < token.size
            slash += 1 if token[i] == '/'
            i += 1
            if slash == 3
                name = token[i..-1]
                break
            end
        end

        link << Brackets[0] << name.rstrip << Brackets[1]
        link << Parenthesis[0] << token.rstrip << Parenthesis[1]

        return link
    end

    def m_param(token)
        name = ""
        details = ""

        token.each_char do |chr|
            break if chr == " "
            name << chr
        end

        details = token[name.size..-1]

        return [name, details]
    end
end
#!/usr/bin/env ruby -wKU
$LOAD_PATH << "src"
$LOAD_PATH << '.'
require "Cli.rb"
require "Generator.rb"

include Cli

# option declaration
option ["-v", "--version"] do
    puts("Version 1.0.1")
    exit(0)
end

option ["-h", "--help"] do
    puts("DESCRIPTION")
    puts("      Lite documentation generator based on Mkdocs")
    puts("")
    puts("SYNOPSIS")
    puts("      ruby ArkDoc.rb -h")
    puts("      ruby ArkDoc.rb -v")
    puts("      ruby ArkDoc.rb -g <site name> [-s <source location>]")
    puts("      ruby ArkDoc.rb -md <site name> [-s <source location>]")
    puts("")
    puts("OPTIONS")
    puts("      -h, --help              Print this help message")
    puts("      -v, --version           Print ArkDoc version and exit")
    puts("      -g, --generate          Generate the website and exit")
    puts("      -md, --markdown         Generate the markdown files and exit")
    puts("      -b, --build             Generate the website using markdown files previously generate with -md option")
    puts("      -s, --source            Set the location of source files")
    puts("")
    puts("LICENCE")
    puts("      Mozilla Public License 2.0")
    exit(0)
end

option ["-s", "--source"]

option ["-g", "--generate"] do
    generator = Generator.new
    name = get("g")
    src =   if called?(["-s", "--source"])
                get("s")
            else
                ""
            end

    Dir.chdir(generator.generate(name, src))
    puts(%x{mkdocs build})
    exit(0)
end

option ["-md", "--markdown"] do
    generator = Generator.new
    name = get("md")
    src =   if called?(["-s", "--source"])
                get("s")
            else
                ""
            end

    generator.generate(name, src)
    exit(0)
end

option ["-b", "--build"] # unusable
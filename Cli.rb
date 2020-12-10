module Cli
    @@options = []
    @@map = {}

    def add
        i = 0

        while i < ARGF.argv.size
            j = 0

            while j < @@options.size
                if ARGF.argv[i] == @@options[j]
                    @@map[@@options[j].delete("-")] = ARGF.argv[i + 1]
                elsif @@options[j].class == ARGF.argv.class
                    k = 0

                    while k < @@options[j].size
                        if ARGF.argv[i] == @@options[j][k]
                            @@map[@@options[j][k].delete("-")] = ARGF.argv[i + 1]
                        end

                        k += 1
                    end
                end

                j += 1
            end

            i += 1
        end
    end

    def option?(pseudo_option)
        return true if @@options.include?(pseudo_option)

        return false
    end

    def get(option)
        if @@map.keys.include?(option)
            return @@map[option]
        else
            keys_ary = []
            (@@options.each {}.to_a.delete_if { |ary| ary.class != Array }).each { |ary|
                keys_ary << [ary[0].delete('-'), ary[1].delete('-')]
            }

            keys_ary.each { |ary|
                ary.each_index { |i|
                    if ary[i] == option
                        case i
                        when 0
                            return @@map[ary[1]]
                        when 1
                            return @@map[ary[0]]
                        end
                    end
                }
            }
        end

        return nil
    end

    def called?(option)
        if option?(option) && @@map.keys.include?(option.delete('-'))
            return true
        end

        if option.class == Array && option?(option)
            if @@map.keys.include?(option[0].delete('-')) || @@map.keys.include?(option[1].delete('-'))
                return true
            end
        end

        return false
    end

    def option(new_option, &block)
        @@options << new_option if !option?(new_option)
        add

        if block_given? && called?(new_option)
            block.call
        end
    end
end
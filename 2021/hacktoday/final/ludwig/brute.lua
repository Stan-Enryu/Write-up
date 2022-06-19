function split_serial(inputstr, sep)
    local count = 0
    if nil == sep then
        sep = "%s"
    end
    local serial = {}
    for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
        table.insert(serial, str)
        count = count + 1
    end
    return serial, count
end
function hex(str)
    return (str:gsub(".", function(c)
        return string.format("%02X", string.byte(c))
    end))
end
function convert(str)
    local value = tonumber(hex(str), 16)
    for i = 1, 1337 do
        value = value ~ value >> 1
    end
    return value
end
io.write([[
INPUT YOUR SERIAL NUMBER !!!
ex: VERY1234-1SECURE1-6SERIAL9
]])
local serial = "VERY1234-1SECURE1-6SERIAL9"
local splitted, length = split_serial(serial, "-")
if 3 == length then
    local secret = {
        9013365925341683735,
        3208797737010034330,
        2619883148120664450
    }
    
    local charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    
    for a in charset:gmatch"." do
        for b in charset:gmatch"." do
            for c in charset:gmatch"." do
                for d in charset:gmatch"." do
                    for e in charset:gmatch"." do
                        for f in charset:gmatch"." do
                            for g in charset:gmatch"." do
                                for h in charset:gmatch"." do
                                    if secret[2] == convert(a .. b .. c .. d .. e .. f .. g .. h) then
                                        io.write(a .. b .. c .. d .. e .. f .. g .. h .. "\n")
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end
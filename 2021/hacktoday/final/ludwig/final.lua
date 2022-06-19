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
local serial = io.read()
local splitted, length = split_serial(serial, "-")
if 3 == length then
  local secret = {
    9013365925341683735,
    3208797737010034330,
    2619883148120664450
  }
  local count = 0
  for k, v in pairs(splitted) do
    local value = convert(v)
    if secret[k] == value then
      count = count + 1
    end
  end
  if 3 == count and 26 == string.len(serial) then
    local flag = ""
    local concatted = table.concat(splitted)
    local more_secret = {
      52,
      38,
      49,
      33,
      47,
      32,
      63,
      47,
      90,
      80,
      63,
      33,
      53,
      52,
      37,
      60,
      93,
      39,
      60,
      33,
      32,
      57,
      35,
      92
    }
    for i = 1, 24 do
      flag = flag .. string.char(more_secret[i] ~ string.byte(concatted, i))
      if 0 == i % 6 then
        flag = flag .. "_"
      end
    end
    flag = flag:sub(1, -2)
    io.write("hacktoday{" .. flag .. "}\n")
  else
    io.write("INVALID SERIAL NUMBER !!!")
  end
else
  io.write("INVALID SERIAL NUMBER !!!")
end
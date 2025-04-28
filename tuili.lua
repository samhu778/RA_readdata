
--MoveAbsJ("R_DR6",K50,v2000,z10,tool0,wobj0,load0)
--MoveAbsJ("R_DL6",K60,v2000,z10,tool0,wobj0,load0)


MoveAbsJ("R_DL6",K80,v2000,z10,tool0,wobj0,load0)
MoveAbsJ("R_DR6",K70,v2000,z10,tool0,wobj0,load0)




local receivedData = nil
local content = nil
--string split
function split(input, delimiter)
    if type(delimiter) ~= "string" or #delimiter <= 0 then
        return
    end
    local start = 1
    local array = {}
    while true do
        local pos = string.find(input, delimiter, start, true)
        if not pos then
            break
        end
        table.insert (array, string.sub (input, start, pos - 1))
        start = pos + string.len (delimiter)
    end
    table.insert (array, string.sub (input, start))
    return array
end

require "SocketApi"

local socketName = "sock1"
local retVal = false
local receivedData = nil

TPWrite("--SocketClient --")
SocketDisconnect(socketName)
Sleep(500)
retVal = SocketConnect(socketName, "192.168.89.122", 8887)
if retVal == 1 then
	TPWrite("Connect successfully")
else
	TPWrite("Connect failed")
	return
end





Sleep(200)
while(1)do
	retVal = SocketSend(socketName, "ready", 2000)
	if retVal ~= 1 then
		TPWrite(string.format("Send failed: %d.", retVal))
		return
	end

retVal, receivedData = SocketReceive(socketName, 0)
	if retVal ~= 1 then
		TPWrite(string.format("Received failed: %d.", retVal))
		return
	end
	TPWrite("Received data: " .. receivedData)

--[[
local fd, err = OpenFile ("1.txt")
while(1)do
local content = ReadFile (fd,"*l")
TPWrite(content)
if content==nil then
	CloseFile (fd)
	Stop()
end
--]]

receivedDataSplit = split(tostring(receivedData),",")	

TPWrite(string.format("receivedDataSplitRobEx, %s", tostring(receivedDataSplit[1])))  
K10.robax.rax_1 = tonumber(receivedDataSplit[1])
K10.robax.rax_2 = tonumber(receivedDataSplit[2]) 
K10.robax.rax_3 = tonumber(receivedDataSplit[3])
K10.robax.rax_4 = tonumber(receivedDataSplit[4])  
K10.robax.rax_5 = tonumber(receivedDataSplit[5])  
K10.robax.rax_6 = tonumber(receivedDataSplit[6]) 

K20.robax.rax_1 = tonumber(receivedDataSplit[7])
K20.robax.rax_2 = tonumber(receivedDataSplit[8]) 
K20.robax.rax_3 = tonumber(receivedDataSplit[9])
K20.robax.rax_4 = tonumber(receivedDataSplit[10])  
K20.robax.rax_5 = tonumber(receivedDataSplit[11])  
K20.robax.rax_6 = tonumber(receivedDataSplit[12]) 
MoveSyncOn("R_DR6","R_DL6")
MoveAbsJ("R_DR6",K20,v2000,z0,tool0,wobj0,load0)
MoveAbsJ("R_DL6",K10,v2000,z0,tool0,wobj0,load0)
MoveSyncRun()
MoveSyncOff()
end
--MoveAbsJ("R_DR6",K40,v2000,fine,tool0,wobj0,load0)
--MoveAbsJ("R_DL6",K30,v2000,fine,tool0,wobj0,load0)


local function GLOBALDATA_DEFINE()
JOINTTARGET("K10",{-1.041,17.246,-95.124,75.877,56.792,59.766,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
JOINTTARGET("K20",{18.031,17.246,-95.124,75.876,47.407,59.766,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
JOINTTARGET("K30",{-119.925,27.828,-94.946,62.858,82.297,24.430,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
JOINTTARGET("K40",{-144.362,27.828,-94.945,62.857,82.298,24.430,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
JOINTTARGET("K50",{-136.042,28.272,-139.945,107.416,82.249,24.418,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
JOINTTARGET("K60",{-1.047,12.908,-129.069,114.165,56.753,59.727,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
JOINTTARGET("K70",{-50.992,39.512,-121.686,27.322,106.682,-7.013,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
JOINTTARGET("K80",{-67.256,37.495,-127.814,6.958,51.342,59.800,0.000},{0.000,0.000,0.000,0.000,0.000,0.000,0.000})
end
print("The end!")
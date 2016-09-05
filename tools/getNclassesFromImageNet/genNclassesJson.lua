require 'torch'
imnet = require 'imagnetClasses'
-- Set 600 classes
n = 100
shuffle = torch.randperm(n)
newList = {}
for i = 1 , n do
   table.insert(newList, imnet[shuffle[i]])
end
f = io.open('imClasses.json','w')
f:write('{')
for i,w in ipairs(newList)do
   f:write('"'..tostring(i)..'":"'..w..'"')
   if i ~= n then f:write(',') end
end
f:write('}')
f:close()
   



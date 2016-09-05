require 'nn'
require 'cunn'
require 'cudnn'
require 'paths'
require 'image'
require 'utils'
local opts = require 'opts'
opt = opts.parse()
print(opt)

function checkClassExist(class)
  for i in pairs(classes) do
    if classes[i] == class then
      return true
    end
  end
  return false
end
function getClass (o, c, i, truepath, falsepath, resizeFail, ver, classIndex)
   local iPath = paths.concat(o,c,i)
   local input
   local eye = 224

   --crop and resizing

   local function resize_image(iPath, dim)
      -- load and rescale image from iPath
      local x = image.load(iPath)
      local dim1 = x:size(1)
      --[[
      if dim1 ~= 3 then
         print('Law image size')
         print(x:size())
      end
      --]]
      -- consider 2-dim image
      x = ((x:dim() == 2) and x:view(1, x:size(1), x:size(2))) or x 

      -- consider greyscale image
      x = ((x:size(1) == 1) and x:repeatTensor(3,1,1)) or x

      -- consider RGBA image
      x = ((x:size(1) > 3) and x[{{1,3},{},{}}]) or x

      local cs , y
      if x:size(2) > x:size(3) then
         cs = x:size(3)
      else
         cs = x:size(2)
      end
      x = image.crop(x,'c',cs,cs)
      y = image.scale(x,eye,eye)
      --[[
      if dim1 ~= 3 then
        --Check input size
        print('Check input size')
        print(y:size())
      end
      --]]
      return y
   end
   --check if it's resized successfully or not
   s =  pcall(function() input = resize_image(iPath, eye) end)
   if not s then table.insert(resizeFail,iPath) end
   if s then
   --   input = torch.FloatTensor(img:size(1),eye,eye)
      local inputDim = input:size(1)
      if inputDim > 3 then inputDim = 3 end
      for ch=1,inputDim do -- channels
         input[ch]:add(-mean[ch])
         input[ch]:div(std[ch])
      end
      input = input:resize(1,3,eye,eye)

      --Do prediction
      model:evaluate()
      model:cuda()
      output = model:forward(input:cuda())
      --Check with classes
      local prob, toPath = 0, nil
      if ver == 1 then
         print(c)
         prob = math.exp(output[1][classIndex])
         print(prob)
         --moves images to corresponding folders based on filter response
         if tonumber(prob) >= opt.th then
            toPath = paths.concat(truepath, i)
            file.copy(iPath, toPath)
            -- print('TRUE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
         else
            toPath = paths.concat(falsepath, i)
            file.copy(iPath, toPath)
            -- print('FALSE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
         end
      else
         probs, indexes = output:topk(1, true, true)
         local index = indexes:squeeze()
         prob = math.exp(probs:squeeze())
         class = classes[index]
      --[[
         print('Class: ')
         print(class)
         print('Probability: ')
         print(prob)
         print('File path: ')
         print(iPath)
       --]]  

         --moves images to corresponding folders based on filter response
         if class == c and tonumber(prob) >= opt.th then
            toPath = paths.concat(truepath, i)
            file.copy(iPath, toPath)
            -- print('TRUE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
         else
            toPath = paths.concat(falsepath, i)
            file.copy(iPath, toPath)
            -- print('FALSE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
         end
      end

   end
end

cutorch.setDevice(opt.GPU) -- by default, use GPU 1
torch.manualSeed(opt.manualSeed)

root    = opt.root
mPath   = paths.concat(root, opt.model)
cPath = paths.concat(root, opt.classes)
sPath    = paths.concat(root, opt.stat)

model   = torch.load(mPath)
classes = torch.load(cPath)
stat    = torch.load(sPath)
std     = stat.std
mean    = stat.mean
flag = false
resizeFail = {}
classIndex = nil 

-- Main loop
filteredTrueDatasetPath = paths.concat(opt.src, 'filteredTrueDataSet'..opt.v)
filteredFalseDatasetPath = paths.concat(opt.src, 'filteredFalseDataSet'..opt.v)
checkPaths(filteredTrueDatasetPath)
checkPaths(filteredFalseDatasetPath)
function checkClassesInModel(classes,c,flag)
   for j in pairs(classes) do
      print(j)
      if classes[j] == c then 
         print('Target class: '..c)
         print(classes[j]..' is in the model class set') 
         flag = true 
         classIndex = j
         break
      else
         flag = false
      end
   end
   return flag, classIndex
end
--Iterates through all subdirectories of dataset folder
for c in paths.files(opt.src) do
   check = checkClassExist(c)
   if c ~= '..' and c ~= '.' and c~= 'filteredFalseDataSet' and c ~= 'filteredTrueDataSet' and check then
      --create folders for correct and incorrect class predictions, ex: sofaTRUE and sofaFALSE
      truepath = paths.concat(filteredTrueDatasetPath, c )
      falsepath = paths.concat(filteredFalseDatasetPath, c )
      --Check path exist if not creath dir
      flag = checkPaths(truepath)
      flag = checkPaths(falsepath)

      -- Check if a target classe and model classe is same if not skip
      flag, classIndex = checkClassesInModel(classes,c,flag)
      -- Check if work has been done with flag is true do work
      if flag then
         p = paths.concat(opt.src, c)
         for i in paths.files(p) do
            if i ~= '..' and i ~= '.' then
               getClass(opt.src, c, i, truepath, falsepath, resizeFail, opt.v, classIndex)
            end
         end
         collectgarbage()
      end
      --print(resizeFail)
   end
end
--Create CSV file to save this table or txt
torch.save(filteredFalseDatasetPath..'resizeFailTable.t7',resizeFail)





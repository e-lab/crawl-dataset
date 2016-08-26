require 'cudnn'
require 'nn'
require 'pl'
require 'paths'
opt = lapp[[
   --model (default none) name of mdoel path
   --root  (default none) name of folder
   ]]

modelPath = paths.concat(opt.root,opt.model)
m = torch.load(modelPath)
m:evaluate()
cudnn.convert(m,nn)
torch.save('cpu_'..opt.model,m)



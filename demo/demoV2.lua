-- loading of a video for torch7
--------------------------------------------------------------------------------
-- Jonghoon, Jin, E. Culurciello, October 9, 2014
--------------------------------------------------------------------------------

require 'pl'
require 'nn'
require 'sys'
require 'image'
--require 'cudnn'
--require 'cunn'
require 'qtwidget'
prediction = require 'prediction'
show       = require 'show'

red = sys.COLORS.red
blu = sys.COLORS.blue
gre = sys.COLORS.green
non = sys.COLORS.none
local video = assert(require("libvideo_decoder"))

-- Options ---------------------------------------------------------------------
opt = lapp[[
-v, --videoPath    (default 'Euge-home-video-small.mp4')    path to video file
-m, --model        (default './models/m_res34_last_aug.t7')
-c, --classes      (default 'classes.t7')
-r, --ratio        (default 0.6)
-b, --batch        (default 3)
-n, --nShow        (default 3)
-s, --stat         (default 'stat.t7')
-t, --th           (default 0.02)
]]

torch.setdefaulttensortype('torch.FloatTensor')
print(opt)
-- load a video and extract frame dimensions
local status, height, width, length, fps = video.init(opt.videoPath)
opt.width  = width
opt.height = height
if not status then
   error("No video")
else
   print('Video statistics: '..height..'x'..width..' ('..(length or 'unknown')..' frames)')
end

-- construct tensor
local dst = torch.Tensor(3, height, width)

-- load model
model_path = opt.model
m = torch.load(model_path)
m:evaluate()
m:add(nn.SoftMax())
stat = torch.load(opt.stat)

-- classes
classes = torch.load(opt.classes)
print(classes)

--init
show:init(opt,classes)
prediction:init(dst, m, stat)

local timer = torch.Timer()
local nb_frames = length or 10
local t_loop = 1

main = function()
   while show.continue() do
      timer:reset()
      video.frame_rgb(dst)
      result = prediction.forward(dst)
      result = result:squeeze()
      if result:dim() == 1 then
         show.process(result, dst, 1/t_loop)
      else
         for i =1 , result:size(1) do
            show.process(result[i], dst, result:size(1)/t_loop)
         end
      end
      t_loop = timer:time().real

      collectgarbage()
   end
   show.close()

   -- free variables and close the video
   video.exit()
end
main()

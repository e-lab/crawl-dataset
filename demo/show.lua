local show = {}

local win
torch.setdefaulttensortype('torch.FloatTensor')
function window_create(opt, classes)
   win_r = opt.ratio
   win_w = opt.width * win_r
   win_h = opt.height * win_r
   batch   = opt.batch
   batch_idx = 0
   nClasses = #classes

   fps_avg      = torch.FloatTensor(batch):zero()
   results      = torch.FloatTensor(nClasses, batch):zero()
   results_mean = torch.FloatTensor(nClasses):fill(-1)
   idx_old      = torch.Tensor(batch):fill(1)
   update_results =
      function(result,batch_idx)
         results[{{},batch_idx}] = result or 0
         if batch_idx == batch then
            results_mean = torch.mean(results,2)
            results_mean = results_mean:squeeze()
         end
      end

   show_n  = opt.nShow
   text_size = 4
   division = 8
   board_x = win_w/division*4
   board_y = win_h/division*4
   board_w = board_x + win_w/division*2
   board_h = board_y + win_h/division*2
   space = (board_h - board_y)/(show_n+ text_size - show_n +1) * 2
   --result_x = board_x + win_w/(1.4*division) + space
   result_x = board_x/2
   result_y = board_y
   fps_x   = result_x
   fps_y   = board_y
   if not win then
      win = qtwidget.newwindow(win_w,win_h,'e-data demo')
   else
      win:resize(win_w,win_h)
   end

   win:setfontsize(space)
   check = 0
   show.process =
      function(result, img, fps)
         result = result:float() or {}
         batch_idx = batch_idx + 1
         if batch_idx > batch then
            batch_idx = 1
         end
         img = image.scale(img, win_w, win_h)
         --print(fps)
         fps_avg[batch_idx] = fps or 0

         update_results(result, batch_idx)

         win:gbegin()
         win:showpage()

         image.display{image = img, win = win, zoom = ratio}

         win:rectangle(board_x,board_y,board_w,board_h)
         win:setcolor(0,0,0,0)
         win:fill()

         win:moveto(fps_x,fps_y)
         win:setcolor(1.0,0.6,0.6)
         win:show(string.format('fps : %.2f', torch.mean(fps_avg)))

         win:setcolor(1.0,0.0,0.0)
         if batch_idx == batch then
            pp, idx = results_mean:sort(1,true)
            idx = idx:squeeze()
         else
            idx = idx_old
         end
         if check > batch then
            for i = 1, show_n do
               local loc_y = result_y + space*i
               win:moveto(result_x,loc_y)
               if pp[i] > opt.th then
                  win:show(string.format('%s %.4f', classes[idx[i]] , pp[i]))
               else
                  win:show(string.format('Not above threshold'))
               end
            end
         end
         check = check + 1
         idx_old = idx
         win:gend()
      end

   show.screen =
      function()
         return win:image()
      end

   show.continue =
      function()
         return win:valid()
      end

   show.close =
      function()
         if win:valid() then
            win:close()
         end
      end
end

function show:init(opt, classes)
   require 'qtwidget'
   window_create(opt,classes)
end

return show

require 'torch'
require 'nn'

require 'LanguageModel'


local cmd = torch.CmdLine()
cmd:option('-checkpoint', 'checkpoints/analogy_cp_20000.t7')
cmd:option('-length', '0')
cmd:option('-start_text', '')
cmd:option('-sample', 1)
cmd:option('-temperature', 0.7)
cmd:option('-gpu', 0)
cmd:option('-gpu_backend', 'opencl')
cmd:option('-verbose', 0)
local opt = cmd:parse(arg)


local checkpoint = torch.load(opt.checkpoint)
local model = checkpoint.model

local msg
if opt.gpu >= 0 and opt.gpu_backend == 'cuda' then
  require 'cutorch'
  require 'cunn'
  cutorch.setDevice(opt.gpu + 1)
  model:cuda()
  msg = string.format('Running with CUDA on GPU %d', opt.gpu)
elseif opt.gpu >= 0 and opt.gpu_backend == 'opencl' then
  require 'cltorch'
  require 'clnn'
  model:cl()
  msg = string.format('Running with OpenCL on GPU %d', opt.gpu)
else
  msg = 'Running in CPU mode'
end
if opt.verbose == 1 then print(msg) end

model:evaluate()

local sample = model:sample(opt)
print(sample)

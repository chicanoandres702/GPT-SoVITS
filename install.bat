mkdir .\GPT_SoVITS\pretrained_models\
cd .\GPT_SoVITS\pretrained_models\
git clone https://huggingface.co/lj1995/GPT-SoVITS
mkdir .\tools\damo_asr
cd .\tools\damo_asr
git clone https://www.modelscope.cn/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch.git
git clone https://www.modelscope.cn/damo/speech_fsmn_vad_zh-cn-16k-common-pytorch.git
git clone https://www.modelscope.cn/damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch.git
mkdir tools/uvr5
cd tools/uvr5
git clone https://huggingface.co/Delik/uvr5_weights
git config core.sparseCheckout true
move GPT_SoVITS/pretrained_models/GPT-SoVITS/* GPT_SoVITS/pretrained_models/

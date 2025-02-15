# from IPython.display import Audio, display
import soundfile as sf
import torch
import numpy as np
from api import StableTTSAPI

device = 'cuda' if torch.cuda.is_available() else 'cpu'

tts_model_path = './checkpoints/checkpoint_9.pt' # path to StableTTS checkpoint
vocoder_model_path = './vocoders/pretrained/firefly-gan-base-generator.ckpt' # path to vocoder checkpoint
vocoder_type = 'ffgan' # ffgan or vocos

# vocoder_model_path = './vocoders/pretrained/vocos.pt'
# vocoder_type = 'vocos'

model = StableTTSAPI(tts_model_path, vocoder_model_path, vocoder_type)
model.to(device)

tts_param, vocoder_param = model.get_params()
print(f'tts_param: {tts_param}, vocoder_param: {vocoder_param}')

ref_audio = '1.wav'
language = 'uzbek' # support chinese, japanese and english
solver = 'midpoint' # recommend using euler, midpoint or dopri5
steps = 30
cfg = 10

while True:
    text = input("Enter text: ")
 
    audio_output, mel_output = model.inference(text, ref_audio, language, steps, 1, 1, solver, cfg)
    audio_output = np.array(audio_output, dtype=np.float32)

    audio_output = np.squeeze(audio_output)
    sf.write("test.wav", audio_output, model.mel_config.sample_rate)

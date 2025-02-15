# # import os
# # import glob
# # import pandas as pd 

# # with open("LJSpeech-1.1/metadata.txt", 'r', encoding="utf-8") as file:
# #     data = file.readlines()


# # with open("filelists/ljspeech.txt", 'a', encoding='utf-8') as ds:
# #     for line in data:
# #         audio, text , _ = line.split("|")
# #         audio_path = f"LJSpeech-1.1/wavs/{audio}.wav"
# #         text = text.lower()

# #         format_text = f"{audio_path.strip()}|{text.strip()}"
# #         ds.write(format_text+"\n")



# from datasets import load_dataset

# # ds_names = [
# #     "blackhole-boys/voice-clone-data-OmarHalil-37-hour",
# #     "blackhole-boys/voice-clone-data-Muhammadjon-5-hour",
# #     "blackhole-boys/voice-clone-data-Charos-33-hour",
# #     "blackhole-boys/voice-clone-data-Muhlisa-39-hour",
# #     "blackhole-boys/TTS-dataset-47-hour"
# #     ]


# # for name in ds_names:

# #     data = load_dataset(name, split='train')

# ds  = load_dataset("aisha-org/AIsha-STT-dataset_v2", token="")
# ds.push_to_hub("blackhole33/full_dataset_v1_140_hours", token="")

from datasets import load_dataset
from tqdm import tqdm 
import soundfile as sf
import os 

# ds = load_dataset("aisha-org/Voice-Clone-splits", cache_dir="./aisha", token="")
# ds.push_to_hub("blackhole33/mixed_speakers_uvc", token="")

ds_names = [

"voice_clone_1",
"voice_clone_2",
"voice_clone_3",
"voice_clone_4",
"voice_clone_5",
"voice_clone_6",
"voice_clone_7",

]
    
for split in ds_names:
    
    ds = load_dataset("aisha-org/Voice-Clone-splits", split=split, cache_dir="./aisha", token="")
    os.makedirs(f"data/{split}", exist_ok=True)

    for line in tqdm(ds):

        audio_path = line['audio']['path']
        audio_array = line['audio']['array']

        audio_simple_rate = line['audio']['sampling_rate']
        text = line['sentence']
        full_audio_path = f"data/{split}/{audio_path}"

        try:

            sf.write(full_audio_path, audio_array, audio_simple_rate)
            text_path = full_audio_path.replace(".mp3", ".lab") if full_audio_path.endswith(".mp3") else full_audio_path.replace(".wav", ".lab")
            with open(f"{text_path}", "w", encoding="utf-8") as df:
                df.write(text.strip()+"\n")

        except:

                pass

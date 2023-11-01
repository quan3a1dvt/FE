from __future__ import absolute_import, division, print_function, unicode_literals
import asyncio
from http.client import HTTPException
import json
from pathlib import Path
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi import Form
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import MySQLdb
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import datetime
import glob
import os
import torch
import numpy as np
import matplotlib.pylab as plt
from Tacotron2PyTorch.text import text_to_sequence
from Tacotron2PyTorch.model.model import Tacotron2
from Tacotron2PyTorch.hparams import hparams as hps
from Tacotron2PyTorch.utils.util import mode, to_arr
from Tacotron2PyTorch.utils.audio import save_wav, inv_melspectrogram
from scipy.io.wavfile import write
from HifiGan.env import AttrDict
from HifiGan.meldataset import MAX_WAV_VALUE
from HifiGan.models import Generator
# from nltk import tokenize
# import nltk
# nltk.download('punkt')
device = None
parent_folder = Path('/Users/quandang/Documents/BTL/HTTM/BE_FastAPI')

    
#HifiGan
hifi_folder = os.path.join(parent_folder, 'HifiGan')
checkpoint_file_path = os.path.join(hifi_folder, 'model','generator_v1')
h = None
def load_checkpoint(filepath, device):
    assert os.path.isfile(filepath)
    print("Loading '{}'".format(filepath))
    checkpoint_dict = torch.load(filepath, map_location=device)
    print("Complete.")
    return checkpoint_dict

config_file = os.path.join(os.path.split(checkpoint_file_path)[0], 'config.json')
with open(config_file) as f:
    data = f.read()
json_config = json.loads(data)
h = AttrDict(json_config)
if torch.cuda.is_available():
    torch.cuda.manual_seed(h.seed)
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
generator = Generator(h).to(device)

state_dict_g = load_checkpoint(checkpoint_file_path, device)
generator.load_state_dict(state_dict_g['generator'])
generator.eval()
generator.remove_weight_norm()



#Tacotron2
tacotron_folder = os.path.join(parent_folder, 'Tacotron2Pytorch')
def load_model(ckpt_pth):
    ckpt_dict = torch.load(ckpt_pth, map_location=torch.device('cpu') )
    model = Tacotron2()
    model.load_state_dict(ckpt_dict['model'])
    model = mode(model, True).eval()
    return model


def infer(text, model):
    sequence = text_to_sequence(text, hps.text_cleaners)
    sequences = mode(torch.IntTensor(sequence)[None, :]).long()
    mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequences)
    return (mel_outputs, mel_outputs_postnet, alignments)
    
ttm_model = load_model(os.path.join(tacotron_folder, 'models','ckpt_200000'))


# # Database configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': '12345678',
#     'db': 'httm',
# }

# # Create a connection to the database
# conn = MySQLdb.connect(**db_config)

app = FastAPI() # gọi constructor và gán vào biến app


@app.get("/audiogen/") 
def download_audio(id: str):
    return FileResponse(os.path.join(parent_folder, 'AudioGen', '{}.wav'.format(id)), media_type="audio/wav", headers={"Content-Disposition": "attachment; filename=generated_audio.mp3"})

@app.get("/tts/")
async def text_to_speech(text: str):
    # You can use asyncio to call the TTS model asynchronously.
    id = await generate_audio_async(text)
    return {"audio_id": id}

@app.post("/model-path/")
async def change_model(ttmPath: str, vocoderPath: str):
    await changeTtmModel(ttmPath)
    await changeVocoderModel(vocoderPath)

async def changeTtmModel(path):
    ttm_model = load_model(os.path.join(tacotron_folder, 'models', path))

async def changeVocoderModel(path):
    checkpoint_file_path = os.path.join(hifi_folder, 'model', path)
    state_dict_g = load_checkpoint(checkpoint_file_path, device)
    generator = Generator(h).to(device)
    generator.load_state_dict(state_dict_g['generator'])
    generator.eval()
    generator.remove_weight_norm()


async def generate_audio_async(text):
    sentence = text
    mels = await generate_mels(sentence)
    audio = await generate_voice(mels)
    curr_dt = datetime.datetime.now()        
    timestamp = int(round(curr_dt.timestamp()))
    output_file = os.path.join(parent_folder, 'AudioGen', '{}.wav'.format(timestamp))
    write(output_file, h.sampling_rate, audio)
    return timestamp

async def generate_mels(sentence):
    output = infer(sentence, ttm_model)
    mel_outputs, mel_outputs_postnet, _ = output
    return mel_outputs_postnet

async def generate_voice(mels):
    with torch.no_grad():
        mel = mels[0]
        y_g_hat = generator(mel)
        audio = y_g_hat.squeeze()
        audio = audio * MAX_WAV_VALUE
        audio = audio.cpu().numpy().astype('int16')
        return audio

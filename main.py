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
    # sequences = [text_to_sequence(sentence, hps.text_cleaners) for sentence in sentences]
    # text_lengths = torch.IntTensor([len(sequence) for sequence in sequences])
    # max_len = max(len(sequence) for sequence in sequences)
    # sequences = [sequence + [0] * (max_len - len(sequence)) for sequence in sequences]
    # sequences = mode(torch.IntTensor(sequences)).long()
    sequence = text_to_sequence(text, hps.text_cleaners)
    sequences = mode(torch.IntTensor(sequence)[None, :]).long()
    mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequences)
    return (mel_outputs, mel_outputs_postnet, alignments)
    
model = load_model(os.path.join(tacotron_folder, 'models','ckpt_200000'))


# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '12345678',
    'db': 'httm',
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)

app = FastAPI() # gọi constructor và gán vào biến app

class Transcript(BaseModel):
    id: int = None
    content: str


class Sample(BaseModel):
    id: int
    audioId: int
    transcriptId: int
    date: datetime.datetime

class TextData(BaseModel):
    text: str

@app.get("/") # giống flask, khai báo phương thức get và url
async def root(): # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return {"message": "Hello World"}

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    cursor = conn.cursor()
    query = "Select * FROM account WHERE username = %s and password = %s"
    cursor.execute(query, (username, password,))
    result = cursor.fetchone()
    cursor.close()
    return {"status" : "success" if result is not None else "failed"}












@app.post("/addtranscript/")
async def add_transcript(name: str = Form(...), content: str = Form(...)):
    cursor = conn.cursor() 
    query = "INSERT INTO transcript (name, content) VALUES (%s, %s)"
    cursor.execute(query, (name, content))
    conn.commit()
    cursor.close()
    return JSONResponse(content={"message": "Add transcript successfully"})

@app.post("/deletetranscript/")
async def delete_sample(id: int = Form(...)):
    cursor = conn.cursor()
    query = "DELETE FROM sample WHERE transcriptId = %s"
    cursor.execute(query, (id,))
    query = "DELETE FROM transcript WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()  
    return JSONResponse(content={"message": "Delete transcript successfully"})

@app.post("/edittranscript/")
async def edit_transcript(id: int = Form(...), name: str = Form(...), content: str = Form(...)):
    cursor = conn.cursor()
    query = "UPDATE transcript SET content = %s, name = %s, lastupdate = CURRENT_TIMESTAMP WHERE id = %s"
    cursor.execute(query, (content, name, id))
    conn.commit()
    cursor.close()    
    return JSONResponse(content={"message": "Update transcript successfully"})  

@app.get("/transcripts/")
def fetch_transcripts(start_idx: int, count: int):
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM transcript"
    cursor.execute(query)
    
    count_transcripts = cursor.fetchone()[0]
    if (start_idx >= count_transcripts):
        return None
    fixed_count = min(count, count_transcripts - start_idx)
    query = "SELECT * FROM transcript LIMIT %s OFFSET %s"
    cursor.execute(query, (fixed_count, start_idx))
    results = cursor.fetchall()
    transcripts = []
    for result in results:
        transcript = {
            "id": result[0],
            "name": result[1],
            "content": result[2],
            "update": result[3],
            "date": result[4]
        }
        transcripts.append(transcript)

    conn.commit()
    cursor.close() 
    return transcripts











@app.post("/addaudio/")
async def add_audio(name: str = Form(...), audio: UploadFile = File(...)):
    file_path = os.path.join(parent_folder, 'Audios', audio.filename)
    with open(file_path, "wb") as file_object:
        shutil.copyfileobj(audio.file, file_object)
    filename, extension = os.path.splitext(audio.filename)
    cursor = conn.cursor() 
    query = "INSERT INTO audio (name, path) VALUES (%s, %s)"
    cursor.execute(query, (name, "Audios/{}".format(audio.filename)))
    conn.commit()
    cursor.close()
    return JSONResponse(content={"message": "Add audio successfully"})

@app.post("/deleteaudio/")
async def delete_sample(id: int = Form(...)):
    cursor = conn.cursor()
    query = "DELETE FROM sample WHERE audioId = %s"
    cursor.execute(query, (id,))
    query = "DELETE FROM audio WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()  
    return JSONResponse(content={"message": "Delete audio successfully"})

@app.post("/editaudio/")
def edit_audio(id: int = Form(...), name: str = Form(...), audio: UploadFile = File(...)):
   
    file_path = os.path.join(parent_folder, 'Audios', audio.filename)
    with open(file_path, "wb") as file_object:
        shutil.copyfileobj(audio.file, file_object)
    filename, extension = os.path.splitext(audio.filename)
    cursor = conn.cursor() 
    query = "UPDATE audio SET name = %s, path = %s, lastupdate = CURRENT_TIMESTAMP WHERE id = %s"
    cursor.execute(query, (name, "Audios/{}".format(audio.filename), id))
    conn.commit()
    cursor.close()    
    return JSONResponse(content={"message": "Update audio successfully"})  

@app.get("/audios/")
def fetch_audios(start_idx: int, count: int):
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM audio"
    cursor.execute(query)
    
    count_audios = cursor.fetchone()[0]
    if (start_idx >= count_audios):
        return None
    fixed_count = min(count, count_audios - start_idx)
    query = "SELECT * FROM audio LIMIT %s OFFSET %s"
    cursor.execute(query, (fixed_count, start_idx))
    results = cursor.fetchall()
    audios = []
    for result in results:
        audio = {
            "id": result[0],
            "name": result[1],
            "update": result[3],
            "date": result[4]
        }
        audios.append(audio)

    conn.commit()
    cursor.close() 
    return audios














@app.get("/transcript-by-name/")
def get_transcript_by_name(name: str):
    cursor = conn.cursor()
    query = "SELECT * FROM transcript WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close() 
    if result is not None:
        return {
            "id": result[0],
            "name": result[1],
            "content": result[2],
            "lastupdate": result[3],
            "date": result[4]
        }
    else:
        raise HTTPException(status_code=404, detail="Transcript name not found")

@app.get("/audio-by-name/")
def get_audio_by_name(name: str):
    cursor = conn.cursor()
    query = "SELECT * FROM audio WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close() 
    if result is not None:
        return {
            "id": result[0],
            "name": result[1],
            "path": result[2],
            "lastupdate": result[3],
            "date": result[4]
        }
    else:
        raise HTTPException(status_code=404, detail="Audio name not found")


@app.post("/addsample/")
async def add_sample(audioId: int = Form(...), transcriptId: int = Form(...)):
    cursor = conn.cursor() 

    query = "INSERT INTO sample (audioId, transcriptId) VALUES (%s, %s)"
    cursor.execute(query, (audioId, transcriptId))

    conn.commit()
    cursor.close()
    return JSONResponse(content={"message": "Add sample successfully"})

@app.post("/deletesample/")
async def delete_sample(id: int = Form(...)):
    cursor = conn.cursor()
    query = "DELETE FROM sample WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()    
    return JSONResponse(content={"message": "Delete sample successfully"})



@app.get("/sample/")
def fetch_sample(id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM sample WHERE id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close() 
    # sample = Sample(id=result[0], audioId=result[1], transcriptId=result[2], date=result[3])
    if result is not None:
        return {
            "id": result[0],
            "audioId": result[1],
            "transcriptId": result[2],
            "date": result[3]
        }
    else:
        raise HTTPException(status_code=404, detail="Sample id not found")

@app.get("/samples/")
def fetch_samples(start_idx: int, count: int):
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM sample"
    cursor.execute(query)
    count_samples = cursor.fetchone()[0]
    if (start_idx >= count_samples):
        return None
    fixed_count = min(count, count_samples - start_idx)
    query = "SELECT * FROM sample LIMIT %s OFFSET %s"
    cursor.execute(query, (fixed_count, start_idx))
    results = cursor.fetchall()


    samples = []
    for result in results:


        sample = {
            "id": result[0],
            "audioId": result[1],
            "transcriptId": result[2],
            "date": result[3]
        }

        query = "SELECT * FROM transcript WHERE id = %s"
        cursor.execute(query, (sample["transcriptId"],))
        result = cursor.fetchone()
        content = result[1]

        query = "SELECT * FROM transcript WHERE id = %s"
        cursor.execute(query, (sample["transcriptId"],))
        result = cursor.fetchone()
        content = result[2]

        sample["content"] = content
        sample["transcriptName"] = result[1]

        query = "SELECT * FROM audio WHERE id = %s"
        cursor.execute(query, (sample["audioId"],))
        result = cursor.fetchone()
        sample["audioName"] = result[1]
        samples.append(sample)

    conn.commit()
    cursor.close() 
    return samples


@app.get("/audio/{id}")
def download_audio(id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM audio WHERE id = %s"
    cursor.execute(query, (id, ))
    audio = cursor.fetchone()
    conn.commit()
    cursor.close() 
    audio_path = audio[2]

    return FileResponse(os.path.join(parent_folder, audio_path), media_type="audio/wav", headers={"Content-Disposition": "attachment; filename={}".format(audio[1])})



@app.post("/editsample/")
def edit_audio(id: int = Form(...), audioId: int = Form(...), transcriptId: int = Form(...)):
    cursor = conn.cursor() 
    query = "UPDATE sample SET audioId = %s, transcriptId = %s WHERE id = %s"
    cursor.execute(query, (audioId, transcriptId, id))
    conn.commit()
    cursor.close()    
    return JSONResponse(content={"message": "Update audio successfully"})  



@app.get("/audiogen/") 
def download_audio(id: str):
    return FileResponse(os.path.join(parent_folder, 'AudioGen', '{}.wav'.format(id)), media_type="audio/wav", headers={"Content-Disposition": "attachment; filename=generated_audio.mp3"})

@app.get("/tts/")
async def text_to_speech(text: str):
    # You can use asyncio to call the TTS model asynchronously.
    id = await generate_audio_async(text)
    return {"audio_id": id}


async def generate_audio_async(text):
    # sentences = text.split('.')
    # sentences = [sentence.strip() for sentence in sentences]
    # print(sentences)
    # audios = []
    # for sentence in sentences:
    sentence = text
    mels = await generate_mels(sentence)
    audio = await generate_voice(mels)
    # if (len(audios) == 0):
    #     audios = audio
    # else:
    #     audios = np.concatenate((audios, audio))

    curr_dt = datetime.datetime.now()        
    timestamp = int(round(curr_dt.timestamp()))
    output_file = os.path.join(parent_folder, 'AudioGen', '{}.wav'.format(timestamp))
    write(output_file, h.sampling_rate, audio)
    return timestamp

async def generate_mels(sentence):
    output = infer(sentence, model)
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


import os
from pathlib import Path
import MySQLdb
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '12345678',
    'db': 'httm',
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)

fdir = Path(r"C:\\Users\\dangv\\Documents\\BTL\\HTTM\\TTS\\LJSpeech-1.1")
f_list = []
with open(os.path.join(fdir, 'metadata.csv'), encoding = 'utf-8') as f:
    for line in f:
        parts = line.strip().split('|')
        wav_path = os.path.join(fdir, 'wavs', '%s.wav' % parts[0])

        cursor = conn.cursor()
        query = "INSERT INTO transcript (content, name) VALUES (%s, %s)"
        cursor.execute(query, (parts[1],parts[0]))
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_insert_id_transcript = cursor.fetchone()

        query = "INSERT INTO audio (name, path) VALUES (%s, %s)"
        cursor.execute(query, (parts[0], "Audios/{}".format('%s.wav' % parts[0])))
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_insert_id_audio = cursor.fetchone()

        query = "INSERT INTO sample (audioId, transcriptId) VALUES (%s, %s)"
        cursor.execute(query, (last_insert_id_audio, last_insert_id_transcript))

        conn.commit()
        cursor.close()
import platform,os,traceback
import ffmpeg
import numpy as np
import subprocess
import gradio as gr
from tools.i18n.i18n import I18nAuto as i18n
import pandas as pd

def load_audio(file, sr):
    try:
        print(file)
        file = clean_path(file)
        if not os.path.exists(file):

            print(f"Audio file not found: {file}")
            # raise RuntimeError(f"Audio file not found: {file}")

        command = [
            "ffmpeg",
            "-nostdin",
            "-threads", "0",
            "-i", file,
            "-f", "f32le",
            "-acodec", "pcm_f32le",
            "-ac", "1",
            "-ar", str(sr),
            "-" # Output to stdout
        ]
        print(command)
        try:
            process = subprocess.run(command, capture_output=True, check=True, text=False) # text=False for raw bytes
            audio_bytes = process.stdout
            audio_array = np.frombuffer(audio_bytes, np.float32).flatten()
            return audio_array
        except:
            return 0

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg subprocess error (return code: {e.returncode}):")
        print(f"Stdout: {e.stdout.decode('utf-8', errors='ignore')}") # Decode stdout if needed
        print(f"Stderr: {e.stderr.decode('utf-8', errors='ignore')}") # **Crucially print stderr**
        raise RuntimeError(f"Failed to load audio via subprocess: FFmpeg error. See stderr output above.")
    except Exception as e:
        traceback.print_exc() # Still print full traceback for other exceptions
        print(f"Unexpected error: {e}")
        # raise RuntimeError(f"Failed to load audio via subprocess: {e}")
    

def clean_path(path_str):
    if platform.system() == 'Windows':
        path_str = path_str.replace('/', '\\')
    return path_str.strip(" ").strip('"').strip("\n").strip('"').strip(" ").strip("\u202a")

def clean_path(path_str: str):
    if path_str is None:
        return ""
    if path_str.endswith(('\\', '/')):
        return clean_path(path_str[0:-1])
    path_str = path_str.replace('/', os.sep).replace('\\', os.sep)
    return path_str.strip(" ").strip('\'').strip("\n").strip('"').strip(" ").strip("\u202a")


def check_for_existance(file_list:list=None,is_train=False,is_dataset_processing=False):
    files_status=[]
    if is_train == True and file_list:
        file_list.append(os.path.join(file_list[0],'2-name2text.txt'))
        file_list.append(os.path.join(file_list[0],'3-bert'))
        file_list.append(os.path.join(file_list[0],'4-cnhubert'))
        file_list.append(os.path.join(file_list[0],'5-wav32k'))
        file_list.append(os.path.join(file_list[0],'6-name2semantic.tsv'))
    for file in file_list:
        if os.path.exists(file):files_status.append(True)
        else:files_status.append(False)
    if sum(files_status)!=len(files_status):
        if is_train:
            for file,status in zip(file_list,files_status):
                # if status:pass
                # else:gr.info(file)
                i18n('以下文件或文件夹不存在')
            return False
        elif is_dataset_processing:
            if files_status[0]:
                return True
            # elif not files_status[0]:
                # gr.info(file_list[0])
            # elif not files_status[1] and file_list[1]:
                # gr.info(file_list[1])
            i18n('以下文件或文件夹不存在')
            return False
        else:
            if file_list[0]:
                # gr.info(file_list[0])
                i18n('以下文件或文件夹不存在')
            else:
                i18n('路径不能为空')
            return False
    return True

def check_details(path_list=None,is_train=False,is_dataset_processing=False):
    if is_dataset_processing:
        list_path, audio_path = path_list
        if (not list_path.endswith('.list')):
            i18n('请填入正确的List路径')
            return
        if audio_path:
            if not os.path.isdir(audio_path):
                i18n('请填入正确的音频文件夹路径')
                return
        with open(list_path,"r",encoding="utf8")as f:
            line=f.readline().strip("\n").split("\n")
        wav_name, _, __, ___ = line[0].split("|")
        wav_name=clean_path(wav_name)
        if (audio_path != "" and audio_path != None):
            wav_name = os.path.basename(wav_name)
            wav_path = "%s/%s"%(audio_path, wav_name)
        else:
            wav_path=wav_name
        if os.path.exists(wav_path):
            ...
        else:
            i18n('路径错误')
        return
    if is_train:
        path_list.append(os.path.join(path_list[0],'2-name2text.txt'))
        path_list.append(os.path.join(path_list[0],'4-cnhubert'))
        path_list.append(os.path.join(path_list[0],'5-wav32k'))
        path_list.append(os.path.join(path_list[0],'6-name2semantic.tsv'))
        phone_path, hubert_path, wav_path, semantic_path = path_list[1:]
        with open(phone_path,'r',encoding='utf-8') as f:
            if f.read(1):...
            else:i18n('缺少音素数据集')
        if os.listdir(hubert_path):...
        else:i18n('缺少Hubert数据集')
        if os.listdir(wav_path):...
        else:i18n('缺少音频数据集')
        df = pd.read_csv(
            semantic_path, delimiter="\t", encoding="utf-8"
        )
        if len(df) >= 1:...
        else:i18n('缺少语义数据集')

from os import mkdir , listdir , system
from os.path import isdir

for word in listdir("./dataset"):
    source_path = "./dataset/"+word
    target_path = "./dataset_format_fixed/"+word

    if(isdir(source_path)):
        mkdir(target_path)
        for audioFile in listdir(source_path):
            srcFilePath = f"{source_path}/{audioFile}"
            destFilePath = f"{target_path}/{audioFile}"

            system(f"ffmpeg -i {srcFilePath} {destFilePath}")

from .utils import *

def convert_files(files_to_convert):
    obj = get_object(files_to_convert)
    
    for key, items in obj.items():
        texts = [process_text(key, item) for item in items]
        save_to_parquet(key, texts, files_to_convert)
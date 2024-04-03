from utils import *

def convert_files():
    obj = get_object()
    
    for key, items in obj.items():
        texts = [process_text(key, item) for item in items]
        save_to_parquet(key, texts)
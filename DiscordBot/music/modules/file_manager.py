from pathlib import Path

BASE_DIR = Path.cwd()

class FileManager(object):
    @staticmethod
    def delete_music (filename):
        file = BASE_DIR.joinpath(filename)
        file.is_file() and file.unlink()
    
    @staticmethod
    def remove_list(list):
        for filename in list:
            filename = BASE_DIR.joinpath(filename)
            filename.unlink()


"""
with open(folder_name + '/' + local_filename, 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)
    print(f'Total: {total}, {index + 1} arquivos baixados, {total - (index + 1)} links restantes')
    with open('progresso.txt', 'w') as progresso:
        progresso.write(str(index + 1))
"""
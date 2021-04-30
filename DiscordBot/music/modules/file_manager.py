from pathlib import Path

BASE_DIR = Path.cwd()

class FileManager(object):
    @staticmethod
    def delete_music (filename):
        try:
            file = Path.joinpath(BASE_DIR, filename)
            if file.is_file():
                file.unlink()
        except Exception as e:
            print(e)

"""
with open(folder_name + '/' + local_filename, 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)
    print(f'Total: {total}, {index + 1} arquivos baixados, {total - (index + 1)} links restantes')
    with open('progresso.txt', 'w') as progresso:
        progresso.write(str(index + 1))
"""
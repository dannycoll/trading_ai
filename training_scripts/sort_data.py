import os
import shutil

current_dirs = ['./data/train/buy', './data/train/sell']

#sorts the images from buy/sell directories into day\(buy/sell) directories
def sort_by_day():
    for current_dir in current_dirs:
        for f in os.listdir(current_dir):
            filename, file_ext = os.path.splitext(f)
            
            try:
                if not file_ext:
                    pass
                elif 'Monday' in filename:
                    shutil.move(
                        os.path.join(current_dir, f'{filename}{file_ext}'),
                        os.path.join(current_dir, 'Monday', f'{filename}{file_ext}')
                    )
                elif 'Tuesday' in filename:
                    shutil.move(
                        os.path.join(current_dir, f'{filename}{file_ext}'),
                        os.path.join(current_dir, 'Tuesday', f'{filename}{file_ext}')
                    )
                elif 'Wednesday' in filename:
                    shutil.move(
                        os.path.join(current_dir, f'{filename}{file_ext}'),
                        os.path.join(current_dir, 'Wednesday', f'{filename}{file_ext}')
                    )
                elif 'Thursday' in filename:
                    shutil.move(
                        os.path.join(current_dir, f'{filename}{file_ext}'),
                        os.path.join(current_dir, 'Thursday', f'{filename}{file_ext}')
                    )
                elif 'Friday' in filename:
                    shutil.move(
                        os.path.join(current_dir, f'{filename}{file_ext}'),
                        os.path.join(current_dir, 'Friday', f'{filename}{file_ext}')
                    )
                elif 'Sunday' in filename:
                    shutil.move(
                        os.path.join(current_dir, f'{filename}{file_ext}'),
                        os.path.join(current_dir, 'Sunday', f'{filename}{file_ext}')
                    )
                elif 'Saturday' in filename:
                    shutil.move(
                        os.path.join(current_dir, f'{filename}{file_ext}'),
                        os.path.join(current_dir, 'Saturday', f'{filename}{file_ext}')
                    )
            except (FileNotFoundError, PermissionError):
                pass

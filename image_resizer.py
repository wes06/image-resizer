from PIL import Image, ImageOps
import os, shutil

if not os.path.exists('2000'):
    os.makedirs('2000')

if not os.path.exists('250'):
    os.makedirs('250')

if not os.path.exists('originals'):
    os.makedirs('originals')





for file in os.listdir('.'):
    if file.endswith('.jpg'):
        print(file)
        img = Image.open(file)
        fn, fext = os.path.splitext(file)

        temp_img = img.copy()
        temp_img.thumbnail((2000, 2000))
        temp_img.save("2000/"+file,"JPEG",optimize=True,quality=85)

        temp_img = img.copy()
        temp_img.thumbnail((4000, 250))
        temp_img.save("250/"+file,"JPEG",optimize=True,quality=100)

        shutil.move(file, 'originals/'+file)

print('\nDone!')
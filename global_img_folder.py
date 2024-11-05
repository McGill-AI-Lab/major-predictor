import os
import shutil

'''
Place all pictures into a single folder, enumerated from 0 to n
'''

#make directories
root = "/Users/ivangaspart/PycharmProjects/majorpredictor/newdata/"
new_root = "/Users/ivangaspart/PycharmProjects/majorpredictor/onefolder/"
os.makedirs(new_root, exist_ok=True)


#copy imgs to the one folder
i = 0
for file in os.listdir(root):
    folder_path = os.path.join(root, file)
    if os.path.isdir(folder_path):
        for img in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img)
            if os.path.isfile(img_path):
                new_name = f"{i}.png"
                shutil.copy(img_path, os.path.join(new_root, new_name))
                i += 1

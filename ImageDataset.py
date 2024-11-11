import os
from matplotlib import pyplot as plt
from PIL import Image
import torch
from torchvision import transforms,utils
from torch.utils.data import Dataset, DataLoader


class ImageDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        try:
            #Load image
            image_path = self.image_paths[idx]
            image = Image.open(image_path).convert('RGB')  #RGB conversion

            #Transformations
            if self.transform:
                image = self.transform(image)

            return image
        except Exception as e:
            print(f"Error loading image {image_path}: {str(e)}")
            return torch.zeros((3, 224, 224))  #zero tensor


def main():
    #1. Specify directory
    base_directory = "enter_directory_here"
    BOOL_BUGTEST = False #Test if the images are well loaded in the dataset with matplotlib.

    #Check if directory exists
    if not os.path.exists(base_directory):
        print(f"Directory '{base_directory}' does not exist.")
        return

    image_paths = []
    #2. Traverse all subdirectories
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.png'):
                full_path = os.path.join(root, file) #concatenation
                image_paths.append(full_path)

    #Check if imgs were found
    if not image_paths:
        print("No images found. Please check the directory and file types.")
        return

    #3. transformations
    transform = transforms.Compose([
        transforms.Resize((224,224)), # High-quality resizing
        transforms.ToTensor(),
    ])
    transform_bugtest = transforms.Compose([
        transforms.Resize((1024), interpolation=Image.LANCZOS),  # High-quality resizing
        transforms.CenterCrop(1024),
        transforms.ToTensor(),
    ])


    #4. Dataset and dataloader
    if not BOOL_BUGTEST:
        dataset = ImageDataset(image_paths, transform=transform)
    else:
        dataset = ImageDataset(image_paths, transform=transform_bugtest)
    print(f"Total images found: {len(dataset)}")

    if len(dataset) > 0:
        dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

        #5. Iterate through dataloader
        if BOOL_BUGTEST:
            for i, batch in enumerate(dataloader):
                img_grid = utils.make_grid(batch)
                plt.figure(figsize=(10, 10),dpi=200)
                plt.imshow(img_grid.permute(1, 2, 0))  # Rearrange for plotting
                plt.title(f"Batch {i}")
                plt.axis("off")
                plt.show()
                if i >= 2:  # Only print first 3 batches for debugging
                    break
        else:
            for i, batch in enumerate(dataloader):
                print(f"Batch {i} shape:", batch.shape)
                if i >= 2:
                    break


    else:
        print("Dataset is empty, cannot create DataLoader.")


if __name__ == "__main__":
    main()

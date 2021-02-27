class AugmentedImagesUtil:
    @staticmethod
    def get_images_file_names_from_folder(folder_images, image_exts):
        """Returns the file names of images in the provided folder"""
        import os
        return [x for x in os.listdir(folder_images) if x.endswith(image_exts)]

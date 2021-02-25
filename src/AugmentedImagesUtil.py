class AugmentedImagesUtil:
    @staticmethod
    def get_images_file_names_from_folder(folder_images, image_exts=(".png", ".jpg")):
        """Returns the file names of images in the provided folder"""
        import os
        return [x for x in os.listdir(folder_images) if x.endswith(image_exts)]

    @staticmethod
    def get_images_file_names_from_folders(folder_sharp, folder_blurred, image_exts=(".png", ".jpg"),):
        """Returns the file names of images that exists in both folders as a list of tuples"""
        import os

        image_sharp_files = AugmentedImagesUtil.get_images_file_names_from_folder(folder_sharp, image_exts)

        for image_blurred_file in image_sharp_files:
            assert os.path.isfile(folder_blurred + image_blurred_file), "Blurred file does not exists for the given image..."

        images_files_paths = []
        for image_file in image_sharp_files:
            images_files_paths.append((image_file, image_file))
        return images_files_paths

    @staticmethod
    def get_section_random_from_two_augmented_images(aug_first, aug_second, section_size=(416, 416)):
        """Returns a tuple of numpy array of a random section of both images with the size specified by section_size"""
        from src.AugmentedImage import AugmentedImage
        import random

        assert (AugmentedImage.get_image_width(aug_first.get_image()) == AugmentedImage.get_image_width(aug_second.get_image()) and
                AugmentedImage.get_image_height(aug_first.get_image()) == AugmentedImage.get_image_height(aug_second.get_image())), "Augmented images have different dimensions..."

        image_width = AugmentedImage.get_image_width(aug_first.get_image())
        image_height = AugmentedImage.get_image_height(aug_first.get_image())
        section_width = section_size[0]
        section_height = section_size[1]

        assert image_width > section_width and image_height > section_height, "Section size bigger than image..."

        x_max = image_width - section_width
        y_max = image_height - section_height

        x = random.uniform(0, x_max)
        y = random.uniform(0, y_max)

        return aug_first.get_section(x, y, section_size), aug_second.get_section(x, y, section_size)

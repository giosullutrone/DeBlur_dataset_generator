class DatasetGenerator:
    def __init__(self, folder_sharp_images,):
        self.__folder_sharp_images = folder_sharp_images
        self.__image_exts = (".jpg", ".png", ".jpeg")

    def set_exts(self, image_exts=(".jpg", ".png", ".jpeg")):
        self.__image_exts = image_exts

    def generate_dataset(self, folder_images_output, number_of_images, section_size=(64, 64), kernel_size=(31, 31), validation_size=0.25):
        import random
        from src.AugmentedImagesUtil import AugmentedImagesUtil

        images_file_names = AugmentedImagesUtil.get_images_file_names_from_folder(self.__folder_sharp_images,
                                                                                  self.__image_exts)

        random.shuffle(images_file_names)

        self.__gen(images_file_names[0:int(len(images_file_names)*(1.0-validation_size))],
                   folder_images_output + "Training/",
                   number_of_images*(1.0 - validation_size),
                   section_size,
                   kernel_size)

        self.__gen(images_file_names[-int(len(images_file_names)*validation_size):],
                   folder_images_output + "Validation/",
                   number_of_images*validation_size,
                   section_size,
                   kernel_size)

    def __gen(self, images_file_names, folder_images_output, number_of_images, section_size=(64, 64), kernel_size=(31, 31)):
        import random
        from src.AugmentedImage import AugmentedImage
        from src.AugmentedImagesUtil import AugmentedImagesUtil
        import os

        os.makedirs(folder_images_output, exist_ok=True)
        os.makedirs(folder_images_output + "Sharp/", exist_ok=True)
        os.makedirs(folder_images_output + "Blurred/", exist_ok=True)

        done = 0

        while done < number_of_images:
            image_file = random.choice(images_file_names)

            aug_sharp = AugmentedImage.from_file(self.__folder_sharp_images + image_file, grayscale=False)

            aug_blurred = AugmentedImage.from_file(self.__folder_sharp_images + image_file, grayscale=False)

            out, inp = AugmentedImagesUtil.get_section_random_from_two_augmented_images(aug_sharp, aug_blurred,
                                                                                        section_size=section_size)

            out = AugmentedImage.blur_an_image(out, kernel_size=kernel_size)

            AugmentedImage.image_to_file(inp, folder_images_output + "Sharp/" + str(done) + ".jpg")
            AugmentedImage.image_to_file(out, folder_images_output + "Blurred/" + str(done) + ".jpg")

            done += 1

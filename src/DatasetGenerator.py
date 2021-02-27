class DatasetGenerator:
    def __init__(self, folder_sharp_images, image_exts=(".jpg", ".png", ".jpeg")):
        self.__folder_sharp_images = folder_sharp_images
        self.__image_exts = image_exts

    def generate_dataset(self, folder_images_output, number_of_images, size, kernel_sizes, full_image, validation_size):
        import random
        from src.AugmentedImagesUtil import AugmentedImagesUtil

        images_file_names = AugmentedImagesUtil.get_images_file_names_from_folder(self.__folder_sharp_images,
                                                                                  self.__image_exts)

        random.shuffle(images_file_names)

        self.__gen(images_file_names[0:int(len(images_file_names)*(1.0-validation_size))],
                   folder_images_output + "Training/",
                   number_of_images*(1.0 - validation_size),
                   size,
                   kernel_sizes,
                   full_image)

        self.__gen(images_file_names[-int(len(images_file_names)*validation_size):],
                   folder_images_output + "Validation/",
                   number_of_images*validation_size,
                   size,
                   kernel_sizes,
                   full_image)

    def __gen(self, images_file_names, folder_images_output, number_of_images, size, kernel_sizes, full_image):
        import os
        import random
        from src.AugmentedImage import AugmentedImage

        os.makedirs(folder_images_output + "Sharp/", exist_ok=True)
        os.makedirs(folder_images_output + "Blurred/", exist_ok=True)

        done = 0

        while done < number_of_images:
            image_file = random.choice(images_file_names)

            aug_sharp = AugmentedImage.image_from_file(self.__folder_sharp_images + image_file, grayscale=False)
            aug_sharp = AugmentedImage.resize_an_image(aug_sharp, size) if full_image else AugmentedImage.get_section_random(aug_sharp, size)

            AugmentedImage.image_to_file(aug_sharp, folder_images_output + "Sharp/" + str(done) + ".jpg")

            aug_blurred = AugmentedImage.blur_an_image_random(aug_sharp, kernel_sizes=kernel_sizes)
            AugmentedImage.image_to_file(aug_blurred, folder_images_output + "Blurred/" + str(done) + ".jpg")

            done += 1

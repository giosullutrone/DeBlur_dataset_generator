class AugmentedImage:
    """Class that lets you manipulate an image"""
    @staticmethod
    def get_image_width(image):
        return image.shape[1]

    @staticmethod
    def get_image_height(image):
        return image.shape[0]

    @staticmethod
    def image_from_file(image_path, grayscale=False):
        """Get image from file path"""
        import cv2
        if grayscale:
            image = cv2.imread(image_path, 0)
        else:
            image = cv2.imread(image_path)
        return image

    @staticmethod
    def blur_an_image(image, kernel_size: int):
        import cv2
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0.0, 0.0)

    @staticmethod
    def blur_an_image_random(image, kernel_sizes: tuple):
        import random
        return AugmentedImage.blur_an_image(image, random.choice(kernel_sizes))

    @staticmethod
    def resize_an_image(image, size):
        import cv2
        return cv2.resize(image, size, interpolation=cv2.INTER_LANCZOS4)

    @staticmethod
    def get_section(image, x, y, section_size):
        """Returns a numpy array of a section of the image with the size specified by section_size starting from (x, y)"""
        image_width = AugmentedImage.get_image_width(image)
        image_height = AugmentedImage.get_image_height(image)
        section_width = section_size[0]
        section_height = section_size[1]

        assert x + section_width <= image_width and y + section_height <= image_height, "Section exceeds image dimensions..."

        return image[int(y):int(y+section_height), int(x):int(x+section_width)]

    @staticmethod
    def get_section_random(image, section_size):
        """Returns a numpy array of a random section of the image with the size specified by section_size"""
        import random

        image_width = AugmentedImage.get_image_width(image)
        image_height = AugmentedImage.get_image_height(image)
        section_width = section_size[0]
        section_height = section_size[1]

        assert image_width >= section_width and image_height >= section_height, "Section size bigger than image..."

        x_max = image_width - section_width
        y_max = image_height - section_height

        x = random.uniform(0, x_max)
        y = random.uniform(0, y_max)

        return AugmentedImage.get_section(image, x, y, section_size)

    @staticmethod
    def image_to_file(image, image_path, image_size=None, grayscale=False, invert=False):
        import cv2

        if image_size is not None:
            image = cv2.resize(image, image_size, interpolation=cv2.INTER_AREA)
        try:
            if grayscale:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            pass
        if invert:
            image = cv2.bitwise_not(image)
        cv2.imwrite(image_path, image)

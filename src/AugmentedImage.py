class AugmentedImage:
    """Class that lets you manipulate an image"""

    def __init__(self, image):
        """Generate augmented image from cv2 image"""
        self.__base_image = image
        self.__image = image

    def get_image(self):
        return self.__image

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
    def from_file(image_path, grayscale=False):
        """Generate an augmented image from file"""
        image = AugmentedImage.image_from_file(image_path, grayscale)
        return AugmentedImage(image)

    def flip_image_horizontally(self):
        """Flip image horizontally"""
        import cv2
        self.__image = cv2.flip(self.__image, 1)

    def flip_image_vertically(self):
        """Flip image vertically"""
        import cv2
        self.__image = cv2.flip(self.__image, 0)

    def blur_image(self, kernel_size=(5, 5), sigmax=0.0, sigmay=0.0):
        """Blur the image with a gaussian filter"""
        import cv2
        self.__image = cv2.GaussianBlur(self.__image, kernel_size, sigmax, sigmay)

    @staticmethod
    def blur_an_image(image, kernel_size=(5, 5), sigmax=0.0, sigmay=0.0):
        import cv2
        return cv2.GaussianBlur(image, kernel_size, sigmax, sigmay)

    def blur_image_random(self, kernel_size_possibles=(3, 5, 7)):
        """Blur the image with a random gaussian filter"""
        import random
        kernel_size = (random.choice(kernel_size_possibles), random.choice(kernel_size_possibles))
        self.blur_image(kernel_size)

    def to_file(self, image_path, image_size=None, grayscale=False, invert=False):
        """Save the image and the boxes to the specified paths"""
        AugmentedImage.image_to_file(self.__image, image_path, image_size=image_size, grayscale=grayscale, invert=invert)

    def get_section(self, x, y, section_size):
        """Returns a numpy array of a section of the image with the size specified by section_size starting from (x, y)"""
        image_width = AugmentedImage.get_image_width(self.__image)
        image_height = AugmentedImage.get_image_height(self.__image)
        section_width = section_size[0]
        section_height = section_size[1]

        assert x + section_width <= image_width and y + section_height <= image_height, "Section exceeds image dimensions..."

        return self.__image[int(y):int(y+section_height), int(x):int(x+section_width)]

    def get_section_random(self, section_size):
        """Returns a numpy array of a random section of the image with the size specified by section_size"""
        import random

        image_width = AugmentedImage.get_image_width(self.__image)
        image_height = AugmentedImage.get_image_height(self.__image)
        section_width = section_size[0]
        section_height = section_size[1]

        assert image_width >= section_width and image_height >= section_height, "Section size bigger than image..."

        x_max = image_width - section_width
        y_max = image_height - section_height

        x = random.uniform(0, x_max)
        y = random.uniform(0, y_max)

        return self.get_section(x, y, section_size)

    def get_sections_annotated(self, section_size):
        """Returns a tuple containing all possible sections of the image, as (x, y, np array)"""
        image_width = AugmentedImage.get_image_width(self.__image)
        image_height = AugmentedImage.get_image_height(self.__image)
        section_width = section_size[0]
        section_height = section_size[1]

        assert image_width >= section_width and image_height >= section_height, "Section size bigger than image..."

        number_of_sections_x = (image_width - section_width / 2) / section_width
        number_of_sections_y = (image_height - section_height / 2) / section_height

        sections = []

        for i in range(int(number_of_sections_x) * 2):
            for j in range(int(number_of_sections_y) * 2):
                x = int(i*section_width / 2)
                y = int(j*section_height / 2)

                sections.append((x, y, self.get_section(x, y, section_size))) #todo: Change this

        #Get overlapping sections if needed
        if number_of_sections_x - int(number_of_sections_x) > 0:
            for j in range(int(number_of_sections_y)):
                x = image_width - section_width
                y = int(j*section_height)

                sections.append((x, y, self.get_section(x, y, section_size)))

        if number_of_sections_y - int(number_of_sections_y) > 0:
            for i in range(int(number_of_sections_x)):
                x = int(i*section_width)
                y = image_height - section_height

                sections.append((x, y, self.get_section(x, y, section_size)))

        if number_of_sections_x - int(number_of_sections_x) > 0 and number_of_sections_y - int(number_of_sections_y) > 0:
            x = image_width - section_width
            y = image_height - section_height

            sections.append((x, y, self.get_section(x, y, section_size)))
        return sections

    def image_from_sections_annotated(self, sections):
        """Overwrite image with the pixels from annotated sections"""
        section_width = sections[0][2].shape[1]
        section_height = sections[0][2].shape[0]
        for section in sections:
            x, y, section_image = section
            self.__image[y:y+section_height, x:x+section_width] = section_image
        return self.__image

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

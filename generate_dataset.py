if __name__ == "__main__":
    import argparse
    from src.DatasetGenerator import DatasetGenerator
    from src.Util import get_fixed_path

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_folder", help="From where to load the sharp images", type=str, required=True)
    parser.add_argument("-o", "--output_folder", help="Where to save the sharp and blurred images", type=str, required=True)

    parser.add_argument("-n", "--number_of_images", help="How many inputs to generate", type=int, required=True)

    parser.add_argument("-k", "--kernel_size", help="Kernel size of the gaussian blur", nargs=2, type=int, required=False,
                        default=(9, 9))
    parser.add_argument("-s", "--size", help="Size of each patch", nargs=2, type=int, required=False,
                        default=(224, 224))

    parser.add_argument("-v", "--validation_size", help="Validation size compared to training size", type=float, required=False,
                        default=0.25)

    args = parser.parse_args()

    assert 0.0 < args.validation_size < 1.0, "Validation size should be between 0.0 and 1.0..."

    input_folder = get_fixed_path(args.input_folder, replace_backslash=True, add_backslash=True)
    output_folder = get_fixed_path(args.output_folder, replace_backslash=True, add_backslash=True)

    gen = DatasetGenerator(folder_sharp_images=input_folder)

    gen.generate_dataset(folder_images_output=output_folder,
                         number_of_images=args.number_of_images,
                         section_size=tuple(args.size),
                         kernel_size=tuple(args.kernel_size),
                         validation_size=args.validation_size)

import os


def convert_to_txt(input_file, output_file):
    try:
        # Open the input file
        with open(input_file, 'rb') as file:
            # Read the contents

            file_contents = file.read()

        # Open a new text file for writing
        with open(output_file, 'wb') as _file:
            # Write the contents to the text file
            _file.write(file_contents)

        print(f"Conversion successful. Text file saved as {output_file}")
        return output_file

    except Exception as e:
        print(f"Error: {e}")


def convert_to_txt_limit(input_file, output_file, limit):
    try:
        size = os.path.getsize(input_file)
        read = 0
        out = []
        counter = 0
        with open(input_file, 'rb') as file:

            while read < size:
                file_contents = file.read(limit)
                with open(output_file + f"_{counter}", 'wb') as txt_file:
                    out.append(output_file + f"_{counter}")
                    txt_file.write(file_contents)
                counter += 1
                read += limit

        # print(f"Conversion successful. Text file saved as {output_file}")
        return out

    except Exception as e:
        print(f"Error: {e}")


def convert_to_original(output_file, input_file):
    try:
        # Open the text file for reading
        with open(input_file, 'rb') as txt_file:
            # Read the contents
            txt_contents = txt_file.read()

        # Open the original file for writing
        with open(output_file, 'wb') as output_file:
            # Write the contents back to the original file
            output_file.write(txt_contents)

        print(f"Conversion successful. Data restored to {output_file}")
        return output_file

    except Exception as e:
        print(f"Error: {e}")


def convert_to_original_limit(output_file, input_file):
    try:
        counter = 0
        data = []
        while os.path.isfile(input_file + f"_{counter}"):
            with open(input_file + f"_{counter}", 'rb') as txt_file:
                # Read the contents
                txt_contents = txt_file.read()
                data.append(txt_contents)
            counter += 1

        # Open the original file for writing
        with open(output_file, 'wb') as file:
            # Write the contents back to the original file
            while data:
                file.write(data.pop(0))

        # print(f"Conversion successful. Data restored to {output_file}")
        return output_file

    except Exception as e:
        print(f"Error: {e}")

# outputs=convert_to_txt_limit("input.mp4", "output", 24_000_000)
# convert_to_original_limit("output.mp4", "output")
import os


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

        return out

    except Exception as e:
        print(f"Error: {e}")


def convert_to_original_limit(output_file, input_file):
    try:
        counter = 0
        data = []
        while os.path.isfile(input_file + f"_{counter}"):
            with open(input_file + f"_{counter}", 'rb') as txt_file:
                txt_contents = txt_file.read()
                data.append(txt_contents)
            counter += 1

        with open(output_file, 'wb') as file:
            while data:
                file.write(data.pop(0))

        return output_file

    except Exception as e:
        print(f"Error: {e}")

def create_path(file_path, valid_paths):
    new_path = "/".join(file_path.split("/")[:-1])
    dirs = new_path.split("/")
    intermediate_path = ""
    while intermediate_path != new_path:
        intermediate_path += "/" + dirs.pop(0)
        if intermediate_path[0]=="/":
            intermediate_path = intermediate_path[1:]
        if intermediate_path in valid_paths:
            continue
        try:
            os.mkdir(intermediate_path, mode = 0o777, dir_fd = None)
        except FileExistsError:
            pass
        valid_paths[intermediate_path] = True
    try:
        os.mkdir(intermediate_path, mode = 0o777, dir_fd = None)
    except FileExistsError:
        pass
    valid_paths[intermediate_path] = True
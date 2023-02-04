"""
Just stitches together two logs into one, based on a folder from a .dscjson config
"""

# how it now works is two files are selected, and their combination is written into the first file
import frontend
import table


def main(fp1=None, fp2=None):
    CONF = frontend.load_config()
    table.init(CONF)

    if (fp1 is None) and (fp2 is None):
        items = table.find_json()
        print("Availible files to combine:")
        for i, file in enumerate(items):
            print(f"{i} - {file}")
        print("input number of first file to combine:")
        int_file1 = int(input())
        print("input number of second file to combine:")
        int_file2 = int(input())
        file1 = table.read(items[int_file1])
        file2 = table.read(items[int_file2])
    else:
        file1 = table.read(fp1)
        file2 = table.read(fp2)
    file2["messages"] += file1["messages"]
    with open(f"{CONF.dest_folder}{table.os.sep}{items[int_file1]}.json", "w", encoding="UTF-8") as f:
        table.json.dump(file2, f)


if __name__ == "__main__":
    main()

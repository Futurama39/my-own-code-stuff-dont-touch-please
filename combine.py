'''
Just stitches together two logs into one, based on a folder from a .dscjson config
'''

# how it now works is two files are selected, and their combination is written into the first file
import frontend
import table
def main(int_file1= None, int_file2= None):
    CONF = frontend.load_config()
    table.init(CONF)
    items = table.find_json()
    if (int_file1 is None) or (int_file2 is None):
        print('Availible files to combine:')
        for i, file in enumerate(items):
            print(f'{i} - {file}')
        print('input number of first file to combine:')
        int_file1 = int(input())
        print('input number of second file to combine:')
        int_file2 = int(input())
    file1 = table.read(items[int_file1])
    file2 = table.read(items[int_file2])
    file2['messages'] += file1['messages']
    with open(f'{CONF.dest_foler}{table.os.sep}{items[int_file1]}.json', 'w', encoding='UTF-8') as f:
        table.json.dump(file2, f)


if __name__ == '__main__':
    main()
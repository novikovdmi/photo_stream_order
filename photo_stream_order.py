import sys
import sqlite3
from os import listdir, mkdir
from os.path import isfile, isdir, expanduser
from shutil import copyfile

db = sqlite3.connect(expanduser("~")+"\\Application Data\\Apple Computer\\MediaStream\\local.db")

def get_num(check_sum):
    result = db.execute("select assetnumber, dateCreated, batchcreatedate from MSASAlbumAssets where checksum=?", (check_sum,)).fetchone()
    return str(result[1])+'-'+str(result[0]) if not (result is None) else None


def put_in_order(dir_name):
    if not isdir(dir_name):
        print('"%s" is not directory name!' % dir_name)

    print('Process "%s"...' % dir_name)

    files = list(filter(lambda x: isfile(dir_name + "\\" + x), listdir(dir_name)))
    print('%d files found' % len(files))

    dir_num = 0
    dest_dir = dir_name + '\\' + "ordered"
    while dir_num < 1000:
        if not isdir(dest_dir):
            mkdir(dest_dir)
            print('Destination directory "%s"' % dest_dir )
            break
        dir_num += 1
        dest_dir = dir_name + '\\' + "ordered" + str(dir_num)
    else:
       print( "Can't make destination directory \"%s\"" % dest_dir )
       return False

    processed = 0
    skipped = 0
    for f in files:
        num = get_num(f[:f.find('.')])
        if num is None:
            print('\nSkipped "%s"\n' % f)
            skipped += 1
        else:
            copyfile(dir_name+'\\'+f, dest_dir+'\\'+str(num)+'-'+f)
            print('%s => %s' % (f, num))
            processed += 1

    print('Processed %d files, skipped %d files' % (processed, skipped))
    return

if len(sys.argv) <= 1:
    print("photo_stream_order SharedPhotoStreamDirectory")
else:
    put_in_order(sys.argv[1])


import os

def splitfile(filepath, linesize=3000):
    filedir, name = os.path.split(filepath)
    name, ext = os.path.splitext(name)
    filedir = os.path.join(filedir, name)
    if not os.path.exists(filedir):
        os.mkdir(filedir)

    partno = 0
    stream = open(filepath, 'r', encoding='utf-8')
    while True:
        partfilename = os.path.join(filedir, name + '_' + str(partno) + ext)
        print('write start %s' % partfilename)
        part_stream = open(partfilename, 'w', encoding='utf-8')

        read_count = 0
        while read_count < linesize:
            read_content = stream.readline()
            if read_content:
                part_stream.write(read_content)
            else:
                break
            read_count += 1

        part_stream.close()
        if (read_count < linesize):
            break
        partno += 1

    print('done')


if __name__ == '__main__':
    splitfile('acsi_postid.txt', 3000)
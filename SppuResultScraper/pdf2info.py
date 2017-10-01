import argparse
import os, sys
from pandas import read_csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--input',
            type=str,
            default='',
            help='PDF containing list of names and roll numbers.'
            )
    FLAGS, unparsed = parser.parse_known_args()
    
    if FLAGS.input:
    
        os.system("pdftotext " + FLAGS.input)

        with open(FLAGS.input[:-4] + '.txt', 'r') as ip:
            i = 0
            for line in ip:
                if i == 21:
                    break
                i = i + 1

            output = "Seat number,Student name,Mother,PRN"
            temp = ip.read()
        temp = temp.replace(' ..', '').replace('\n',' ').split()
        i = 0
        for word in temp:
            #print(word)
            if word.startswith('S150'):
                output= output + '\n' + word + ','
                i = 0
                continue
            if word.startswith('71') or word == 'Fresh':
                output = output + ',' + word
                continue
            if i == 3:
                output = output + ','
            output = output + word + ' '
            i = i + 1 
        with open('Name List.csv', 'w+') as op:
            op.write(output)

    df = read_csv('Name List.csv')
    
    matrix = df[['Seat number', 'Mother']].as_matrix()
    for i in range(len(matrix)):
        matrix[i][1] = matrix[i][1].replace('.','')
    import pickle
    pickle.dump(matrix, open('student_info.p','wb'))

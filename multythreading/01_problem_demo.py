from multythreading.count_three_sum import read_ints, count_three_sum

if __name__ == '__main__':
    print('started main')
    ints = read_ints("..\\data\\1Kints.txt")
    print('what are you waiting for?')
    count_three_sum(ints)
    print('all done')

# до тех пор, пока count_three_sum(ints) не будет исполнен, взаимодействие юзера и программы прекращаеся
# это мб плохо
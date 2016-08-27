import random
from itertools import combinations


master = [0]*2001
total_count = [0]


def fill_master(size):
    for i in range(1, size + 1):
        master[i] = random.randint(0,1)

    # for i in range(1, size, 4):
    #     print(master[i:i+4], end=" ")
    # print()


def check_solution(solution, master_size):
    if solution < 0 or solution > master_size:
        raise ValueError("Solution not in range: " + str(solution))

    total = sum(master)

    if float(total) == master_size/2:
        return solution == 0
    elif total > master_size/2:
        return master[solution] == 1
    else:
        return master[solution] == 0


def QCOUNT(test):
    for i in range(4):
        if test[i] < 1:
            raise  ValueError("not a valid query")

    count = master[test[0]] + master[test[1]] + master[test[2]] + master[test[3]]

    total_count[0] += 1

    if count == 2:
        return 0
    elif count == 1 or count == 3:
        return 2
    elif count == 0 or count == 4:
        return 4


def compare_fours(one, two):
    return False if QCOUNT([one[0], one[1], two[0], two[1]]) == 0 else True


def compare_two_threes(oracle, three1, three2, count_ones, count_zeros, zero_index):
    size2 = QCOUNT([three1[2], three1[3], three2[0], three2[1]])

    if size2 == 4:
        if QCOUNT([oracle[0], oracle[1], three2[0], three2[1]]) == 4:
            if zero_index == -1:
                if QCOUNT([oracle[0], oracle[1], oracle[2], three2[2]]) == 4:
                    return count_ones + 6, count_zeros + 2, three2[3]
                else:
                    return count_ones + 6, count_zeros + 2, three2[2]
            else:
                return count_ones + 6, count_zeros + 2, zero_index
        else:
            return count_ones + 2, count_zeros + 6, three2[0]
    elif size2 == 0:
        res = QCOUNT([three1[0], three1[1], three2[2], three2[3]])

        if res == 0:
            if zero_index == -1:
                for i in range(3):
                    if QCOUNT([oracle[0], oracle[1], oracle[2], three2[i]]) == 3:
                        return count_ones + 4, count_zeros + 4, three2[i]
                return count_ones + 4, count_zeros + 4, three2[3]
            else:
                return count_ones + 4, count_zeros + 4, zero_index
        elif res == 4:
            sec_res = QCOUNT([oracle[0], oracle[1], three2[2], three2[3]])

            if sec_res == 4:
                if zero_index == -1:
                    if QCOUNT([oracle[0], oracle[1], oracle[2], three2[0]]) == 3:
                        return count_ones + 6, count_zeros + 2, three2[0]
                    else:
                        return count_ones + 6, count_zeros + 2, three2[1]
                else:
                    return count_ones + 6, count_zeros + 2, zero_index
            elif sec_res == 0:
                if zero_index == -1:
                    return count_ones + 2, count_zeros + 6, three2[3]
                else:
                    return count_ones + 2, count_zeros + 6, zero_index
            else:
                raise ValueError('sec_res should never be a 2!')
        else:
            raise ValueError('res should never be a 2!')
    else:
        dont_check = [[] for i in range(16)]
        dont_check_count = 2

        test = [three1[2], three1[3], three2[0], three2[1]]
        for i in range(4):
            dont_check[0].append(test[i])

        test = [three1[0], three1[1], three2[2], three2[3]]
        for i in range(4):
            dont_check[1].append(test[i])

        size3 = 0
        save = []

        count = 0
        out_of_inner = 0
        for comb in combinations(three1, 2):
            for comb2 in combinations(three2, 2):
                save = [comb[0], comb[1], comb2[0], comb2[1]]

                do_check = 1

                for l in dont_check:
                    if len(l) != 0:
                        if set(save) == set(l):
                            do_check = 0

                if do_check == 1:
                    size3 = QCOUNT(save)
                    count += 1

                    if size3 == 4 or size3 == 0:
                        out_of_inner = 1
                        break

                first = [x for x in three1 if x != comb[0] and x != comb[1]]
                sec = [x for x in three2 if x != comb2[0] and x != comb2[1]]
                test = [first[0], first[1], sec[0], sec[1]]
                for i in range(4):
                    dont_check[dont_check_count].append(test[i])
                dont_check_count += 1

            if out_of_inner == 1:
                break

        other_three1 = [i for i in three1 if i not in save]
        other_three2 = [i for i in three2 if i not in save]

        three1 = other_three1 + [save[0], save[1]]
        three2 = [save[2], save[3]] + other_three2

        if size3 == 4:
            if QCOUNT([oracle[0], oracle[1], three2[0], three2[1]]) == 4:
                if zero_index == -1:
                    if QCOUNT([oracle[0], oracle[1], oracle[2], three2[2]]) == 4:
                        return count_ones + 6, count_zeros + 2, three2[3]
                    else:
                        return count_ones + 6, count_zeros + 2, three2[2]
                else:
                    return count_ones + 6, count_zeros + 2, zero_index
            else:
                return count_ones + 2, count_zeros + 6, three2[0]
        elif size3 == 0:
            res = QCOUNT([three1[0], three1[1], three2[2], three2[3]])

            if res == 0:
                if zero_index == -1:
                    for i in range(3):
                        if QCOUNT([oracle[0], oracle[1], oracle[2], three2[i]]) == 3:
                            return count_ones + 4, count_zeros + 4, three2[i]
                    return count_ones + 4, count_zeros + 4, three2[3]
                else:
                    return count_ones + 4, count_zeros + 4, zero_index
            elif res == 4:
                sec_res = QCOUNT([oracle[0], oracle[1], three2[2], three2[3]])

                if sec_res == 4:
                    if zero_index == -1:
                        if QCOUNT([oracle[0], oracle[1], oracle[2], three2[0]]) == 3:
                            return count_ones + 6, count_zeros + 2, three2[0]
                        else:
                            return count_ones + 6, count_zeros + 2, three2[1]
                    else:
                        return count_ones + 6, count_zeros + 2, zero_index
                elif sec_res == 0:
                    if zero_index == -1:
                        return count_ones + 2, count_zeros + 6, three2[3]
                    else:
                        return count_ones + 2, count_zeros + 6, zero_index
                else:
                    raise ValueError('sec_res should never be a 2!')
            else:
                raise ValueError('res should never be a 2!')


def check_threes(oracle, count_ones, count_zeros, logical_size, three_indices, zero_index):
    to_remove = []
    for i, index in enumerate(three_indices):
        if i % 2 == 1:
            to_remove.append(index)
            to_remove.append(three_indices[i-1])
            three1 = []
            three2 = []
            for j in range(4):
                three1.append(index + j)
                three2.append(three_indices[i - 1] + j)

            count_ones, count_zeros, zero_index = compare_two_threes(oracle,
                                                                     three1,
                                                                     three2,
                                                                     count_ones,
                                                                     count_zeros,
                                                                     zero_index)

            if check_sizes(count_ones, count_zeros, logical_size) == -1:
                return oracle[0], -1, -1, -1, -1
            elif check_sizes(count_ones, count_zeros, logical_size) == -2:
                return zero_index, -1, -1, -1, -1
            elif check_sizes(count_ones, count_zeros, logical_size) == -3:
                return 0, -1, -1, -1, -1

    if len(three_indices) % 2 == 1:
        return -1, count_ones, count_zeros, three_indices[-1], zero_index
    else:
        return -1, count_ones, count_zeros, -1, zero_index


def check_sizes(count_ones, count_zeros, logical_size):
    if float(count_ones) > logical_size / 2.0:
        return -1
    elif float(count_zeros) > logical_size / 2.0:
        return -2
    elif count_ones == count_zeros and count_ones + count_zeros == logical_size:
        return -3
    else:
        return 1


def get_solution(size):
    oracle = [-1, -1, -1, -1]
    logical_size = size
    my_array = [1, 2, 3, 4]
    current_four = [[-1, -1, -1, -1],[-1, -1, -1, -1]]
    current_four_size = 0
    count_ones = 0
    count_zeros = 0
    zero_index = -1
    three_indices = []
    checked_threes = 0

    num_four_blocks = 0
    num_three_blocks = 0
    two_block = [-1, -1, -1, -1]

    current_three = [[-1, -1, -1, -1],[-1, -1, -1, -1]]
    current_three_size = 0

    for i in range(int(size / 4)):
        check = QCOUNT(my_array)

        if check == 0:
            logical_size -= 4 # every time logical_size is decreased, should check to see if we have enough ones/zeros

            if check_sizes(count_ones, count_zeros, logical_size) == -1:
                return oracle[0]
            elif check_sizes(count_ones, count_zeros, logical_size) == -2:
                return zero_index
            elif check_sizes(count_ones, count_zeros, logical_size) == -3:
                return 0

            if two_block[0] == -1:
                for i in range(4):
                    two_block[i] = my_array[i]
        elif check == 4:
            num_four_blocks += 1

            if oracle[0] == -1:
                for i in range(4):
                    oracle[i] = my_array[i]

            for i in range(4):
                current_four[current_four_size][i] = my_array[i]
            current_four_size += 1

            if current_four_size == 2:
                current_four_size = 0

                check = QCOUNT([oracle[0], oracle[1], current_four[0][0], current_four[1][0]])

                if check == 4:
                    count_ones += 8
                elif check == 0:
                    count_zeros += 8
                    zero_index = current_four[0][0]
                else:
                    logical_size -= 8

                if check_sizes(count_ones, count_zeros, logical_size) == -1:
                    return oracle[0]
                elif check_sizes(count_ones, count_zeros, logical_size) == -2:
                    return zero_index
                elif check_sizes(count_ones, count_zeros, logical_size) == -3:
                    return 0
        elif check == 2:
            num_three_blocks += 1

            if oracle[0] == -1:
                three_indices.append(my_array[0])
            else:
                if checked_threes == 0:
                    checked_threes = 1

                    check, count_ones, count_zeros, three_index, zero_index = check_threes(oracle,
                                                                                           count_ones,
                                                                                           count_zeros,
                                                                                           logical_size,
                                                                                           three_indices,
                                                                                           zero_index)

                    if check != -1:
                        return check

                    if three_index != -1:
                        for i in range(4):
                            current_three[0][i] = three_index + i
                        current_three_size += 1

                three_indices.append(my_array[0])

                for i in range(4):
                    current_three[current_three_size][i] = my_array[i]

                current_three_size += 1

                if current_three_size == 2:
                    current_three_size = 0

                    count_ones, count_zeros, zero_index = compare_two_threes(oracle,
                                                                 current_three[0],
                                                                 current_three[1],
                                                                 count_ones,
                                                                 count_zeros,
                                                                 zero_index)

                    if check_sizes(count_ones, count_zeros, logical_size) == -1:
                        return oracle[0]
                    elif check_sizes(count_ones, count_zeros, logical_size) == -2:
                        return zero_index
                    elif check_sizes(count_ones, count_zeros, logical_size) == -3:
                        return 0

        my_array[0] += 4
        my_array[1] += 4
        my_array[2] += 4
        my_array[3] += 4

    # Below this point is all of the code to deal with the cases of not finding a majority when looking through
    #   all of the n/4 blocks.

    if num_four_blocks == 0 and num_three_blocks == 0:
        return 0

    if num_four_blocks == 1 and num_three_blocks == 0:
        return oracle[0]

    if num_four_blocks == 1:
        count_ones += 4

        if checked_threes == 0:
            check, count_ones, count_zeros, three_index, zero_index = check_threes(oracle,
                                                                                   count_ones,
                                                                                   count_zeros,
                                                                                   logical_size,
                                                                                   three_indices,
                                                                                   zero_index)


            if check != -1:
                return check

            if three_index != -1 or num_three_blocks == 1:

                count_for = 0
                count_opp = 0

                for i in range(4):
                    if QCOUNT(oracle[1:] + [three_indices[-1] + i]) == 4:
                        count_for += 1
                    else:
                        count_opp += 1

                    if count_for == 2 or count_opp == 2:
                        break

                if count_for == 2:
                    count_ones += 3
                    count_zeros += 1
                else:
                    count_ones += 1
                    count_zeros += 3


        if checked_threes != 0 and num_three_blocks % 2 == 1:
            count_for = 0
            count_opp = 0
            for i in range(4):
                if QCOUNT([oracle[0], oracle[1], oracle[2], current_three[0][i]]) == 4:
                    count_for += 1
                else:
                    count_opp += 1
                    zero_index = current_three[0][i]
                if (count_for >= 2 or count_opp >= 2) and zero_index != -1:
                    break

            if count_for >= 2:
                count_ones += 3
                count_zeros += 1
            else:
                count_ones += 1
                count_zeros += 3

        if count_zeros == count_ones:
            return 0
        elif count_zeros > count_ones:
            return zero_index
        else:
            return oracle[0]

    if num_four_blocks % 2 == 1:
        if compare_fours(oracle, current_four[0]):
            count_ones += 4
        else:
            count_zeros += 4

        if num_three_blocks % 2 == 1:
            count_for = 0
            count_opp = 0
            for i in range(3):
                if QCOUNT([oracle[0], oracle[1], oracle[2], current_three[0][i]]) == 4:
                    count_for += 1
                else:
                    count_opp += 1
                if count_for == 2 or count_opp == 2:
                    break

            if count_for == 2:
                count_ones += 3
                count_zeros += 1
            else:
                count_ones += 1
                count_zeros += 3

        if count_ones > count_zeros:
            return oracle[0]
        elif count_ones < count_zeros:
            return zero_index
        else:
            return 0

    if num_four_blocks % 2 == 0 and num_four_blocks > 1:
        if num_three_blocks % 2 == 1:
            count_for = 0
            count_opp = 0

            for i in range(4):
                if QCOUNT([oracle[0], oracle[1], oracle[2], three_indices[-1] + i]) == 4:
                    count_for += 1
                else:
                    count_opp += 1
                    zero_index = three_indices[-1] + i

                if count_for == 2 or count_opp == 2:
                    break

            if count_for == 2:
                count_ones += 3
                count_zeros += 1
            else:
                count_ones += 1
                count_zeros += 3

        if checked_threes == 0:
            check, count_ones, count_zeros, three_index, zero_index = check_threes(oracle,
                                                                       count_ones,
                                                                       count_zeros,
                                                                       logical_size,
                                                                       three_indices,
                                                                       zero_index)
            if check != -1:
                return check

            if three_index != -1 or num_three_blocks == 1:

                count_for = 0
                count_opp = 0

                for i in range(4):
                    if QCOUNT(oracle[1:] + [three_indices[-1] + i]) == 4:
                        count_for += 1
                    else:
                        count_opp += 1

                    if count_for == 2 or count_opp == 2:
                        break

                if count_for == 2:
                    count_ones += 3
                    count_zeros += 1
                else:
                    count_ones += 1
                    count_zeros += 3

        if count_zeros == count_ones:
            return 0
        elif count_zeros > count_ones:
            return zero_index
        else:
            return oracle[0]


    if num_four_blocks == 0 and num_three_blocks == 1:
        new_check = two_block
        for i in range(4):
            new_check.append(three_indices[0] + i)

        for check in combinations(new_check, 4):
            if QCOUNT(check) == 4:
                return check[0]

    if num_four_blocks == 0 and num_three_blocks > 1:
        new_check = []
        for i in range(4):
            new_check.append(three_indices[0] + i)
        for i in range(4):
            new_check.append(three_indices[1] + i)

        for check in combinations(new_check, 4):
            if QCOUNT(check) == 4:
                oracle = check
                break

        new_block = []
        for i in range(8):
            if new_check[i] not in oracle:
                new_block.append(new_check[i])

        check = QCOUNT(new_block)

        if check == 4:
            logical_size -= 8

            if num_three_blocks == 2:
                return 0
        elif check == 0:
            count_ones += 6
            count_zeros += 2
            if num_three_blocks == 2:
                return oracle[0]

        check, count_ones, count_zeros, three_index, zero_index = check_threes(oracle,
                                                                               count_ones,
                                                                               count_zeros,
                                                                               logical_size,
                                                                               three_indices[2:],
                                                                               zero_index)

        if check != -1:
            return check

        if three_index != -1:
            count_for = 0
            count_opp = 0

            for i in range(4):
                if QCOUNT([oracle[0], oracle[1], oracle[2], three_indices[-1] + i]) == 4:
                    count_for += 1
                else:
                    count_opp += 1
                    zero_index = three_indices[-1] + i

                if (count_for >= 2 or count_opp >= 2) and zero_index != -1:
                    break

            if count_for >= 2:
                count_ones += 3
                count_zeros += 1
            else:
                count_ones += 1
                count_zeros += 3

        if count_zeros == count_ones:
            return 0
        elif count_zeros > count_ones:
            return zero_index
        else:
            return oracle[0]


if __name__ == "__main__":
    import sys

    random.seed(0)
    num_tests = 10000
    for size in [2000]:
        for i in range(num_tests):
            fill_master(size)

            sol = get_solution(size)

            if i % 500 == 0:
                print("After", i+1, "trials")
                print(total_count[0]/(i+1))
                print()

            if check_solution(sol, size) == False:
                raise ValueError("Error at loop " + str(i) + ", solution given: " + str(sol))

            sys.stdout.flush()

        print(total_count[0]/num_tests)


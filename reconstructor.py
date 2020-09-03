import re


def last_char1(val):
    switch = {
        0: 'J',
        1: 'Z',
        2: 'I',
        3: 'H',
        4: 'G',
        5: 'F',
        6: 'E',
        7: 'D',
        8: 'C',
        9: 'B',
        10: 'A'
    }
    return switch.get(val)


def last_char2(val):
    switch = {
        0: 'X',
        1: 'W',
        2: 'U',
        3: 'T',
        4: 'R',
        5: 'Q',
        6: 'P',
        7: 'N',
        8: 'M',
        9: 'L',
        10: 'K'
    }
    return switch.get(val)


def validate_nric(nric):
    x = (int(nric[1]) * 2) + (int(nric[2]) * 7) + (int(nric[3]) * 6) + (int(nric[4]) * 5) + (int(nric[5]) * 4) + (int(nric[6]) * 3) + (int(nric[7]) * 2)

    if nric[0] == 'T' or nric[0] == 'G':
        x = x + 4

    y = x % 11

    if nric[0] == 'S' or nric[0] == 'T':
        z = last_char1(y)

        if nric[8] == z:
            return True
        else:
            return False
    elif nric[0] == 'F' or nric[0] == 'G':
        z = last_char2(y)

        if nric[8] == z:
            return True
        else:
            return False


def permgen(items, n):
    # generates the 1st n numbers of nric
    if n == 0:
        yield []
    else:
        for i in range(len(items)):
            for cc in permgen(items, n-1):
                yield [items[i]]+cc


def construct_ic(partial_nric, n):
    nric_set = set()
    for c in permgen(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 7-n+1):
        for i in range(4):
            nric = []
            if i == 0:
                nric.append('S')
                nric.append(''.join(c))
                nric.append(partial_nric)

                # try nric
                success = validate_nric(''.join(nric))

                if success:
                    nric_set.add(''.join(nric))
            elif i == 1:
                nric.append('T')
                nric.append(''.join(c))
                nric.append(partial_nric)

                success = validate_nric(''.join(nric))

                if success:
                    nric_set.add(''.join(nric))
            elif i == 2:
                nric.append('F')
                nric.append(''.join(c))
                nric.append(partial_nric)

                success = validate_nric(''.join(nric))

                if success:
                    nric_set.add(''.join(nric))
            else:
                nric.append('G')
                nric.append(''.join(c))
                nric.append(partial_nric)

                success = validate_nric(''.join(nric))

                if success:
                    nric_set.add(''.join(nric))
    return nric_set


def filter_nric(year, citizenship, last, nric_set, location_of_birth):
    # Singapore citizens and permanent residents born before 1 January 2000 are assigned the letter "S".
    # Singapore citizens and permanent residents born on or after 1 January 2000 are assigned the letter "T".
    # Foreigners issued with long-term passes before 1 January 2000 are assigned the letter "F".
    # Foreigners issued with long-term passes on or after 1 January 2000 are assigned the letter "G".
    # Singapore citizens and permanent residents born on or after 1 January 1968 are issued NRIC numbers starting with their year of birth, e.g. S71xxxxx# for a person born in 1971 and T02xxxxx# for a person born in 2002. For those born in Singapore, these numbers are identical to the birth registration number on their birth certificates, which are automatically transferred to the NRIC at age 15 and above.
    if (citizenship == 'S' or citizenship == 'P') and int(year) >= 2000:
        first_letter = 'T'
    elif (citizenship == 'S' or citizenship == 'P') and int(year) <= 2000:
        first_letter = 'S'
    elif citizenship == 'F' and int(year) >= 2000:
        first_letter = 'G'
    else:
        first_letter = 'F'
    if location_of_birth == 'Y':
        pattern = f'{first_letter}{year[2:]}[0-5]*{str(last)}'
    else:
        pattern = f'{first_letter}{year[2:]}[5-9]*{str(last)}'
    r = re.compile(pattern)
    nric_filtered = list(filter(r.match, nric_set))
    print(f'Possible NRIC ({len(nric_filtered)})')
    for nric in nric_filtered:
        print(nric)


def main():
    n = int(input('How many characters of the NRIC do you have?: '))
    partial_nric = input(f'Enter last {n} characters of NRIC: ')
    dob = input('Enter Year of Birth [YYYY]: ')
    citizenship = input('Enter Citizenship ([P]R / [S]ingaporean / [F]oreigner): ')
    location_of_birth = input('Is the person born in Singapore? [Y / N]: ')
    nric_set = construct_ic(partial_nric, n)
    filter_nric(dob, citizenship, partial_nric, nric_set, location_of_birth)


if __name__ == '__main__':
    main()

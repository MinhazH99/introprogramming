# For testing
#
# with open('main_test_file.txt', 'r+') as test_file:  # opening test file at beginning for use in all functions
#     data = test_file.readlines()
#     print("Number of lines: ", len(data))
#     i = 0
#     for line in data:
#         print(line)
#         print('Volunteer1' in line)
#         part = line.split('/')
#         for i in range(len(part)):
#             print(part[i])

def getLine():
    with open('main_test_file.txt', 'r+') as test_file:  # opening test file at beginning for use in all functions
        data = test_file.readlines()
        print("Number of lines: ", len(data))
        i = 0
        for line in data:
            if('Volunteer1' in line):
                return line
            else:
                return False

print(getLine())
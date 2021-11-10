import argparse
import itertools


def not_contained(small, big):
    """Checks if the small line is contained in the big list of lines"""
    for z in range(len(big)):
        for i in range(len(big[z]) - len(small) + 1):
            for j in range(len(small)):
                if big[z][i + j] != small[j]:
                    break
            else:
                return False
    return True


def find_all_lines():
    """Finds and returns all lines that can be formed"""
    # All combinations of points in txt
    all_unique_lines = list(itertools.combinations(points_list, 2))
    # Equations coefficients list 
    equations = []
    for line in all_unique_lines:
        point1 = line[0]  # Point 1 of combination
        point2 = line[1]  # Point 2 of combination
        try:  # If equation is in the form y = a*x + b
            a = (point1[1] - point2[1]) / (point1[0] - point2[0])
            b = point2[1] - (a * point2[0])
            if [a, b] not in equations:
                equations.append([a, b])
        except ZeroDivisionError:  # If equation is in the form x = a
            if [point1[0]] not in equations:
                equations.append([point1[0]])
    # All unique lines
    all_unique_lines = []
    for eq in equations:
        temp = []
        for point in points_list:
            try:  # if the point is on the line y = a*x + b
                # ( x == 0 ) won't work due to simplification
                if 0.0001 >= point[1] - eq[0] * point[0] - eq[1] >= -0.0001:
                    temp.append((point[0], point[1]))
            except IndexError:  # if the point is on the line x = a
                if point[0] - eq[0] == 0:
                    temp.append((point[0], point[1]))
        all_unique_lines.append(temp)
    # Return a list of all lines in the form [[(point), (point), +++ ] +++]
    return all_unique_lines


def find_all_parallel():
    """Finds and returns all parallel to the axes lines that can be formed"""
    all_x = []  # x = a
    all_y = []  # y = a
    # For every point
    for i in range(len(points_list)):
        x = points_list[i][0]
        y = points_list[i][1]
        temp_x = []
        temp_y = []
        # For every next point
        for j in range(i + 1, len(points_list)):
            next_x = points_list[j][0]
            next_y = points_list[j][1]
            # if there are 2 points with the same x coordinate
            if x == next_x:
                if (x, y) not in temp_x:
                    temp_x.append((x, y))
                temp_x.append((next_x, next_y))
            # if there are 2 points with the same y coordinate
            if y == next_y:
                if (x, y) not in temp_y:
                    temp_y.append((x, y))
                temp_y.append((next_x, next_y))
        # if not empty an not contained in an other line
        if temp_x != [] and not_contained(temp_x, all_x):
            all_x.append(temp_x)
        if temp_y != [] and not_contained(temp_y, all_y):
            all_y.append(temp_y)
    all_lines = all_x + all_y  # All lines in the form x = a followed by y = a
    # If a point does not have a pair to complete a line 
    # then is paired with the non-existing (x + 1, y)
    for point in points_list:
        alone = True
        for line in all_lines:
            if point in line:
                alone = False
        if alone:
            all_lines.append([point, (point[0] + 1, point[1])])
    return all_lines


def find_best_line():
    best_line = []
    best_score = 0
    for line in all_lines:
        temp_score = 0
        for point in line:
            if point in points_list:
                temp_score = temp_score + 1
        if temp_score > best_score:
            best_score = temp_score
            best_line = line
    return best_line


# Handle arguments
my_parser = argparse.ArgumentParser()
my_parser.add_argument('-f', action='store_const', const=True, help="Find Best Solution")
my_parser.add_argument('-g', action='store_const', const=True, help="Use Parallel Lines")
my_parser.add_argument('points_file')
args = my_parser.parse_args()

# list of all points in txt
points_list = []
with open(args.points_file) as lines:
    points = lines.readlines()
    for point in points:
        x, y = point.strip().split(" ")
        points_list.append((int(x), int(y)))
points_list = sorted(points_list)

# Final result list
result = []

# Identify the flags
if args.f and args.g:
    # Parallel lines and Best solution
    all_lines = find_all_parallel()
    for i in range(1, len(all_lines)):
        # Start from combinations of 1 lines and go on to 2,3,4,++
        subsets = list(itertools.combinations(all_lines, i))
        for subset in subsets:
            # Check if subset contains all points
            temp = []
            for line in subset:
                for point in line:
                    if point not in temp:
                        temp.append(point)
            count = 0
            for point in temp:
                if point in points_list:
                    count = count + 1
            # if subset contains all points
            if count == len(points_list):
                result = subset
                break
        if len(result) != 0:
            break
elif args.f:
    # All lines and Best solution
    all_lines = find_all_lines()
    for i in range(1, len(all_lines)):
        # Start from combinations of 1 lines and go on to 2,3,4,++
        subsets = list(itertools.combinations(all_lines, i))
        for subset in subsets:
            # Check if subset contains all points
            temp = []
            for line in subset:
                for point in line:
                    if point not in temp:
                        temp.append(point)
            # if subset contains all points
            if len(temp) == len(points_list):
                result = subset
                break
        if len(result) != 0:
            break
elif args.g:
    # Parallel lines and Greedy algorithm
    all_lines = find_all_parallel()
    while len(points_list) != 0:
        best_line = find_best_line()
        result.append(best_line)
        # Remove points in line
        temp_points_list = []
        for point in points_list:
            if point not in best_line:
                temp_points_list.append(point)
        points_list = temp_points_list
else:
    # All lines and Greedy algorithm
    all_lines = find_all_lines()
    while len(points_list) != 0:
        best_line = find_best_line()
        result.append(best_line)
        # Remove points in line
        temp_points_list = []
        for point in points_list:
            if point not in best_line:
                temp_points_list.append(point)
        points_list = temp_points_list

# Sort lines
result = sorted(result)  # By elements
result = sorted(result, key=len, reverse=True)  # By descending length

# Print final result
for line in result:
    print(str(line)[1:-1].replace("),", ")"))

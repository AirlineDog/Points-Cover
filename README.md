# Points-Cover
A python script able to find the lowest number of lines needed to connect a specific number of points.

The script has the capability of producing results with two different approaches: 

- By using a greedy algorithm which will give a quick solution but not always the optimal one.
- By testing all subsets which will give the optimal solution, but can't be used for a large number of points due to increasing run time.

There is also the option to work only with parallel lines.

Call the script by passing as arguments the txt file with points given as [example_1.txt](https://github.com/AirlineDog/Points-Cover/blob/main/example_1.txt)
 and the flags ```-f``` for finding the optimal solution and ```-g``` for parallel lines

Examples:
```
#  Greedy algorithm using all lines
py .\re_crossword.py .\example_1.txt

#  Optimal solution using all lines
py .\re_crossword.py -f .\example_1.txt

#  Greedy algorithm using only parallel lines
py .\re_crossword.py -g .\example_1.txt

#  Optimal solution using only parallel lines
py .\re_crossword.py -f -g .\example_1.txt
```

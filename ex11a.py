"""
File Name: ex11a.py
Author: Joshua Hall (10787004)
Last Edited: 6/24/2020
File Purpose: Reads data.csv and collects employee data. Sorts employee data by their id using a mergesort function,
which is a modified version of the source code from https://www.geeksforgeeks.org/merge-sort/. The sorted results are
writen to by_id.txt. The data is then processed and sorted by employee's last and first name. The newly sorted data is
then writen to the file by_name.txt.
Honesty Declaration: I declare that the following source code was written solely by me. I understand that copying any
source code, in whole or in part, constitutes cheating, and that I will receive a zero on this project if I am found in
violation of this policy.
"""
from msort import mergesort
import numpy as np


def read_data(filename):
    """
    Reads a file and organizes lines into a list of tuples.
    :param filename: file to be read
    :return: None
    """
    with open(filename, 'r') as f:
        data = [tuple(line.strip('\n').split(',')) for line in f]
        return data


def sort_by_id(data, comparison_func):
    """
    Sorts data in ascending or descending order based off an employee's id and a comparison function.
    :param data: data to be sorted
    :param comparison_func: used to compare data items together in different ways
    :return: None
    """
    mergesort(data, comparison_func)


def sort_by_name(data, comparison_func):
    """
    Sorts data in ascending or descending order based off an employee's name (last name prioritized before first name)
    and a comparison function.
    :param data: data to be sorted
    :param comparison_func: used to compare data items together in different ways
    :return: None
    """
    to_sort = np.array(data)
    to_sort = [name.split() for name in to_sort[:, 1]]  # takes the full names for employees
    to_sort = [tuple([name[-1], name[0]]) for name in to_sort]  # makes employee tuples: (last name, first name)
    mergesort(to_sort, comparison_func)  # sort the list; last name will be prioritized when sorting
    sorted_data = []
    for name in to_sort:
        for employee in data:
            if employee[1].split()[-1] == name[0] and employee[1].split()[0] == name[1]:
                sorted_data.append(employee)  # if the name from the sorted list matches, add employee to sorted_data
    data[:] = sorted_data


def main():
    """
    Reads a csv file with employee data and sorts them by id then by name. Results for both sorts are writen to output
    text files.
    :return: None
    """
    employee_data = read_data('data.csv')
    sort_by_id(employee_data, lambda x, y: x < y)
    with open('by_id.txt', 'w') as f1:
        for line in employee_data:
            f1.write(f'{line}\n')
    sort_by_name(employee_data, lambda x, y: x < y)
    with open('by_name.txt', 'w') as f2:
        for line in employee_data:
            f2.write(f'{line}\n')


if __name__ == '__main__':
    main()

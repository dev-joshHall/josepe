"""
File Name: msort.py
Last Edited: 6/23/2020
File Purpose: Sorts an array using a comparison function to determine whether it is sorted in ascending or descending
order.
Honesty Declaration: I declare that the following source code was written by https://www.geeksforgeeks.org/merge-sort/.
Any modifications were writen solely by me. I understand that copying any other source code, in whole or in part,
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""


def mergesort(arr, comparison_func):
    if len(arr) > 1:
        # Sort halves ito separate memory
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        mergesort(L, comparison_func)
        mergesort(R, comparison_func)

        # Merge L and R back into arr
        i = j = k = 0
        while i < len(L) and j < len(R):
            if comparison_func(L[i], R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any elements were left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import math
import random

class MathFunctions(APIView):

    def __init__(self):
        self.f1 = ""
        self.f2 = ""
        self.pop_size = 20
        self.max_gen = 921
        self.min_x = -55
        self.max_x = 55
        self.solution = [self.min_x + (self.max_x - self.min_x) * random.random() for i in range(0, self.pop_size)]
        self.gen_no = 0

    def function1(self, x):
        return -eval(self.f1)

    def function2(self, x):
        return -eval(self.f2)

    def index_of(self, a, lista):
        for i in range(0, len(lista)):
            if lista[i] == a:
                return i
        return -1

    def sort_by_values(self, list1, values):
        sorted_list = []
        while len(sorted_list) != len(list1):
            if self.index_of(min(values), values) in list1:
                sorted_list.append(self.index_of(min(values), values))
            values[self.index_of(min(values), values)] = math.inf
        return sorted_list

    def fast_non_dominated_sort(self, values1, values2):
        s = [[] for i in range(0, len(values1))]
        front = [[]]
        n = [0 for i in range(0, len(values1))]
        rank = [0 for i in range(0, len(values1))]

        for p in range(0, len(values1)):
            s[p] = []
            n[p] = 0
            for q in range(0, len(values1)):
                if (values1[p] > values1[q] and values2[p] > values2[q]) or (
                        values1[p] >= values1[q] and values2[p] > values2[q]) or (
                        values1[p] > values1[q] and values2[p] >= values2[q]):
                    if q not in s[p]:
                        s[p].append(q)
                elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
                        values1[q] >= values1[p] and values2[q] > values2[p]) or (
                        values1[q] > values1[p] and values2[q] >= values2[p]):
                    n[p] = n[p] + 1
            if n[p] == 0:
                rank[p] = 0
                if p not in front[0]:
                    front[0].append(p)

        i = 0
        while front[i]:
            Q = []
            for p in front[i]:
                for q in s[p]:
                    n[q] = n[q] - 1
                    if n[q] == 0:
                        rank[q] = i + 1
                        if q not in Q:
                            Q.append(q)
            i = i + 1
            front.append(Q)

        del front[len(front) - 1]
        return front

    def crowding_distance(self, values1, values2, front):
        distance = [0 for i in range(0, len(front))]
        sorted1 = self.sort_by_values(front, values1[:])
        sorted2 = self.sort_by_values(front, values2[:])
        distance[0] = 4444444444444444
        distance[len(front) - 1] = 4444444444444444
        for k in range(1, len(front) - 1):
            distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / (
            max(values1) - min(values1))
        for k in range(1, len(front) - 1):
            distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (
            max(values2) - min(values2))
        return distance

    def crossover(self, a, b):
        r = random.random()
        if r > 0.5:
            return self.mutation((a + b) / 2)
        else:
            return self.mutation((a - b) / 2)

    # Funcion para realizar la mutacion
    def mutation(self, solution):
        mutation_prob = random.random()
        if mutation_prob < 1:
            solution = self.min_x + (self.max_x - self.min_x) * random.random()
        return solution

    def post(self, request):
        self.f1 = request.data[0]
        self.f2 = request.data[1]

        while self.gen_no < self.max_gen:
            function1_values = [self.function1(self.solution[i]) for i in range(0, self.pop_size)]
            function2_values = [self.function2(self.solution[i]) for i in range(0, self.pop_size)]
            non_dominated_sorted_solution = self.fast_non_dominated_sort(function1_values[:], function2_values[:])
            print("The best front for Generation number ", self.gen_no, " is")
            for values in non_dominated_sorted_solution[0]:
                print(round(self.solution[values], 3), end=" ")
            print("\n")
            crowding_distance_values = []
            for i in range(0, len(non_dominated_sorted_solution)):
                crowding_distance_values.append(
                    self.crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
            solution2 = self.solution[:]

            while len(solution2) != 2 * self.pop_size:
                a1 = random.randint(0, self.pop_size - 1)
                b1 = random.randint(0, self.pop_size - 1)
                solution2.append(self.crossover(self.solution[a1], self.solution[b1]))
            function1_values2 = [self.function1(solution2[i]) for i in range(0, 2 * self.pop_size)]
            function2_values2 = [self.function2(solution2[i]) for i in range(0, 2 * self.pop_size)]
            non_dominated_sorted_solution2 = self.fast_non_dominated_sort(function1_values2[:], function2_values2[:])
            crowding_distance_values2 = []
            for i in range(0, len(non_dominated_sorted_solution2)):
                crowding_distance_values2.append(
                    self.crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))
            new_solution = []
            for i in range(0, len(non_dominated_sorted_solution2)):
                non_dominated_sorted_solution2_1 = [
                    self.index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
                    range(0, len(non_dominated_sorted_solution2[i]))]
                front22 = self.sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
                front = [non_dominated_sorted_solution2[i][front22[j]] for j in
                         range(0, len(non_dominated_sorted_solution2[i]))]
                front.reverse()
                for value in front:
                    new_solution.append(value)
                    if len(new_solution) == self.pop_size:
                        break
                if len(new_solution) == self.pop_size:
                    break
            self.solution = [solution2[i] for i in new_solution]
            self.gen_no = self.gen_no + 1

        function1 = [round(i * -1, 2) for i in function1_values]
        function2 = [round(j * -1, 2) for j in function2_values]
        result = [function1, function2]
        return Response(result)

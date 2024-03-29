
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, depth, cost, heuristic, action): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)
    
    def in_parent(self, newstate):
        if self.parent == None:
            return False
        if self.parent.state == newstate:
            return True
        
        return self.parent.in_parent(newstate)


# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0, 0, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 0
        self.non_terminals = 0
        self.highest_cost_nodes = []
        self.average_depth = 0
        self.nodes = 0
        self.totalDepth = 0

    @property 
    def length(self):
        return self.solution.depth
    
    @property 
    def avg_branching(self):
        return (self.terminals + self.non_terminals - 1)/self.non_terminals 
    
    @property 
    def cost(self):
        return self.solution.cost
    
    @property
    def plan(self):
        return self.get_plan(self.solution)
    
    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)
    
    def get_plan(self,node):
        if node.parent == None:
            return []
        plan = self.get_plan(node.parent)
        plan += [node.action]
        return(plan)

    # procurar a solucao
    def search(self, limit = None):
        while self.open_nodes != []:
            self.terminals = len(self.open_nodes)
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.average_depth = self.totalDepth / self.nodes
                return self.get_path(node)
            
            lnewnodes = []
            self.non_terminals +=1
            if limit == None or node.depth < limit:
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    if not node.in_parent(newstate):
                        newnode = SearchNode(newstate,node, node.depth + 1, node.cost + self.problem.domain.cost(node.state, a), self.problem.domain.heuristic(newstate, self.problem.goal), a) #node.depth + 1 vai somar 1 à profundidade do node pai
                        lnewnodes.append(newnode)
                        
                        self.nodes +=1
                        self.totalDepth += newnode.depth 

                        if not self.highest_cost_nodes or newnode.cost > self.highest_cost_nodes[0].cost:
                            self.highest_cost_nodes = [newnode]
                        elif newnode.cost == self.highest_cost_nodes[0].cost:
                            self.highest_cost_nodes.append(newnode)
                        
                self.add_to_open(lnewnodes)

        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            for node in lnewnodes:
                self.open_nodes.append(node)
                self.open_nodes.sort(key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            for node in lnewnodes:
                self.open_nodes.append(node)
                self.open_nodes.sort(key= lambda node: node.heuristic)
        elif self.strategy == 'a*':
            for node in lnewnodes:
                self.open_nodes.append(node)
                self.open_nodes.sort(key= lambda node: node.cost + node.heuristic)



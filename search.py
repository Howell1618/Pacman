# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from copy import copy, deepcopy
from inspect import trace
from operator import indexOf, truediv
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    #variables
    NewState=problem.getStartState() #problem.startState
    ValidActions = None
    IsGoalState = False
    TempAction=(NewState,None,0)
    Actions=[TempAction]
    ReturnActions=[]
    VisitedPoints=[NewState]
    IsRetry = False
    # Times = 0
    import util
    Tree = util.Stack()

    #status
    print("Start:", problem.getStartState())
    
    while not IsGoalState:
        # Times +=1 
        if not IsRetry:
            ValidActions=problem.expand(NewState)  #use expand to instead of getActions
            #rint("Valid actions:", ValidActions)

            #save to Tree, Last in Fisrt out
            if len(ValidActions) > 0:          
                #Others to Tree from right to left
                while len(ValidActions)>1:
                    Tree.push([ValidActions[len(ValidActions)-1],TempAction])
                    ValidActions.pop()
                TempAction =ValidActions[0] #No.0 Action

            else: #If no other actions:
                #find the nearest parent node which current node is its left child node, turn to right child node
                if not Tree.isEmpty():
                    TempAction,LastAction = Tree.pop()
                    Actions=Actions[:Actions.index(LastAction)+1] 
                    IsRetry=True
                    continue
                #if current node is last right child node
                else:
                    print("can't find route!")
                    return []

        NewState=TempAction[0]
        if VisitedPoints.__contains__(NewState):
            #to duplicate point
            if not Tree.isEmpty():
                TempAction,LastAction = Tree.pop()
                NewState=TempAction[0]
                Actions=Actions[: Actions.index(LastAction)+1] 
                IsRetry=True
                continue                   
            #if current node is last right child node
            else:
                print("can't find route!")
                return []
        else:
            VisitedPoints.append(NewState)
            IsGoalState = problem.isGoalState(NewState)

            #print("Get Next State:", NewState, " IsGoal:", IsGoalState)
            Actions.append(TempAction)
            IsRetry=False
            # #test red area issue
            # if Times > 15:
            #     break

    #print("Get action cost:", problem.getActionCost(problem.startState,s,NextState))
   
    for action in Actions[1:]:
        ReturnActions.append(action[1]) 
    return ReturnActions 


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    #variables
    CurrentState=problem.getStartState() #problem.startState
    CurrentAction = None # the action to this state
    ValidActions = None
    IsGoalState = False
    TempActions=[((CurrentState,None,0),0)]
    ActionsList=[(TempActions,[])]
    ExpandActionsList = [(TempActions,[])]

    NextActionsList=[]
    import util  
    FullGoalsActionsList = util.PriorityQueue()
    GoalActionsList = []
  
    
    ReturnActions=[]
    VisitedPoints=[] 
 
    IsFirstTime = True
    HasFoundGoal=False
    GoalCount = 1
    NeedFindAllRoute=False

    #status
    #print("Start:", problem.getStartState())
     

    while (not IsGoalState) and len(ActionsList)>0: 
        for actions,visitedgoals in ActionsList:
            CurrentState,CurrentAction,Cost = actions[len(actions)-1][0]
            if not VisitedPoints.__contains__(CurrentState):
                VisitedPoints.append(CurrentState)  
                IsGoalState = problem.isGoalState(CurrentState)   
                if IsGoalState: 
                    HasFoundGoal = True
                    GoalActionsList.append((actions,visitedgoals))
                    break
                
                ValidActions=problem.expand(CurrentState)
                # print("Valid actions:", ValidActions)

                #Find potential states and del duplicate states(include del backaction)
                for action in ValidActions: 
                    TempActions = copy(actions)
                    PathCost = TempActions[len(TempActions)-1][1] + action[2]
                    TempActions.append((action,PathCost))                
                    NextActionsList.append((TempActions,visitedgoals))

        if not HasFoundGoal: 
            #prepare for next layer
            ActionsList = copy(NextActionsList) 
            NextActionsList.clear()

    FullGoalsActionsList.heap.clear()
    for actions,visitedgoals in GoalActionsList:
        FullGoalsActionsList.push(actions,actions[len(actions)-1][1])


    if len(FullGoalsActionsList.heap)==0:
        print("can't find route!")
        return []


    TempActions = FullGoalsActionsList.pop()
    for action in TempActions[1:]:
        ReturnActions.append(action[0][1]) 
    return ReturnActions 
 

def uniformCostSearch(problem):
    "*** YOUR CODE HERE ***"
    #variables
    CurrentState=problem.getStartState()  
    CurrentAction = None # the action to this state
    ValidActions = None
    IsGoalState = False
    TempActions=[((CurrentState,None,0),0)]
    import util
    ActionsList = util.PriorityQueue()#util.Stack()
    ActionsList.push(TempActions,0)
  
    ReturnActions=[]
    VisitedPoints=[]
    GoalActionsList = util.PriorityQueue()
  
    #status
    #print("Start:", problem.getStartState())

    try:
 
        #ActionsList.push(((1,2),None,3)) # test: the newest one at the last place
   
        while (not IsGoalState) and len(ActionsList.heap)>0:  #not need process every list in stack, just process the upper one, not need cycle
            TempActions = ActionsList.pop()
            CurrentState,CurrentAction,Cost = TempActions[len(TempActions)-1][0]
            if not VisitedPoints.__contains__(CurrentState):
                VisitedPoints.append(CurrentState)  
                IsGoalState = problem.isGoalState(CurrentState)   
                if IsGoalState: 
                    PathCost=TempActions[len(TempActions)-1][1]
                    GoalActionsList.push(TempActions,PathCost)
                    break
                #else
                ValidActions=problem.expand(CurrentState)
    
    #  PriorityQueue has function to sort
                # #save to Tree, Last in Fisrt out, sort by path cost
                # for i in range(0,len(ValidActions)-1,1):
                #     tmpplace=i
                #     for j in range(i+1,len(ValidActions),1):
                #         if ValidActions[tmpplace][2]>ValidActions[j][2]:
                #             tmpplace=j
                #     if tmpplace!=i:
                #         tmpaction=ValidActions[i]
                #         ValidActions[i]=ValidActions[tmpplace]
                #         ValidActions[tmpplace]=tmpaction
    
                while len(ValidActions) > 0:          
                    #points to Tree from cost more to less
                    #if not VisitedPoints.__contains__(ValidActions[len(ValidActions)-1][0]):                    
                        #need add this route after sort in ActionsList   , PriorityQueue?
                    PathCost = TempActions[len(TempActions)-1][1] + ValidActions[len(ValidActions)-1][2]
                    ActionsList.push(TempActions+[(ValidActions[len(ValidActions)-1],PathCost)],PathCost)
                    #after if check
                    ValidActions.pop()
 
   
        if not IsGoalState:
            print("can't find route!")
            return []

        TempActions = GoalActionsList.pop()
        for action in TempActions[1:]:
            ReturnActions.append(action[0][1]) 
        return ReturnActions 
 
    except Exception as err:
        print(err)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    import util

    #variables
    CurrentState=problem.getStartState()  
    ValidActions = None
    IsGoalState = False
    TempActions=[((CurrentState,None,0),0)] #(state,action,cost),totalcost

    ActionsList = util.PriorityQueue()
    ActionsList.push((TempActions,[]),0) #(actions,visitedgoals), totalcost for sort
    
    ReturnActions=[]
    VisitedPoints=[]
    GoalActionsList = util.PriorityQueue() 
 
    #status
    print("Start:", problem.getStartState())

    try:
  
        while len(ActionsList.heap)>0:  #not need process every list in stack, just process the upper one, not need cycle
            TempActions,visitedgoals = ActionsList.pop()
            CurrentState,CurrentAction,Cost = TempActions[len(TempActions)-1][0]
            if not VisitedPoints.__contains__(CurrentState):
                VisitedPoints.append(CurrentState)  
                IsGoalState = problem.isGoalState(CurrentState)   
                if IsGoalState: 
                    PathCost=TempActions[len(TempActions)-1][1]
                    GoalActionsList.push((TempActions,visitedgoals),PathCost)
                    break
                #else
                ValidActions=problem.expand(CurrentState)
    
                #     # from rear to front tinySearch h=0 is 5298,  front to rear 5057; with heuristic are the same
                # while len(ValidActions) > 0:          
                #     PathCost = TempActions[len(TempActions)-1][1] + ValidActions[len(ValidActions)-1][2]
                #     h=heuristic(ValidActions[len(ValidActions)-1][0],problem)
                #     f=PathCost+h
                #     ActionsList.push((TempActions+[(ValidActions[len(ValidActions)-1],PathCost)],visitedgoals),f)
                #     ValidActions.pop()

                #front to rear 5057
                for action in ValidActions:         
                    PathCost = TempActions[len(TempActions)-1][1] + action[2]
                    h=heuristic(action[0],problem)
                    f=PathCost+h
                    ActionsList.push((TempActions+[(action,PathCost)],visitedgoals),f)
                
                    
        if not IsGoalState: 
            print("can't find route!")
            return []

        TempActions = GoalActionsList.pop()
        for action in TempActions[0][1:]:
            ReturnActions.append(action[0][1]) 
        return ReturnActions 
       
 
    except Exception as err:
        print(err)
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

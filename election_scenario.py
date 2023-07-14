#Author - Harshawardhan Mane

import networkx as nx
import matplotlib.pyplot as plt
import random as r
import math as m

#Basic function that will take input from the user to play the game
def play():
    option=input("Play as blue or red?: ")
    if option=="blue":
        print("You are playing as blue")
        print()
        simulate("blue")
    elif option=="red":
        print("You are playing as red")
        print()
        simulate("red")

#Main simulation structure
def simulate(selection):
    #taking standard input from the user, a number of parameters, for the simulation to run
    print("Please input the following parameters - ")
    parameters={1:"1. Number of agents in the green team(n) and probability of connections(p)",
                2:"2. Number of agents in the grey team(n) and proportion of agents who are spies from the red team(p)",
                3:"3. Uncertainty interval",
                4:"4. Percentage of agents (green) who want to vote in the election"}
    for value in parameters.values():
        print(value)
    print()
    parameter_input=dict()
    for i in range(1,5):
        input_buffer=input("Please input the parameter "+str(i)+", (separated by a comma(s)): ").split(",")
        print()
        if len(input_buffer)==2:
            parameter_input[i]=(input_buffer[0], input_buffer[1])
        else:
            parameter_input[i]=input_buffer[0]
    
    #variables for graph creation-start
    
    #basic green demographics
    no_of_greens=int(parameter_input[1][0]) #total population of green nodes
    connection_probability=float(parameter_input[1][1]) #probability of forming connections between green nodes
    #basic grey demographics
    no_of_greys=int(parameter_input[2][0]) #total no of grey agents
    proportion_of_spies=float(parameter_input[2][1]) #proportion of grey agents who are spies for the red team
    
    #determining factors
    energy_level=[100] #energy level of the blue agents, which will be spent on each turn accordingly
    voting_percent=[float(parameter_input[4])] #percentage of green population that have decided to vote
    red_followers=[100-voting_percent[0]]
    uncertainty_interval=parameter_input[3]
    interval_size=int(uncertainty_interval[1])-int(uncertainty_interval[0])
    interval_bounds=[int(uncertainty_interval[0]), int(uncertainty_interval[1])]
    
    #storing the data of the green population
    greens=dict()
    greens_voting=m.floor(no_of_greens*(voting_percent[0]/100))
    greens_not_voting=no_of_greens-greens_voting
    for i in range(0, greens_voting):
        uncertainty=round(r.uniform(float(uncertainty_interval[0]), float(uncertainty_interval[1])/2), 3)
        greens[i]=["person"+str(i), uncertainty, "Voting"]
    for i in range(greens_voting, no_of_greens):
        uncertainty=round(r.uniform(float(uncertainty_interval[1])/2, float(uncertainty_interval[1])), 3)
        greens[i]=["person"+str(i), uncertainty, "Not voting"]
    
    #storing the data of the grey agents (alloting grey_good-s and grey_bad-s their slots)
    greys=[]
    grey_bad=m.floor(no_of_greys*proportion_of_spies)
    grey_good=no_of_greys-grey_bad
    for i in range(0, grey_bad):
        greys.append("grey_bad")
    for j in range(0, grey_good):
        greys.append("grey_good")
    
    #variables for graph creation-end
        
    #determine connections between green nodes-start
    G=nx.fast_gnp_random_graph(no_of_greens, connection_probability, seed=None, directed=False)
    connections=list(nx.to_edgelist(G, nodelist=None))
    #determine connections between green nodes-end
    
    #game model, if the user chooses to play as blue agent
    if selection=="blue":
        while energy_level[0]>0:
            #emulate human-input driven blue agent's turn
            blue("human", greens, greys, energy_level, voting_percent, no_of_greys, interval_size, interval_bounds)
            if red_followers[0]==0:
                print("Red team lost")
                break
            #emulate automated red agent's turn
            red("automation", greens, red_followers, voting_percent, interval_size, interval_bounds, energy_level)
            #emulate automated green agent's turn
            green(greens, connections, interval_size, voting_percent, interval_bounds)
            
                
        if voting_percent[0]>=50:
            print("You have won the game")
        else:
            print("You have lost the game")
        
        
    #game model, if the user chooses to play as red agent
    if selection=="red":
        while red_followers[0]>0:
            #emulate human-input driven red agent's turn
            red("human", greens, red_followers, voting_percent, interval_size, interval_bounds, energy_level)
            if energy_level[0]==0:
                print("Blue team lost")
                break
            #emulate automated blue agent's turn
            blue("automation", greens, greys, energy_level, voting_percent, no_of_greys, interval_size, interval_bounds)
            #emulate green agent's turn
            green(greens, connections, interval_size, voting_percent, interval_bounds)
        
        if voting_percent[0]<50:
            print("You have won the game")
        else:
            print("You have lost the game")
            
    #create graph for red and blue agents-start
    A=nx.Graph()
    A.add_nodes_from([0, 1])
    attrs_agents={0:{"color" : "red"}, 1:{"color": "blue"}}
    nx.set_node_attributes(A, attrs_agents)
    nx.relabel_nodes(A, {0:"Red Team", 1:"Blue Team"}, copy=False)
    #create graph for red and blue agents-end
    
    #set attributes to the green-nodes graph-start
    attrs_greens={}
    for i in range(0, len(greens)):
        attrs_greens[i]={"name": greens[i][0], "color": "green", "Vote": greens[i][2]}
    nx.set_node_attributes(G, attrs_greens)
    node_labels=nx.get_node_attributes(G, 'Vote')
    node_labels["Red Team"]="Red Team"
    node_labels["Blue Team"]="Blue Team"
    #set attributes to the green-nodes graph-end
    
            
    #merge red/blue and green agent graphs-start
    M=nx.union(G, A, rename=(None, None))
    #merge red/blue and green agent graphs-end
    
    #determine display attributes-start
    
    #determine display attributes-end
    
    #call display function to display the graph
    display(M, node_labels)

#Agents
            
#Blue Agent
def blue(mode, greens, greys, energy_level, voting_percent, no_of_greys, interval_size, interval_bounds):
    options={0:["The format is -> Campaign message | Potency | Energy loss"],
             1:["Voting will create new government and new oppportunities", -round((interval_size/50), 3), -1.5],
             2:["Free and fair elections mean better quality of life", -round((interval_size/50), 3), -1.5],
             3:["Majority mandated government means more degrees of freedom for everyone", -round((interval_size/50), 3), -1.5],
             4:["Arbitrary propaganda A", -round(2*(interval_size/50), 3), -3.0],
             5:["Arbitrary propaganda B", -round(2*(interval_size/50), 3), -3.0],
             6:["Arbitrary Propaganda C", -round(3*(interval_size/50), 3), -3.5],
             7:["Arbitrary Propaganda D", -round(3*(interval_size/50), 3), -3.5],
             8:["Provide monetary bribe to vote", -round(4*(interval_size/50), 3), -4.0],
             9:["Provide material bribe to vote", -round(4*(interval_size/50), 3), -4.0],
             10:["Provide vehicles to escort people to go to voting booths", -round(5*(interval_size/50), 3), -4.5],
             11:["grey", "variable uncertainty value", "Energy loss=0"]}
    
    if mode=="human":
        for item in options.items():
            print(item)
        
        print()
        print("Your current energy level is: " + str(energy_level[0]))
        print("Current voting percent is: " +str(voting_percent[0]))##############
        user_input=int(input("Please select an option from 1-11 to proceed: "))
        print()
        if user_input==11:
            if no_of_greys>0:
                grey(greens, greys, voting_percent, interval_size, interval_bounds)
            else:
                print("You are out of grey agents")
        else:
            interaction(options[user_input][1], greens, voting_percent, interval_size, "blue", interval_bounds)
            energy_level[0]+=options[user_input][2]
            
    elif mode=="automation":
        if voting_percent[0]<30:
            choice=10
            interaction(options[choice][1], greens, voting_percent, interval_size, "blue", interval_bounds)
            energy_level[0]+=options[choice][2]
        if voting_percent[0] in range(30, 40):
            choice=r.randint(8, 9)
            interaction(options[choice][1], greens, voting_percent, interval_size, "blue", interval_bounds)
            energy_level[0]+=options[choice][2]
        if voting_percent[0] in range(40, 50):
            choice=r.randint(6, 7)
            interaction(options[choice][1], greens, voting_percent, interval_size, "blue", interval_bounds)
            energy_level[0]+=options[choice][2]
        if voting_percent[0] in range(50, 60):
            if no_of_greys >0:
                grey(greens, greys, voting_percent, interval_size, interval_bounds)
            else:
                choice=r.randint(4,5)
                interaction(options[choice][1], greens, voting_percent, interval_size, "blue", interval_bounds)
                energy_level[0]+=options[choice][2]
        if voting_percent[0] in range(60, 70):
            if no_of_greys>0:
                grey(greens, greys, voting_percent, interval_size, interval_bounds)
            else:
                choice=r.randint(1,3)
                interaction(options[choice][1], greens, voting_percent, interval_size, "blue", interval_bounds)
                energy_level[0]+=options[choice][2]
        if voting_percent[0] in range(70, 80):
            choice=r.randint(1,3)
            interaction(options[choice][1], greens, voting_percent, interval_size, "blue")
            energy_level[0]+=options[choice][2]
            
    
#Red Agent    
def red(mode, greens, red_followers, voting_percent, interval_size, interval_bounds, energy_level):
    options={0:["The format is -> Campaign message | Potency | Possible follower loss"],
             1:["Do not waste your time voting", round((interval_size/50), 3), -0.5],
             2:["There are goons deployed at the voting booth", round((interval_size/50), 3), -0.5],
             3:["The party has rigged the elections", round((interval_size/50), 3), -0.5],
             4:["Arbitrary propaganda A", round(2*(interval_size/50), 3), -0.6],
             5:["Arbitrary propaganda B", round(2*(interval_size/50), 3), -0.6],
             6:["Arbitrary propaganda C", round(3*(interval_size/50), 3), -0.7],
             7:["Arbitrary propaganda D", round(3*(interval_size/50), 3), -0.7],
             8:["Provide monetary bribe to not vote", round(4*(interval_size/50), 3), -0.8],
             9:["Provide material bribe to not vote", round(4*(interval_size/50), 3), -0.8],
             10:["Actually Spread a flu-type disease to prevent people from going out to vote", round(5*(interval_size/50), 3), -1.0]}
    if mode=="human":
        for item in options.items():
            print(item)
        print()
        print("Current red followers are: " + str(red_followers[0]))
        print("Current voting percent is: " +str(voting_percent[0]))##############
        user_input=int(input("Please select an option from 1-10 to proceed: "))
        interaction(options[user_input][1], greens, voting_percent, interval_size, "red", interval_bounds)
        red_followers[0]+=options[user_input][2]
        
    elif mode=="automation":
        if voting_percent[0]>70:
            choice=10
            interaction(options[choice][1], greens, voting_percent, interval_size, "red", interval_bounds)
            red_followers[0]+=options[choice][2]
            energy_level[0]+=round(10*(options[choice][2]/4), 2)
        elif voting_percent[0]>55 and voting_percent[0]<=70:
            choice=r.randint(8,9)
            interaction(options[choice][1], greens, voting_percent, interval_size, "red", interval_bounds)
            red_followers[0]+=options[choice][2]
            energy_level[0]+=round(10*(options[choice][2]/4), 2)
        elif voting_percent[0]>45 and voting_percent[0]<=55:
            choice=r.randint(6,7)
            interaction(options[choice][1], greens, voting_percent, interval_size, "red", interval_bounds)
            red_followers[0]+=options[choice][2]
            energy_level[0]+=round(10*(options[choice][2]/4), 2)
        elif voting_percent[0]>25 and voting_percent[0]<=45:
            choice=r.randint(4,5)
            interaction(options[choice][1], greens, voting_percent, interval_size, "red", interval_bounds)
            red_followers[0]+=options[choice][2]
            energy_level[0]+=round(10*(options[choice][2]/4), 2)
        elif voting_percent[0]>0 and voting_percent[0]<=25:
            choice=r.randint(1,3)
            interaction(options[choice][1], greens, voting_percent, interval_size, "red", interval_bounds)
            red_followers[0]+=options[choice][2]
            energy_level[0]+=round(10*(options[choice][2]/4), 2)
                
    
#Grey agent, can be a spy or work favourably for the blue agent
def grey(greens, greys, voting_percent, interval_size, interval_bounds):
    total_greys=len(greys)
    blue_uncertainty_factor=[round(interval_size/50, 3), round(2*(interval_size/50), 3), round(3*(interval_size/50), 3), round(4*(interval_size/50), 3), round(5*(interval_size/50), 3)]
    red_uncertainty_factor=[round(interval_size/50, 3), round(2*(interval_size/50), 3), round(3*(interval_size/50), 3), round(4*(interval_size/50), 3), round(5*(interval_size/50), 3)]
    ran_num=r.randint(0,4)
    
    #grey agent emulation
    if total_greys > 0:
        luck=r.randint(0, total_greys-1)
        instance=greys[luck]
        if instance=="grey_good":
            interaction(-blue_uncertainty_factor[ran_num], greens, voting_percent, interval_size, "blue", interval_bounds)
            greys.pop(luck)
            
        elif instance=="grey_bad":
            interaction(red_uncertainty_factor[ran_num], greens, voting_percent, interval_size, "red", interval_bounds)
            greys.pop(luck)

    else:
        print("You are out of grey-agents")
    
    

#interaction function, that determines what change will happen in the uncertainty of green agent 
def interaction(potency, greens, voting_percent, interval_size, caller, interval_bounds):
    half=interval_size/2
    for i in range(0, len(greens)):
        uncertainty_previous=greens[i][1]
        greens[i][1]=round(potency+uncertainty_previous, 3)
        
        if greens[i][1]<interval_bounds[0]:
            greens[i][1]=interval_bounds[0]
        if greens[i][1]>interval_bounds[1]:
            greens[i][1]=interval_bounds[1]
        
    
    for i in range(0, len(greens)):
        if greens[i][1]>half:
            greens[i][2]="Not voting"
        if greens[i][1]<=interval_size/2:
            greens[i][2]="Voting"
    
    voter_count=0
    for i in range(0, len(greens)):
        if greens[i][2]=="Voting":
            voter_count=voter_count+1

    voting_percent[0]=round((voter_count/len(greens))*100, 3)


#an interaction function, specifically designed for when greens will interact with each other
def green(greens, connections, interval_size, voting_percent, interval_bounds):
    for i in range(0, len(connections)):
        node1=connections[i][0]
        node2=connections[i][1]
        node1_uncertainty=greens[node1][1]
        node2_uncertainty=greens[node2][1]
        if interval_size/2-abs(node1_uncertainty)>interval_size/2-abs(node2_uncertainty):
            if greens[node2][2]=="Not Voting":
                greens[node1][1]+=round(abs(node2_uncertainty/interval_size),3)
                greens[node1][2]=greens[node2][2]
            elif greens[node2][2]=="Not Voting":
                greens[node1][1]-=round(abs(node2_uncertainty/interval_size), 3)
                greens[node1][2]=greens[node2][2]
            
        elif interval_size/2-abs(node1_uncertainty)<interval_size/2-abs(node2_uncertainty):
            if greens[node1][2]=="Not Voting":
                greens[node2][1]+=round(abs(node2_uncertainty/interval_size), 3)
                greens[node2][2]=greens[node2][2]
            elif greens[node1][2]=="Not Voting":
                greens[node2][1]-=round(abs(node2_uncertainty/interval_size), 3)
                greens[node2][2]=greens[node2][2]
    voter_count=0   
    for i in range(0, len(greens)):
        if greens[i][2]=="Voting":
            voter_count+=1
    
    voting_percent[0]=round((voter_count/len(greens))*100, 3)
    

#display function to show the output of graph on screen
def display(graph, node_labels):
    color_map = []
    for node in graph:
        if node=="Red Team":
            color_map.append("red")
        elif node=="Blue Team":
            color_map.append("blue")
        else:
            color_map.append("green")
    nx.draw(graph, node_color=color_map, labels=node_labels, with_labels=True)
    plt.show()

play()
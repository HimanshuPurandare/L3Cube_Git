'''
*	This program proves the Birthday Paradox.
*
*	First option gives the probability of getting two birthdays on same day firstly by random experiment and then by using formula.
*
*	Second option gives the minimum number of people required so that probability of two people having same birthday is always greater
*	than the value provided by the user. It is NOT the reverse of first option and is meant for cross checking the output given by 
*	option 1.
*	
*	Third option plots the graph of Probabilty vs number of people in a group by random experiment and by formula.
'''


import math
import random
from decimal import *
import matplotlib.pyplot as plt


getcontext().prec=100

def get_rand_exp_count(n,days_in_year,freq=10000):

	same=not_same=0
	for i in xrange(freq):
		l=[]
		for j in range(days_in_year):
			l.append(0)
		for j in xrange(n):
			b=random.randint(0,days_in_year-1)
			l[b]+=1
		for j in l:
			if j>1:
			    same+=1
			    break
		else:
			not_same+=1

	return [same,not_same]

def get_no_of_people(prob,days_in_year):
	if prob == 1.0:
		return days_in_year+1
	else:
		return math.ceil(Decimal(math.sqrt(Decimal(2*days_in_year)*Decimal(math.log(Decimal(1)/Decimal(1-prob)))))); 
	
def get_probability(no_of_people,days_in_year):
	ans=1
	for i in range(days_in_year,days_in_year-no_of_people,-1):
		ans*=i
	ans=Decimal(ans)/Decimal(days_in_year**no_of_people)
	return Decimal(1.00000000000000000000000000000000000000000000000000)-Decimal(ans)

option = -1
while option%4:
	print "\n\t\t***Birthday Paradox***"
	print "\n1.Calculate Probability for no of people\n2.Calculate No of People for given Probability\n3.Plot the graph\n4.Exit"
	print "\nChoose the option:"
	option=int(raw_input())	
	while (option>4 or option<1):
		print "Please choose the correct option"
		option=int(raw_input())
	
	if option==4:
		break

	days_in_year=-1
	print "Enter No. of days in year(365/366)?:"		
	while days_in_year!=365 and days_in_year!=366:
		days_in_year=int(raw_input())

	if option==1:
	
		print "Enter the number of people(randomly selected) in Group:"
		n=int(raw_input())
		print "Wait a minute, processing ...\n\t*** Precision till 100 decimals ***"

		l= get_rand_exp_count(n,days_in_year)	
		same=l[0]
		not_same=l[1]
	
		rand_exp_ans=float(same)/10000.00
		math_ans=get_probability(n,days_in_year)	    
	
		print "\n\n\n***Probability of at least two people having same birthday = P.A.T.P.H.S.B.***"
	
		print "\n\tThe experiment was performed 10000 times by taking group of",n,"people on random basis,"
		print "\tIt was found that",same,"times at least 2 people were having birthday on same day"
		print "\tAnd",not_same,"times no two people in the group were having birthday on same day."
		print "\tThus By performing random experiment:PATPHSB=",rand_exp_ans,"(",rand_exp_ans*100,"% )"
		print "\tBy using theory of probability,PATPHSB is:\n\n\t",math_ans,"(",float(math_ans*100),"% )"
	
	if option==2:
		print "\n\nEnter the probability of 'at least two people with same birthday' you want:(Enter value between 0 to 1 )"
		prob=Decimal(raw_input())
		print "\nWhen there are at least",get_no_of_people(prob,days_in_year)%(days_in_year+2),"people in group then probability of two people having same birthday is greater equal",prob*100,"%"	

	if option == 3:
		print "\n\t*** Plotting the graph... Please Wait ***\n"
		x_people_count = range(1,121)
		y_prob = []
		y_rand_exp=[]
		for cnt in range(1,121):
			y_rand_exp.append(Decimal(get_rand_exp_count(cnt,days_in_year,500)[0])/Decimal(500))
			y_prob.append(get_probability(cnt,days_in_year))
		plt.plot(x_people_count,y_rand_exp,label="Random Experiment")
		plt.plot(x_people_count,y_prob,linestyle='-',color='r',label="By Maths")
		
		plt.xlabel('Number of People in Group')
		plt.ylabel('Random Experiment Answer and Probability by Maths')
		plt.title('Random Experiment and Probability vs No of People')
		plt.legend()
		plt.ylim(0,1.05)
		


		plt.show()	
		
	

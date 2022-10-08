#########
# v 1.0 #
#########

import random

#Mine yearly output
goldInflationBase = 3583
goldInflationOPEC = 358
goldInflationOPECPlus = 36
goldInflationBRICS = 179
goldInflationUS = 1433
goldInflationEU = 537
goldInflationRestWorld5 = 179


#20 years chance to be adopted by
goldChanceOPEC = .20
goldChanceOPECPlus = .50 #only if goldOpec = true!
goldChanceBrics = .20
goldChanceUS = .15
goldChanceEU = .05
goldChanceRestWorld5 = .10

#Increase of adopting chance after trigger
goldTriggerOPEC = .25
goldTriggerOPECPlus = .05 #only if goldOpec = true!
goldTriggerBrics = .20
goldTriggerUS = .50
goldTriggerEU = .35
goldTriggerRestWorld5 = .15

#GeneralData
USEconomySize = .239
EUEconomySize = .148
goldAboveGround = 205238
toneToToz = 32150.7

#PopulationGrowth
#Firsr element 2023
popGrowth = [.0088, .0087, .0086, .0085, .0097, .0084, .0083, .0083, .0070, .0081, .0081, .0069, .0079, .0068, .0078, .0067, .0066, .0066, .0065, .0054, .0065]				

#DiscountRate
baseDisc = 0.053 - .02

#M in XAU
XAUInUS = 1709.58
XAUInEUR = 1746.42
mEU = ((7389683 + (.50 * 3486458)) * 1000000) / XAUInEUR
mUS = ((19377758 + (.50 * 2236142) + (.15 * 12000000)) * 1000000) / XAUInUS
m5 = ((0.05 * (0.5 * 38120)) * 1000000)

class calcResult:
  def __init__(self, amount, year):
    self.amount = amount
    self.year = year


def simulateNext():
	
	goldOpec_tmp = False
	goldOpecPlus_tmp = False
	goldBRICS_tmp = False
	goldUS_tmp = False
	goldEU_tmp = False
	goldRestWorld5_tmp = 0
	
	goldOpec_local = False
	goldOpecPlus_local = False
	goldBRICS_local = False
	goldUS_local = False
	goldEU_local = False
	goldRestWorld5_local = 0
	
	goldRestWorld5 = 0
	discRate = []	
	goldActualOutput = goldInflationBase
	goldTriggerAccumulated = 0
	totalGlobalAdoption = 0
	goldAboveGround_local = goldAboveGround
	
	while(totalGlobalAdoption < EUEconomySize or totalGlobalAdoption < (1 - EUEconomySize - USEconomySize) / 5):
		year = len(discRate)
		
		if(goldOpec_local == False):
			if(random.uniform(0, 1) < 1-(1-goldChanceOPEC*(1 + goldTriggerAccumulated))**(1/20)):
				goldOpec_tmp = True
				
		if(goldOpecPlus_local == False and (goldOpec_tmp or goldOpec_local)):
			tmpOPPlus = 1 if (1-goldChanceOPECPlus*(1 + goldTriggerAccumulated)) <= 0 else 1-(1-goldChanceOPECPlus*(1 + goldTriggerAccumulated))**(1/20)
			if(random.uniform(0, 1) < tmpOPPlus):
				goldOpecPlus_tmp = True
				
		if(goldBRICS_local == False):
			if(random.uniform(0, 1) < 1-(1-goldChanceBrics*(1 + goldTriggerAccumulated))**(1/20)):
				goldBRICS_tmp = True
				
		if(goldUS_local == False):
			if(random.uniform(0, 1) < 1-(1-goldChanceUS*(1 + goldTriggerAccumulated))**(1/20)):
				goldUS_tmp = True
				
		if(goldEU_local == False):
			if(random.uniform(0, 1) < 1-(1-goldChanceEU*(1 + goldTriggerAccumulated))**(1/20)):
				goldEU_tmp = True
				
		if(goldRestWorld5_local == False):
			i = 0
			for i in range (0,20 - goldRestWorld5_local):
				if(random.uniform(0, 1) < 1-(1-goldChanceRestWorld5*(1 + goldTriggerAccumulated))**(1/20)):
					goldRestWorld5_tmp += 1
					
		#production
		goldAboveGround_local += goldInflationBase
		if(goldOpec_local):
			goldAboveGround_local += goldInflationOPEC
		if(goldOpecPlus_local):
			goldAboveGround_local += goldInflationOPECPlus
		if(goldBRICS_local):
			goldAboveGround_local += goldInflationBRICS
		if(goldUS_local):
			goldAboveGround_local += goldInflationUS
		if(goldEU_local):
			goldAboveGround_local += goldInflationEU
		if(goldRestWorld5_local):
			goldAboveGround_local += goldInflationRestWorld5 * goldRestWorld5_local
				
		if(goldOpec_tmp):
			goldOpec_tmp = False
			goldOpec_local = True
			goldTriggerAccumulated += goldTriggerOPEC
			goldActualOutput += goldInflationOPEC
			
		if(goldOpecPlus_tmp):
			goldOpecPlus_tmp = False
			goldOpecPlus_local = True
			goldTriggerAccumulated += goldTriggerOPECPlus
			goldActualOutput += goldInflationOPECPlus
			
		if(goldBRICS_tmp):
			goldBRICS_tmp = False
			goldBRICS_local = True
			goldTriggerAccumulated += goldTriggerBrics
			goldActualOutput += goldInflationBRICS
			
		if(goldUS_tmp):
			goldUS_tmp = False
			goldUS_local = True
			goldTriggerAccumulated += goldTriggerUS
			goldActualOutput += goldInflationUS
			totalGlobalAdoption += USEconomySize
			
		if(goldEU_tmp):
			goldEU_tmp = False
			goldEU_local = True
			goldTriggerAccumulated += goldTriggerEU
			goldActualOutput += goldInflationEU
			totalGlobalAdoption += EUEconomySize
			
		if(goldRestWorld5_tmp>0):			
			goldRestWorld5_local += goldRestWorld5_tmp
			goldTriggerAccumulated += goldTriggerRestWorld5 * goldRestWorld5_tmp
			goldActualOutput += goldInflationRestWorld5 * goldRestWorld5_tmp
			totalGlobalAdoption += ((1 - EUEconomySize - USEconomySize) / 20) * goldRestWorld5_tmp
			goldRestWorld5_tmp = 0	
			
		discRate.append(-0.5* (popGrowth[20] if year >= 20 else popGrowth[year]) + baseDisc)		
		
	discRate.reverse()
	XAUAmount = mEU * goldEU_local + mUS * goldUS_local + (m5 / 20) * goldRestWorld5_local 
	XAUVal = XAUAmount/(goldAboveGround_local * toneToToz)
	for i in range (0, len(discRate)):
		XAUVal = XAUVal / (1 + discRate[i])	
	return calcResult(XAUVal, len(discRate))

print("number of simulations (in hundreds)")
numSimulations = int(input()) * 100
simResults = []
while(len(simResults) < numSimulations):	
	simResults.append(simulateNext())
totalVal = 0
totalYears = 0
for i in range (0, len(simResults)):
	totalVal += simResults[i].amount
	totalYears += simResults[i].year
print("XAU: " + str(totalVal/len(simResults)) + " Years: " + str(totalYears/len(simResults)))
	


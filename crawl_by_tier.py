'''

crawl_by_tier.py
Yewon Kim
Last Modified: 1/3/2020
Get user information based on tier and its division.

'''

from riotwatcher import RiotWatcher, ApiError
import sys
import os
import time

# command format: python /PATH/TO/crawl_by_tier.py region

#my API
watcher = RiotWatcher('enter your Riots API here')

# region
my_region = str(sys.argv[1])

'''

get summonerID from each tier division and save it to file

'''
tier_list = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
division_list = ['IV', 'III', 'II', 'I']

for tier in tier_list:
	for division in division_list:
		print(tier + division)
		userIDs = []
		page = 1
		data = ['initialization']
		while True:
			try:
				data = watcher.league.entries(my_region, 'RANKED_SOLO_5x5', tier, division, page)
			except ApiError as err:
				if err.response.status_code == 429:
					print('Rate limited. Waiting to retry %d seconds...' % err.response.retry-after)
					wait(err.response.retry-after)
			else:
				if len(data) == 0:
					break
				print("page %d" % page)
				for u in data:
					userIDs.append(u['summonerName'])
				page += 1

		fName = tier + '_' + division + '.txt'
		save_path = "crawled/" + my_region
		if not os.path.isdir(save_path):
			os.makedirs(save_path)
		complete_name = os.path.join(save_path, fName)
		
		with open(complete_name, 'w') as f:
			for ID in userIDs:
				f.write("%s\n" % ID)
		f.close()


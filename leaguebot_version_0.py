from riotwatcher import RiotWatcher
from requests import HTTPError


watcher = RiotWatcher('RGAPI-e0710767-a042-4dec-af3a-70eaf3005765')
'''
my_region = 'na1'

me = watcher.summoner.by_name(my_region, 'joe joe joe joe')
print(me)

# all objects are returned (by default) as a dict
# lets see if i got diamond yet (i probably didnt)
my_ranked_stats = watcher.league.positions_by_summoner(my_region, me['id'])
print(my_ranked_stats)
'''

def get_summoner_rank(summoner_name, region):
	try:
	    summoner = watcher.summoner.by_name(region, summoner_name)
	    ranked_stats = watcher.league.positions_by_summoner(region, summoner['id'])
	    #print(ranked_stats)
	    if len(ranked_stats) == 0:
	    	return None
	    ranked_data = []
	    ranked_data.append(summoner['name'])
	    for queue in ranked_stats:
	    	if queue['queueType'] == 'RANKED_SOLO_5x5':
	    		ranked_data.append(queue['tier'])
	    		ranked_data.append(queue['rank'])
	    		ranked_data.append(queue['leaguePoints'])
	    return ranked_data	
	except HTTPError as err:
	    if err.response.status_code == 429:
	        print('We should retry in {} seconds.'.format(e.headers['Retry-After']))
	        print('this retry-after is handled by default by the RiotWatcher library')
	        print('future requests wait until the retry-after time passes')
	    elif err.response.status_code == 404:
	        print('Summoner with that ridiculous name not found.')
	    else:
	        raise
	return None
	

if __name__== "__main__":
	print(get_summoner_rank("Ooglyoogly", "na1"))




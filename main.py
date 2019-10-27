import requests
##############
# note: This repository is great and I recommend you if you want more data for analysis 
# https://github.com/CaliAlec/snap-map-private-api/
##############
RADIUS = "5000" # 5000 Meters ----> 5Km
def getEpoch(): # epoch == timestamp
	"""
	// Send POST requests to 'ms.sc-jpl.com' with '/web/getLatestTileSet' endpoint to get Unix timestamp (epoch) [Note: SnapchatAPI Depends on server-side time not client-side time]
	// Don't use 'str(int(time.time()))' !!
	POST https://ms.sc-jpl.com/web/getLatestTileSet HTTP/1.1
	Content-Type: application/json
	
	{}
	"""
	return requests.post('https://ms.sc-jpl.com/web/getLatestTileSet',headers={'Content-Type':'application/json'},data='{}').json()['tileSetInfos'][1]['id']['epoch']

def getSnaps(lat,lon):
	"""
	POST https://ms.sc-jpl.com/web/getPlaylist HTTP/1.1
	Content-Type: application/json
	
	{"requestGeoPoint":{"lat":LATITUDE,"lon":LONGITUDE},"tileSetId":{"flavor":"default","epoch":EPOCH,"type":1},"radiusMeters":RADIUS}
	"""
	Epoch = getEpoch()
	dataPost = '{"requestGeoPoint":{"lat":'+str(lat)+',"lon":'+str(lon)+'},"tileSetId":{"flavor":"default","epoch":'+Epoch+',"type":1},"radiusMeters":'+RADIUS+'}'
	responseSnaps = requests.post('https://ms.sc-jpl.com/web/getPlaylist',headers={'Content-Type':'application/json'},data=dataPost)
	totalSnaps = responseSnaps.json()['manifest']['totalCount']
	responseText = responseSnaps.text
	fileName = "S"+str(lat)+":"+str(lon)+"_"+Epoch+".txt" # File will be saved with snaps info
	file = open(fileName, 'a')
	file.write(responseText.encode('utf-8'))
	file.close()
	return "I found "+str(totalSnaps)+" Snaps in these coordinates ("+str(lat)+","+str(lon)+")\nyou will find the data saved in "+fileName+" for the purpose of analysis\n"
if __name__ == "__main__":
	Snaps = getSnaps('24.83893115615588','46.71576928913487')
	print(Snaps)

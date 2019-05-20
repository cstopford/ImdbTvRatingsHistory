import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from bs4 import BeautifulSoup

imdbID = 'tt0060028' # ST:TOS
imdbID = 'tt2357547' # Jessica Jones
imdbID = 'tt0944947' # Game of Thrones

# Find number of seasons:
seasonUrl = 'https://www.imdb.com/title/' + imdbID

seasonResponse = urllib.request.urlopen(seasonUrl)
seasonData = seasonResponse.read()      # a `bytes` object
seasonText = seasonData.decode('utf-8')

ssoup = BeautifulSoup(seasonText, 'html.parser')

ssection = ssoup.find('div', attrs={'class':'seasons-and-year-nav'})
nseasonsStr = ssection.text.replace('Seasons','').replace('Years','')
nseasonsStr = nseasonsStr.lstrip()
nseasonsStr = nseasonsStr[:nseasonsStr.find('\xa0')]

# Find season title
stitle = ssoup.find('title').text.replace(' - IMDb','')
print(stitle + ', ' + nseasonsStr + ' seasons')


# Get ratings:
ratings = []  
votes = []    

# Number the episodes so we can plot different colours etc
seriesNumber = []
episodeNumber = []
RunningEpisodeNumber = 0
FirstEpisodeOfSeries = 0
maxVotes = 0

# Create figure
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

for i in range(1, int(nseasonsStr)+1):
    FirstEpisodeOfSeries = -1

    print('  Season: ' + str(i))
    url = 'http://www.imdb.com/title/' + imdbID + '/episodes?season=' + str(i)
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8')

    soup = BeautifulSoup(text, 'html.parser')

    sections = soup.find_all('div', attrs={'class':'ipl-rating-star'})

    for section in sections:
        if len(section) == 7:
            # Running Episode Number
            RunningEpisodeNumber = RunningEpisodeNumber + 1
            
            # First episode of season
            if FirstEpisodeOfSeries < 0:
                FirstEpisodeOfSeries = RunningEpisodeNumber

            # Get episode rating
            valString = section.text.lstrip()
            rating = float(valString[:valString.find('\n')])
            ratings.append(rating)
            
            # Get episode number of votes
            vote = valString[valString.find('(') + 1 : valString.find(')')].replace(',','')
            votes.append(float(vote)) 
            if float(vote)>maxVotes:
                maxVotes=float(vote)   


    
    print('First episode number: '+ str(FirstEpisodeOfSeries))
    print('Running episode number: ' + str(RunningEpisodeNumber))
    print('Length of ratings: ' + str(len(ratings)))
    print(' ')
    # Plot
    x = range(FirstEpisodeOfSeries, len(ratings) + FirstEpisodeOfSeries)
    ax1.scatter(x, ratings)
    ax2.scatter(x, votes)
            
    # Reset episode stuff
    ratings.clear()
    votes.clear()



# Plot output        
x = range(0,len(ratings))
ax1.set_title(stitle)
ax1.set_ylabel('Rating')
ax1.set
ax1.set_ylim(0, 10)
ax1.grid()

ax2.set_ylim(0, maxVotes*1.2)
ax2.set_ylabel('# Votes')
ax2.grid()
plt.savefig(imdbID + '.png')
plt.show()


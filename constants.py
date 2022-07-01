import sys

sys.path.append("..")

# Cache
ALL_ENTRIES_UNFILTERED_CACHE_KEY = 'k:allEntriesUnfiltered'
ALL_ENTRIES_STARRED_CACHE_KEY = 'k:allEntriesStarred'
CURRENT_USER_CACHE_KEY = 'k:currentUser'

# Profile model
PERSONAL = 'Personal'
TRAVELOGUE = 'Travelogue'
COOKBOOK = 'Cookbook'
SPIRITUAL = 'Spiritual'
DAILY = 'Daily Log'
PURPOSE = (
    (PERSONAL, 'Personal'),
    (TRAVELOGUE, 'Travelogue'),
    (COOKBOOK, 'Cookbook'),
    (SPIRITUAL, "Spiritual"),
    (DAILY, 'Daily Log'),
)
NONE = 'None'
ACTION = 'Action'
COMEDY = 'Comedy'
DRAMA = 'Drama'
FANTASY = 'Fantasy'
HORROR = 'Horror'
MYSTERY = 'Mystery'
ROMANCE = 'Romance'
THRILLER = 'Thriller'
WESTERN = 'Musical'
MUSICAL = 'Musical'
MOVIE_GENRES = (
    (ACTION, 'Action'),
    (COMEDY, 'Comedy'),
    (DRAMA, 'Drama'),
    (FANTASY, 'Fantasy'),
    (HORROR, 'Horror'),
    (MYSTERY, 'Mystery'),
    (ROMANCE, 'Romance'),
    (THRILLER, 'Thriller'),
    (WESTERN, 'Western'),
    (MUSICAL, 'Musical'),
)
BLUES = 'Blues'
COUNTRY = 'Country'
CLASSICAL = 'Classical'
DANCE = 'Dance'
DRILL = 'Drill'
DNB = 'DnB'
DUBSTEP = 'Dubstep'
EDM = 'Electronic'
FOLK = 'Folk'
FUNK = 'Funk'
GARAGE = 'Garage'
INDIE = 'Indie'
HIPHOP = 'Hiphop'
HOUSE = 'House'
METAL = 'Metal'
JAZZ = 'Jazz'
KPOP = 'Kpop'
POP = 'Pop'
PUNK = 'Punk'
PSYCHEDELIC = 'Psychedelic'
RAP = 'Rap'
ROCK = 'Rock'
RNB = 'RnB'
REGGAE = 'Reggae'
SOUL = 'Soul'
MUSIC_GENRES = (
    (COUNTRY, 'Country'),
    (CLASSICAL, 'Classical'),
    (DANCE, 'Dance'),
    (BLUES, 'Blues'),
    (DRILL, 'Drill'),
    (DNB, 'DnB'),
    (DUBSTEP, 'Dubstep'),
    (EDM, 'Electronic'),
    (FOLK, 'Folk'),
    (FUNK, 'Funk'),
    (GARAGE, 'Garage'),
    (INDIE, 'Indie'),
    (HIPHOP, 'Hiphop'),
    (HOUSE, 'House'),
    (METAL, 'Metal'),
    (JAZZ, 'Jazz'),
    (KPOP, 'Kpop'),
    (POP, 'Pop'),
    (PUNK, 'Punk'),
    (PSYCHEDELIC, 'Psychedelic'),
    (RAP, 'Rap'),
    (ROCK, 'Rock'),
    (RNB, 'RnB'),
    (REGGAE, 'Reggae'),
    (SOUL, 'Soul'),
)

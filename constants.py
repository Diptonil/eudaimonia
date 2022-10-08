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
QUOTES = (
    '"People who wonder if the glass is half empty or full miss the point. The glass is refillable."',
    '"Smart people learn from everything and everyone, average people from their experiences, stupid people already have all the answers."',
    '"We need to accept that we won\'t always make the right decisions, that we\'ll screw up royally sometimes―understanding that failure is not the opposite of success, it\'s part of success."',
    '"Very often, a change of self is needed more than a change of scene."',
    '"Twenty years from now you\'ll be more disappointed by the things you did not do than the ones you did."',
    '"Take criticism seriously, but not personally. If there is truth or merit in the criticism, try to learn from it. Otherwise, let it roll right off you."',
    '"If you think you\'re too small to make a difference, try sleeping with a mosquito."',
    '"Remember, you\'ve been criticizing yourself for years and it hasn\'t worked. Try approving of yourself and see what happens."',
    '"When you find no solution to a problem, it is probably not one to be solved but rather a truth to be accepted."',
    '"It is impossible to live without failing at something, unless you live so cautiously that you might as well not have lived at all ―in which case, you fail by default."',
    '"The problem with being prepared for the worst, is that the best things in life become easier to ignore..."'
)
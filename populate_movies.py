import pandas as pd

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advcbv.settings')

import django
django.setup()

import csv
from basic_app.models import Movie, Genre
from django.utils import timezone
from datetime import datetime
#movies = pd.read_csv('/home/lester/Downloads/newlist4.csv')

# genres = ['Drama', 'Action', 'Crime', 'Adventure', 'Comedy', 'Sci-Fi',
#        'Mystery', 'Biography', 'Horror', 'Animation', 'Thriller', 'Family',
#        'Documentary', 'Romance', 'Short', 'Reality-TV', 'Western',
#        'Fantasy', 'News', 'History', 'Game-Show', 'Music', 'Musical',
#        'Talk-Show', 'Sport', 'War','爱情','战争','奇幻','犯罪','动作',
#        '惊悚','剧情','喜剧','恐怖','悬疑',
#        '科幻','西部','情色','舞台艺术','动画',
#        '历史','运动','传记',]

#reader = csv.reader('/home/lester/Downloads/newlist4.csv')

def populate():
    # for r in genres:
    #     genre = Genre.objects.get_or_create(name=r)



    # for row in reader:
    #
    #     print(len(row[1]))
    #
    #     mygenres = []
    #     for g in row[4]:
    #         mygenres.append(g)
    #     print(mygenres)
    #     movie = Movie.objects.get_or_create(title = row[1],
    #                                         year = row[2],
    #                                         rate = row[3],
    #                                         genres = mygenres,
    #                                         votes = row[5],
    #                                         runtime = row[6],
    #                                         desc = row[7],
    #                                         dateadded = timezone.now
    #                                         )


    import csv
    with open('/home/lester/Downloads/newlist4.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        mygenres = []
        for row in reader:
            mygenres = Genre.objects.get_or_create(name=row['genre'])

            print('-----------------------------'+mygenres[0].name)

            try:
                rdate = datetime.strptime(row['date'], "%Y-%m-%d").date()
                movie = Movie.objects.create(title = row['title'],
                                                        year = int(row['year']),
                                                        rate = float(row['rate']),
                                                        #votes = int(float(row['votes'])),
                                                        runtime = int(row['runtime'].lstrip().replace('分钟', '')),
                                                        date =rdate,
                                                        imgurl =row['img'],
                                                        downloadurl =row['downloadurl'],
                                                        language =row['language'],
                                                        country =row['country'],
                                                        desc =row['desc'],
                                                        #dateadded = timezone.now
                                                        )
                movie.genres.add(mygenres[0])
            except:
                pass


if __name__ == '__main__':
    print('populating script!')
    populate()
    print('populating compalete!')

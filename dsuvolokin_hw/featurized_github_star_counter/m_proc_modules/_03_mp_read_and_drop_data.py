from sqlalchemy import create_engine
from os import remove,path

def read_data():
    if path.isfile('github_stars.db'):
        engine = create_engine('sqlite:///github_stars.db')
        print("most famous repos and its' owners:")
        with engine.connect() as connection:
            result = connection.execute("select * from repo")
            for row in result:
                print("organization: ",row['org'],"|", "repo_id: ", row["repo_id"],"|","repo_name: ",row['name'],"|","stars_count: ", row['stars_count'])
        try:
            remove('github_stars.db')
        except Exception as e:
            print("database not dropped")
            print(e)
        else:
            print("-"*25,"\ndata dropped successfully\n"+"-"*25)
    else:
        print('database is absent')

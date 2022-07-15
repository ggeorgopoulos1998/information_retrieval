from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np

es = Elasticsearch([{'host':'localhost','port':9200}])

movie_input = input("Give a string to find a movie: ")
user_id_input = int(input("give me the id of the user : "))
res = es.search(index = 'movies',body = {'query': {'match':{'title': movie_input}}})

df_ratings = pd.read_csv('ratings.csv')
df_movies_score_pu = df_ratings.filter(['userId','movieId','rating'] , axis=1)
df_movies_avg_score = df_ratings.filter(['movieId','rating'] , axis=1)
df_movies_avg_score = df_movies_avg_score.groupby('movieId').mean()
df_movies_avg_score.rename(columns = {'rating' : 'Average Score'}, inplace = True)
df_movies_avg_score=df_movies_avg_score.reset_index()
df_es_score_data = pd.DataFrame(columns = ['movieId','title','genres','es_score'])

for i in range(len(res['hits']['hits'])):
     #create a temp df to store the values temporarily 
     temp_df = pd.DataFrame([ [ int(res['hits']['hits'][i]['_source']['movieId']), res['hits']['hits'][i]['_source']['title'], res['hits']['hits'][i]['_source']['genres'], res['hits']['hits'][i]['_score'] ] ], columns=['movieId', 'title', 'genres', 'es_score'])
     print(i+1,')',res['hits']['hits'][i]['_source']['title'],"Score: ",res['hits']['hits'][i]['_score'])
     #storing the data of the temp df to the the dataframe for the es_score
     df_es_score_data = df_es_score_data.append(temp_df, ignore_index = True)


#another one temp df that contains  the es_score and the avg score of its movie
df_another_temp = pd.merge(df_es_score_data,df_movies_avg_score,on='movieId',how='left') 

#creating the df that contains the sum of the es_score and the avg_score for its movie t
df_another_temp['es_score + avg_score'] = df_another_temp['es_score'] + df_another_temp['Average Score']

#getting all the movies that the user has seen 
x = df_movies_score_pu.loc[df_movies_score_pu['userId'] == user_id_input]
df = x[["movieId","rating"]]

#the temp final df that contains everything 
df_another_temp = df_another_temp.merge(df, on = 'movieId', how = 'left')

#df_another1_temp = pd.merge(df_another_temp,x,on='movieId',how='left') 
print("this df contains the sum of the columns es_score and Average score and the rating by the user : ")
df_another_temp['rating'] = df_another_temp['rating'].replace(np.nan, 0)
df_another_temp.to_csv(r'Path where you want to store the exported CSV file\File Name.csv', index = False)
df_another_temp['final_score'] = df_another_temp['es_score + avg_score'] + df_another_temp['rating']
print(df_another_temp)

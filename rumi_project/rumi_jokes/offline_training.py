
def train_offline():
    import mysql.connector
    from pymongo import MongoClient
    import pandas as pd

    mongo_client = MongoClient("db-mongo:27017")
    db = mongo_client.dbms
    conn = mysql.connector.connect(
      host="db-mysql",
      user="root",
      passwd="mysql",
      database="rumi"
    )
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recommendations WHERE expired = 0')
    query = db.Joke.find({}, {"content": 0})
    jokes_df = pd.DataFrame(list(query))
    jokes_df['winrate'] = 0
    for i in range(jokes_df.shape[0]):
        if jokes_df.at[i, 'views'] != 0:
            jokes_df.at[i, 'winrate'] = jokes_df.at[i, 'score']/jokes_df.at[i, 'views']
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()
    val = []
    for user in users:
        priority = 0
        df = jokes_df
        df = df.drop(df[df['author'] == user[0]].index)
        for i in range(5):
            target_index = df.views.idxmin(1)
            target_wr = df.at[target_index, 'winrate']
            first_joke = df.at[target_index, '_id']
            df = df.drop(target_index)
            wr_diff = df.winrate.sub(target_wr)
            second_index = wr_diff.idxmin(1)
            second_joke = df.at[second_index, '_id']
            df = df.drop(second_index)
            first_joke = str(first_joke)
            second_joke = str(second_joke)
            t = (user[0], first_joke, second_joke, priority)
            val.append(t)
            priority += 1
    sql = "INSERT INTO recommendations(user_id, joke_1, joke_2, priority) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
    mongo_client.close()
        

if __name__ == '__main__':
    train_offline()



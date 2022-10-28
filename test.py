# # app = Flask(__name__)
# # app.secret_key = 'dont tell anyone'
# # scheduler = BackgroundScheduler()
# # scheduler.start()

# # mysql = MySQL(app)
# # app.config['MYSQL_HOST'] = 'localhost'
# # app.config['MYSQL_USER'] = 'root'
# # app.config['MYSQL_PASSWORD'] = ''
# # app.config['MYSQL_DB'] = 'website'

# # def interval_task():
# #     with app.app_context():
# #         ct = datetime.datetime.now()
# #         cursor = mysql.connection.cursor()
# #         cursor.execute(''' INSERT INTO db_cache_statistic VALUES(%s,%s,%s,%s,%s,%s)''',(len(memory_cache),sys.getsizeof(memory_cache),requests[0],miss[0],hit[0],ct))
# #         mysql.connection.commit()
# #         cursor.close()

# # def delay_Mins():

# #     with app.app_context():
# #         # Changes[0] = len(memory_cache)
# #         # Changes[1] = sys.getsizeof(memory_cache)
# #         # Changes[2] = requests[0]

# #         cursor = mysql.connection.cursor()
# #         cursor.execute(''' Select AVG(No_of_items) AS average from db_cache_statistic ''')
# #         rows = cursor.fetchall()
# #         for i in rows:
# #             Changes[0] = i[0]

# #         cursor = mysql.connection.cursor()
# #         cursor.execute(''' Select AVG(TotalSize_of_items) AS average from db_cache_statistic ''')
# #         rows = cursor.fetchall()
# #         for i in rows:
# #             Changes[1] = i[0]

# #         cursor = mysql.connection.cursor()
# #         cursor.execute(''' Select AVG(No_of_requests ) AS average from db_cache_statistic ''')
# #         rows = cursor.fetchall()
# #         for i in rows:
# #             Changes[2] = i[0]

# #         cursor = mysql.connection.cursor()
# #         cursor.execute(''' Select AVG(Miss_rate) AS average from db_cache_statistic ''')
# #         rows = cursor.fetchall()
# #         for i in rows:
# #             Changes[3] = i[0]

# #         cursor.execute(''' Select AVG(Hit_rate) AS average from db_cache_statistic ''')
# #         rows = cursor.fetchall()
# #         for i in rows:
# #             Changes[4] = i[0]

# # scheduler.add_job(func=interval_task, trigger="interval", seconds=5)
# # scheduler.add_job(func=delay_Mins, trigger="interval", minutes=10)

# # LRU code
# # defining the table size
# # from pyparsing import LRUMemo


# table_size = 3
# reference_string = {1 : "sdvadsv", 2: "dssdf", 3:"dsvadv", 4:"dsvasvd", 1:"dvasv", 2:"sdv", 5:"sdv", 1:"sdv", 2:"dsv", 3:"sfv", 4:"sfv", 5:"fsv"}

# # # the list which stores the current pages in memory
# # # and where page replacement is executed.
# pages = {}

# faults = 0


# for page in reference_string:
#     x =  {k: v for k, v in sorted(pages.items(), key=lambda item: item[1])}

    
#     print(page)

#     if page in pages:
#         pages[page] = pages[page]+1

#     else:
#         if(len(pages) < table_size):
#             pages[page] = 1

#         else:
           
#             pages.popitem()
#             pages[page] = 1

#     faults += 1
#     print(pages)
# print("total page faults = ", faults)
# print(pages)





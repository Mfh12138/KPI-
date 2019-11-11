from dbprops import *
import pymysql
# 连接数据库，核心代码
def getConnection():
    conn = pymysql.Connection(host=HOST, port=PORT, db=DB, user=USER,
                              passwd=PASSWORD,charset=CHARSET)
    print('type:{}\tconn:{}'.format(type(conn), conn))
    return conn

# 通过用户名和密码返回查询到的用户值
def get_user(username, password):
    conn = getConnection()
    sql = """ select username,password from user 
              where username='%s' and password='%s' """ % (username, password)
    cl = conn.cursor()
    print(sql)
    count = cl.execute(sql)
    result = cl.fetchall()
    print("查询到记录数", type(count), count)
    cl.close()
    conn.close()
    return result

# 通过用户名查询用户
def getUserByName(username):
    conn = getConnection()
    sql = """select * from user 
             where username='%s' """ % username
    print(sql)
    cl = conn.cursor()
    count = cl.execute(sql)
    print(type(count), count)
    cl.close()
    conn.close()
    return count

# 插入用户值,用户名，密码
def insert_user(username, password):
    conn = getConnection()
    sql = """
             insert into user(username,password)
             values('%s','%s')
          """ % (username, password)
    cl = conn.cursor()
    result = cl.execute(sql)
    conn.commit()  # 将数据真正存入数据库
    print(type(result), result)
    cl.close()
    conn.close()
    return result

def get_year():
    conn = getConnection()
    sql = """select 建筑年代 from xiaoqu"""
    cl = conn.cursor()
    row_count = cl.execute(sql)
    print(row_count)
    rs = cl.fetchall()
    # print(type(rs), rs)
    # print(type(rs[1][0]), rs[1][0])
    result = []
    for year in rs:
        if year != '':
            # print(type(year[0]), year[0])
            result.append(year[0])
    return result

def getReliData():
    conn = getConnection()
    cl = conn.cursor()
    print(type(cl), cl)
    sql = """ select LNGQ, LATQ,房屋总数 from xiaoqu"""
    n = cl.execute(sql)
    print(n)
    result = cl.fetchall()
    # print("查询结果", type(result), result)
    sqlData = []
    # 经度：LNGQ， 纬度：LATQ
    # centerzuobiao = {
    #     'jingdu': result[20][0],
    #     'weidu': result[20][1]
    # }
    for weizhi in result:
        count = int(weizhi[2] / 30)
        jw = {}  # 每次需要新建一个字典才能生成不同的值
        jw["lng"] = weizhi[0]
        jw["lat"] = weizhi[1]
        jw["count"] = count
        sqlData.append(jw)
    return sqlData

def insert_year_count(yearAnay):
    conn = getConnection()
    cl = conn.cursor()
    select_sql = "select * from house_year_count"
    if cl.execute(select_sql) > 0:
        print("数据库中已有数据")
        # 更新数据库
        update_sql = """update house_year_count 
        set 90年代前=%d,90年代=%d,00年代=%d,10年代=%d
        where id=1""" % (yearAnay['90年代前'], yearAnay['90年代'], yearAnay['00年代'], yearAnay['10年代'])
        print(update_sql)
        rs = cl.execute(update_sql)
        conn.commit()
        cl.close()
        conn.close()
        return rs
    print("传送数据库测试", type(yearAnay['90年代前']), yearAnay['90年代前'])
    sql = """insert into house_year_count (90年代前, 90年代, 00年代,10年代) 
    values(%d,%d,%d,%d)""" % (yearAnay['90年代前'], yearAnay['90年代'], yearAnay['00年代'], yearAnay['10年代'])
    print(sql)
    rs = cl.execute(sql)
    print(type(rs), rs)
    conn.commit()
    return rs

def get_year_count():
    conn = getConnection()
    cl = conn.cursor()
    sql = """select * from house_year_count"""
    count = cl.execute(sql)
    result = cl.fetchall()
    print(type(list(result[0])), list(result[0][1:]))
    return list(result[0][1:])








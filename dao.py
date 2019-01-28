# -*- coding:utf8 -*-
'''数据库操作方法'''

import MySQLdb
from log import logger
import conf


class UseData(object):
    def __init__(self):
        self.connection = lambda: MySQLdb.connect(host=conf.MYSQL_HOST, user=conf.MYSQL_USER, passwd=conf.MYSQL_PASSWORD, db=conf.MYSQL_DB)
        self.hasTable()

    def hasTable(self):
        '''判断是否含有指定表,如果没有就创建'''
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'CREATE TABLE IF NOT EXISTS {0}(id INT NOT NULL AUTO_INCREMENT,srcIp VARCHAR(100) NOT NULL,dstIp VARCHAR(100) NOT NULL,sport INT NOT NULL,dport INT NOT NULL,count int NOT NULL,PRIMARY KEY ( id ))'.format(
                conf.MYSQL_TABLE)
            cursor.execute(sql)
        except Exception as e:
            logger.error("数据库表 %s 创建失败", conf.MYSQL_TABLE)
            print(e)
        finally:
            cursor.close()
            connection.close()

    '''
    @description: 批量插入
    @param {tuple} 表头 srcIp, dstIp, sport,dport,count
    @param {list} 表值 [(),()]
    '''

    def insert(self, values):
        '''批量插入'''
        try:
            logger.error("数据库表 %s 数据插入", conf.MYSQL_TABLE)
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'INSERT INTO {0} (srcIp, dstIp, sport,dport,count) VALUES '.format(
                conf.MYSQL_TABLE)
            length = len(values)
            for i in range(length):
                string = '%s;' if i == length - 1 else '%s,'
                sql += string % str(values[i])
            cursor.execute(sql)
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            logger.error("数据库表 %s 批量插入失败，错误信息：%s", conf.MYSQL_TABLE, e)
        finally:
            cursor.close()
            connection.close()

    '''
    @description: 清空表
    '''

    def clearTable(self):
        try:
            logger.error("数据库表 %s 清空", conf.MYSQL_TABLE)
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'truncate table %s' % conf.MYSQL_TABLE
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            connection.rollback()
            logger.error("数据库表 %s 清空失败，错误信息：", conf.MYSQL_TABLE, e)
        finally:
            cursor.close()
            connection.close()


dataBase = UseData()
# m.insert([('Name 1', 'Value 1', 22, 4, 5), ('Name 2', 'Value 2', 22, 5, 8),
#           ('Name 3', 'Value 3', 33, 6, 9), ('Name 4', 'Value 4', 44, 7, 0)])
# m.clearTable()

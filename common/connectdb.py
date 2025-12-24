import pymysql
import redis
from rediscluster import  RedisCluster
from common.recordlog import logs
from conf.operateconf import OperateConf


class ConnectMysql:
    """
    连接mysql数据库
    """
    def __init__(self):
        self.conf = OperateConf()
        mysql_conf={
            "host": self.conf.get_mysql('host'),
            "port": int(self.conf.get_mysql('port')),
            "user": self.conf.get_mysql('username'),
            "password": self.conf.get_mysql('password'),
            "database": self.conf.get_mysql('database'),
        }
        # 连接数据库
        self.conn=pymysql.connect(**mysql_conf,charset='utf8')
        # 创建游标, 操作数据库
        self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        logs.info("""连接数据库成功
        host:{host}
        port:{port}
        db:{database}
        """.format(**mysql_conf))

    def close(self):
        if self.cursor and self.conn:
            self.cursor.close()
            self.conn.close()

    def query(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            logs.error(e)
        finally:
            self.close()


    def execute(self,sql):
        """
        mysql增删改语句
        :param sql:
        :return:
        """
        try:
            execute = self.cursor.execute(sql)
            self.conn.commit()
            return execute
        except Exception as e:
            logs.error(e)
            self.conn.rollback()
        finally:
            self.close()


class ConnectRedis:
    """
    连接redis数据库
    """
    def __init__(self):
        self.conf = OperateConf()
        self.redis_conf={
            "host": self.conf.get_redis('host'),
            "port": int(self.conf.get_redis('port')),
            "db": int(self.conf.get_redis('db'))
        }
        # 集群
        self.nodes_list=[]
        redis_nodes_str = self.conf.get_redis('startup_nodes')
        if redis_nodes_str:
            nodes_str_split = redis_nodes_str.split(',')
            for node_str in nodes_str_split:
                host,port=node_str.split(':')
                dict_data={'host':host,'port':port}
                self.nodes_list.append(dict_data)
            #startup_nodes 集群格式：[{'host': '192.168.1.1', 'port': 6379}, {'host': '192.168.1.2', 'port': 6379}]
            self.redis_cluster = RedisCluster(startup_nodes=self.nodes_list)
            logs.info(f"连接到redis集群服务，host：{redis_nodes_str}")
        else:
            # 单机
            # 创建数据库连接
            pool = redis.ConnectionPool(**self.redis_conf)
            self.redis_cluster = redis.Redis(connection_pool=pool)
            logs.info(f"连接redis服务器：ip:{self.redis_conf['host']}，port:{self.redis_conf['port']}")




    def redis_except(self,e):
        if "MOVED" in str(e):
            logs.error("MOVED错误")
        else:
            logs.error("error")

    def get(self,key):
        try:
            value= self.redis_cluster.get(key)
            if isinstance(value,bytes):
                return value.decode('utf-8')
            return value
        except Exception as e:
            self.redis_except(e)

    def set(self,key,value,ex=None):
        try:
            return self.redis_cluster.set(key,value,ex)
        except Exception as e:
            self.redis_except(e)


if __name__ == '__main__':
    connect_redis = ConnectRedis()



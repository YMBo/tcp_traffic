# tcp_traffic
python抓包解析并存储，流量分析

# tcp_traffic
python抓包解析并存储，流量分析

## install
pip install -r requirements.txt
sudo python getTraffic

## 说明
此工具是pypcap抓包，通过dpkt解包获得想要的数据，这里主要针对的是TCP的包，可以在conf.py设定存储间隔，每隔一段时间存储到Mysql(先清空，再存储)

## 目录结构
>├── README.md
├── conf.py&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;//配置文件
├── dao.py	&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;//数据库操作					
├── getTraffic.py &ensp;&ensp;&ensp;//抓包程序
├── log.py	&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;							//日志程序
└── requirements.txt	&ensp;&ensp;&ensp;&ensp;&ensp;//依赖包

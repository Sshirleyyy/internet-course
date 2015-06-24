# internet-course
Internet course at UrFU

[![Code Climate](https://codeclimate.com/github/slogger/internet-course/badges/gpa.svg)](https://codeclimate.com/github/slogger/internet-course)

[Описание задач](http://anytask.urgu.org/course/38)

## sntp
Для запуска сервера, требуется `python 3.4` или выше

Запускаем сервер, по умолчанию на `5000` порту
```
python3 sntp-server.py [--delay смещение]
```

и просим клиента сходить к нам
```
python3 sntp-client.py -s localhost:5000
```

## tracert
Утилита показывая `traceroute` до какого нибудь хоста, по пути определяя номер автономной системы и страну маршрутизатора
```
sudo python3 tracert-as.py ya.ru
```

## portscan
Уилита умеющая в TCP сканирование портов
```
python3 127.0.0.1 -tp all -m 5
```

```
usage: portscan.py [-h] [-a] [-t] [-p PORTS] [-m MULTITHREADING] target

portscan.py

positional arguments:
  target                The target(s) you want to scan (192.168.0.1)

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Enable this for full output
  -t, --tcpscan         Enable this for TCP scans
  -p PORTS, --ports PORTS
                        The ports you want to scan (21,22,80,24-42)
  -m MULTITHREADING, --multithreading MULTITHREADING
                        Thread count
```

## dns
Кэширующий DNS сервер
```
sudo python3 dns_server.py 8.8.4.4

```

## vk-api
Утилита выгружающая все фотографии из какого либо альбома пользователя vk.com в максимальном качестве

## pop
```
./main -h
Usage of ./main:
  -login="example@mail.ru": is a pop server
  -pass="pass": is a password
  -port="995": is a port
  -server="pop.mail.ru": is a pop server

example:
./main -login=pi201-2015@mail.ru -pass=2015pi201
```

## smtp
```
usage: smtp.py [-h] [--server SERVER] [--port PORT] [--username USERNAME]
               [--subject SUBJECT] [--text TEXT] [--path PATH]
               login password receiver

DNS server

positional arguments:
  login                 Sender email addres (login)
  password              Password
  receiver              Receiver email addres

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER       smtp server
  --port PORT           Port
  --username USERNAME   Username for EHLO
  --subject SUBJECT, -s SUBJECT
                        Message subject
  --text TEXT, -t TEXT  Message text
  --path PATH, -p PATH  Path for attachment

example:
python3 smtp.py pi201-2015@mail.ru 2015pi201 slogger1994@gmail.com --server smtp.mail.ru --port 465 -s "Hello world" -t "Hey, Slogger" -p pic
```

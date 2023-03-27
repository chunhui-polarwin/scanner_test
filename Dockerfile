FROM python:3.8

ENV TZ Asia/Shanghai

WORKDIR /root

COPY ./conf.ini /root
COPY ./main.py /root
COPY ./server.py /root

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/

RUN pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

CMD ["/usr/local/bin/python", "main.py"]

EXPOSE 8008
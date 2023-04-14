FROM selenium/standalone-chrome

# 安装pip
RUN apt-get update
RUN apt-get -y install python3-pip
# 修改pip镜像源
RUN pip config set global.trusted-host mirrors.aliyun.com
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/

COPY . /geo

WORKDIR /geo

RUN pip install -r /geo/requirements.txt

ENTRYPOINT ['python3', '/geo/main.py']
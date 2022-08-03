FROM tiagopeixoto/graph-tool:latest

RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

COPY ./cfg /cfg
RUN pip install -r /cfg/requirements.txt

COPY ./src /src
WORKDIR /src

CMD python test.py

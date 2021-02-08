FROM python:3.6
COPY . /IoT_Project
RUN pip3 install -r /IoT_Project/requirements.txt
RUN cd /IoT_Project/src/Testy/ && python3 ./unit_test.py
RUN cd /IoT_Project/src/Testy/ && python3 ./unit_test_backend_heat.py
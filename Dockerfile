FROM python:3.6
COPY . /IoT_Project
RUN pip3 install -r /IoT_Project/requirements.txt 
RUN python3 /IoT_Project/src/Testy/unit_test.py
RUN python3 /IoT_Project/src/Testy/unit_test_backend_heat.py
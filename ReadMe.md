## Uruchamianie Dockera
sudo docker run -it -v <ścieżka do repo>:/IoT_Project python:3.6 bash




mongo:

sudo apt purge mongodb-org*
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt update
sudo apt-get install -y mongodb-org

sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongodb


sprawdzenie kontenerów
sudo docker ps

uruchomienie dockera z konkretnego kontenera
sudo docker start 2f16b84c6b3e

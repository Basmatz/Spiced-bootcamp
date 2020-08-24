sudo apt-get install openjdk-8-jdk -y
wget https://downloads.metabase.com/v0.36.4/metabase.jar
sudo nohup java -jar -DMB_JETTY_PORT=80 metabase.jar &


# get metabase jar file from web
wget https://downloads.metabase.com/v0.35.3/metabase.jar

# install software
sudo yum install java-1.8.0
#sudo yum install python3
#sudo yum install git
#sudo pip3 install pandas

sudo nohup java -jar -DMB_JETTY_PORT=80 metabase.jar &

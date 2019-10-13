
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak

#ubuntu=trusty
ubuntu=xenial
boost_ver=1.55
boost_ver=

echo -e "deb http://mirrors.aliyun.com/ubuntu/ $ubuntu main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ $ubuntu-security main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ $ubuntu-updates main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ $ubuntu-proposed main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse \n" \
>> /etc/apt/sources.list

sudo rm -rf /etc/apt/sources.list.d/*.list

sudo apt-get -y update

sudo apt-get install -y build-essential dos2unix cmake git libboost$boost_ver-all-dev

git config --global user.email "leochan007@github.com"
git config --global user.name "leochan007"

sudo cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime

sudo chown $user:$user /home/$user -R

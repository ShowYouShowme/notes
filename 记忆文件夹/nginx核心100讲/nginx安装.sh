wget http://nginx.org/download/nginx-1.16.1.tar.gz
tar -zxvf nginx-1.16.1.tar.gz
cd ./nginx-1.16.1

# nginx配置文件在VIM中高亮
mkdir ~/.vim/
cp -r ./contrib/vim/* ~/.vim/

yum install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel -y


./configure --prefix=/usr/local/nginx/

make -j4


make install
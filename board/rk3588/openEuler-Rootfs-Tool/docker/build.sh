cp -r ../libs libs
cp -r ../include include

docker build -t rknn:v1 .

rm -rf libs include


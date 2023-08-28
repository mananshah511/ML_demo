# ML_demo
This is basic repo to understand GIT command and CI/CD.

creating conda environment
...
conda create -p venv python==3.7 -y
...
conda activate venv/
...

To add files to git 
...
git add .
OR 
git add filename

To check all versions
...
git log

To solve error of task running 
...
rm -f .git/index.lock

To make the commit 
...
git commit -m "messeages"

To send changes to git 
...
git push origin main

To check remote url
...
git remote -v

Docker build
...
docker build -t ml-project:latest .

To list docker images
...
docker images

Run docker image
...
docker run -p 5000:5000 -e PORT=5000 imageid

running docker images
...
docker ps

stop docker images
...
docker stop c_id
 
to stop docker container


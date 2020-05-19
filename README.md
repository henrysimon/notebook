# notebook
this are the files needed to run jupyter notebook docker container  
put this files in /application (linux vm / or if you in windows you can remap the folder in docker-compose.yml)  
###sample volumes in docker-compose.yml in Project/simon/docker-compose.yml  
    volumes:  
      - '/application/Project/simon/files:/home/jovyan/files'  
      - '/application/Project/simon/config:/home/jovyan/config'  

and download docker jupyter notebook by running this command (assuming you already have docker installed on the vm)  
$ docker pull henrysimon/testing:notebook  
and run by using (if using linux, if using windows just point to the yml that you change the folder above)  
$ docker-compose -f /application/Project/simon/docker-compose.yml up -d  
  
and you can browse the jupyter by opening browser (no password needed)  
http://localhost:8888  

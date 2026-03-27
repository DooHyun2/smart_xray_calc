This application is a specialized calculator designed to optimize "X-ray exposure time" for experimental setups.

industrial RT sites (using X-ray, Ir-192, Co-60) and laboratory X-ray transmission experiments


2026/03/16 Update: Added X-ray Tube Mode (mA/kV)

No installation required


http://52.62.146.78:8501 (PC, Mobile)

Latest Version

[![Open App](https://img.shields.io/badge/Open_App-Smart_X--ray_Calculator-blue?style=for-the-badge&logo=streamlit)](http://52.62.146.78:8501) << click (PC, Mobile) 

[![Docker Pulls](https://img.shields.io/docker/pulls/doohyun2/smart-xray-calc)](https://hub.docker.com/r/doohyun2/smart-xray-calc)  << click

previous

[![Docker Pulls](https://img.shields.io/docker/pulls/doohyun2/smart_xray_calc)](https://hub.docker.com/r/doohyun2/smart_xray_calc)



<img width="812" height="565" alt="image" src="https://github.com/user-attachments/assets/62ce871f-7049-4246-bd9f-fd12cd65ede4" />


<img width="772" height="759" alt="image" src="https://github.com/user-attachments/assets/9a2cb391-c2cc-441e-af64-8c3760567512" />





How to run 


[![Open App](https://img.shields.io/badge/Open_App-Smart_X--ray_Calculator-blue?style=for-the-badge&logo=streamlit)](http://52.62.146.78:8501) << click 

http://52.62.146.78:8501  (PC,Mobile)


-docker pull-
sudo docker pull doohyun2/smart-xray-calc:latest


-Quick Start (Docker Hub)-


Linux :    sudo docker run -d -p 8501:8501 --name xray-final doohyun2/smart-xray-calc

MacOS :  sudo docker run -d -p 8501:8501 --name xray-final doohyun2/smart-xray-calc

Window:      docker run -d -p 8501:8501 --name xray-final doohyun2/smart-xray-calc





run and click >> 
[![Localhost Connect](https://img.shields.io/badge/Local-App_Connect-8501?style=for-the-badge&logo=docker&logoColor=white&color=0db7ed)](http://localhost:8501)




-docker build start-

docker build -t smart-xray-calc .

docker run -p 8501:8501 smart-xray-calc 














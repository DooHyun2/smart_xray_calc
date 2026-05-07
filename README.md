This application is a specialized calculator designed to optimize "X-ray exposure time" for experimental setups.

industrial RT sites (using X-ray, Ir-192, Co-60) and laboratory X-ray transmission experiments


2026/03/16 Update: Added X-ray Tube Mode (mA/kV)




[https://doohyun-xray.streamlit.app/](https://doohyun-xray.streamlit.app/) (PC, Mobile)

Latest Version


[![Docker Pulls](https://img.shields.io/docker/pulls/doohyun2/smart-xray-calc)](https://hub.docker.com/r/doohyun2/smart-xray-calc) 

[![Docker Pulls](https://img.shields.io/docker/pulls/doohyun2/smart_xray_calc)](https://hub.docker.com/r/doohyun2/smart_xray_calc)

previous

[https://doohyun-xray.streamlit.app/](https://doohyun-xray.streamlit.app/) 



<img width="870" height="776" alt="image" src="https://github.com/user-attachments/assets/dd141cf1-a900-473a-9085-4ae7695c1fb8" />


<img width="790" height="730" alt="image" src="https://github.com/user-attachments/assets/22815ec2-8396-4479-a989-baf887bc1ded" />










How to run 



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














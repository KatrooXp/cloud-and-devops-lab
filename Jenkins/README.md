## Jenkins task

### 1.1 Set Static node

- run EC2 instance on AWS cloud installed jdk-11

- configured credentials on master
![Alt text](<pics/Screenshot from 2023-10-06 13-16-15.png>)

- configured static node on master
![Alt text](<pics/Screenshot from 2023-10-06 13-17-04.png>)

- connected to static node
![Alt text](<pics/Screenshot from 2023-10-06 13-24-18.png>)

### 1.2 Set dynamic node

- configure Docker host machine: install Docker, open port 4243 for Jenkins master, configure Docker host with remote API

![Alt text](<pics/Screenshot from 2023-10-10 16-46-14.png>)
![Alt text](<pics/Screenshot from 2023-10-10 16-45-19.png>)

- add and configure cloud in Jenkins
![Alt text](<pics/Screenshot from 2023-10-10 16-49-37.png>)
![Alt text](<pics/Screenshot from 2023-10-10 16-50-04.png>)

- run test pipeline

![Alt text](<pics/Screenshot from 2023-10-10 16-47-51.png>)

![Alt text](<pics/Screenshot from 2023-10-10 16-38-02.png>)
![Alt text](<pics/Screenshot from 2023-10-10 16-39-05.png>)
 
### 2. Configure credentials

![Alt text](<pics/Screenshot from 2023-10-09 13-18-28.png>)

Example of configuring ssh credentials for Git Hub:

- generate ssh keys as jenkins user

![Alt text](<pics/Screenshot from 2023-10-09 13-20-36.png>)

- deploy keys on GitHub repository (copy the id_rsa.pub)

![Alt text](<pics/Screenshot from 2023-10-09 13-22-31.png>)

- authentificate wiht GitHub using known_host strategy

![Alt text](<pics/Screenshot from 2023-10-09 13-23-58.png>)

- configure credentials in Jenkins using id_rsa private key

![Alt text](<pics/Screenshot from 2023-10-09 13-29-29.png>)

### 3. Налаштування прав доступу. Створити три групи (dev, qa, devops та надати різні права доступу)
![Alt text](<pics/Screenshot from 2023-10-11 10-10-40.png>)
![Alt text](<pics/Screenshot from 2023-10-11 10-21-33.png>)
![Alt text](<pics/Screenshot from 2023-10-11 10-22-24.png>)

## Multibranch pipeline

- Multibranch pipeline configuration in Jenkins

![Alt text](<pics/Screenshot from 2023-10-13 14-42-12.png>)
![Alt text](<pics/Screenshot from 2023-10-13 12-56-48.png>)
![Alt text](<pics/Screenshot from 2023-10-13 12-57-14.png>)

- GitHook to trigger Jenkins

![Alt text](<pics/Screenshot from 2023-10-12 09-53-03.png>)

- pipeline for each brand

![Alt text](<pics/Screenshot from 2023-10-13 13-08-50.png>)

- Jenkinsfile configuration

![Alt text](<pics/Screenshot from 2023-10-23 20-25-26.png>)

- Pipeline result

![Alt text](<pics/Screenshot from 2023-10-23 20-14-13.png>)
![Alt text](<pics/Screenshot from 2023-10-23 20-14-52.png>)

![Alt text](<pics/Screenshot from 2023-10-23 21-51-19.png>)

## CI pipeline

- Pipeline configuration in Jenkins

![Alt text](<pics/Screenshot from 2023-10-13 16-50-11.png>)
![Alt text](<pics/Screenshot from 2023-10-13 16-50-54.png>)

- GitHook to trigger Jenkins

![Alt text](<pics/Screenshot from 2023-10-13 16-42-24.png>)

- Test the maven project pipeline

![Alt text](<pics/Screenshot from 2023-10-17 14-16-23.png>)
![Alt text](<pics/Screenshot from 2023-10-17 14-16-54.png>)

- Configure SonarQube with docker container

source used: https://medium.com/@nanditasahu031/jenkins-pipeline-with-maven-sonarqube-and-talisman-fa9118910b98

docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest

    create a project
![Alt text](<pics/Screenshot from 2023-10-17 12-39-43.png>)
![Alt text](<pics/Screenshot from 2023-10-17 14-21-45.png>)
![Alt text](<pics/Screenshot from 2023-10-17 14-22-35.png>)

    generate tocken
![Alt text](<pics/Screenshot from 2023-10-17 14-23-18.png>)

    copy the provided code to Jenkinsfile
![Alt text](<pics/Screenshot from 2023-10-17 14-28-22.png>)

    install Sonar scaner plugin and configure
![Alt text](<pics/Screenshot from 2023-10-17 14-32-23.png>)  
![Alt text](<pics/Screenshot from 2023-10-17 15-11-29.png>)  
![Alt text](<pics/Screenshot from 2023-10-17 15-33-23.png>)
![Alt text](<pics/Screenshot from 2023-10-17 15-35-11.png>)

    add Sonar Qube analysys stage to Jenkinsfile
![Alt text](<pics/Screenshot from 2023-10-17 15-59-47.png>)

    test the pipeline
![Alt text](<pics/Screenshot from 2023-10-17 15-54-05.png>)
![Alt text](<pics/Screenshot from 2023-10-17 15-54-31.png>)

    get Dockerhub credentials and add to Jenkins and Jenkinsfile
![Alt text](<pics/Screenshot from 2023-10-19 11-35-53.png>)
![Alt text](<pics/Screenshot from 2023-10-19 11-37-59.png>)
![Alt text](<pics/Screenshot from 2023-10-19 11-40-05.png>)

    add Docker build, login, push stages to Jenkinsfile
![Alt text](<pics/Screenshot from 2023-10-19 11-41-49.png>)

    final pipeline test
![Alt text](<pics/Screenshot from 2023-10-19 11-13-29.png>)

    Dockerhub repository
![Alt text](<pics/Screenshot from 2023-10-19 11-43-17.png>)

## CD pipeline

    configure Jenkins pipeline
![Alt text](<pics/Screenshot from 2023-10-23 14-43-09.png>)
![Alt text](<pics/Screenshot from 2023-10-19 13-16-04.png>)

    jenkinsfile
![Alt text](<pics/Screenshot from 2023-10-23 14-45-12.png>)

    pipeline test
![Alt text](<pics/Screenshot from 2023-10-23 14-54-47.png>)
![Alt text](<pics/Screenshot from 2023-10-23 14-56-46.png>)

    enable teams notifications
![Alt text](<pics/Screenshot from 2023-10-23 15-18-53.png>)
![Alt text](<pics/Screenshot from 2023-10-23 15-17-45.png>)
![Alt text](<pics/Screenshot from 2023-10-23 15-23-00.png>)
![Alt text](<pics/Screenshot from 2023-10-23 15-24-11.png>)















## Jenkins pipeline

<b>Task</b>: Need to create a pipeline with Jenkins, where after we pushes code to github and start build in jenkins, Jenkins will checkout the updated code, build and push the image and lastly update and apply the latest manifest file into minikube.

---
<h3>Expected Flow</h3>
Code → Build image → Push → Update image → Deploy to K8s

<br/>

---
<h3>What i have done to achieve this?</h3>
Installed necessary tools like jenkins, docker, minikube. Gave jenkins the necessary permission to use docker and kubectl. Created the jobs with Jenkinsfile And execute the job.

---
<h3>Possible improvments</h3>
 - Add webhook or polling to detect changes automatically
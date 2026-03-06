#this code  is for load balancing using nft-tables

##features 
-nftables resides inside the kernel which makes it possible for low latency and resource load balancing.
-it uses hashing for the purpose of session affinity.
-traffic is managed using between the public ip and private backend servers using linux commands only.

#prerequisites
. linux kernel with nftables
.Docker for hosting backend servers

##How it works
-This project is designed with security as a priority,to ensure that IP are not exposed.
-.gitignore file is used to automatically prevent sensitive locally.
-local motivation: the build.sh script is configured to be ignored by Git.
-The prerouting hook catches incoming TCP traffics on port 80
-the jhash map distributes incoming traffic, based on source ip while preserving session affinity
-the destination address is rewritten to the selected backend servers(docker containers)


##Usage
-spin up the backends by creating  two docker containers
-Apply the rules using   nft -f "filename.nft"
-Spin a web server using python3 -m http.server 8080 on a separate terminal.
-test using curl host-ip:80


##Troubleshooting
connection refused: usually due to nothing listening on a port

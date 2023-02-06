import requests
import argparse

pUser = '54da973e-10f8-454f-8577-cb99e606ebeb'
pPass = 'BE+s8ijq/q3kg+aFzfsDdkjPOuA='
pVersion = 'v22.01'
cAddr = "australia-southeast1.cloud.twistlock.com"

# http://192.168.137.120:8080 proxy
    
def parseArgs():
    parser = argparse.ArgumentParser(description='Parse site name to other function')
    parser.add_argument('-c', '--cluster', action="store", dest="clusterName", help="specify cluster name", required=True)
    parser.add_argument('-p', '--proxy', action="store", dest="proxy", help="specify proxy")
    parser.add_argument('-o', '--orchestration', action="store", dest="orchestration", help="specify orchestration")
    parser.add_argument('-lk', '--labelkey', action="store", dest="labelkey", help="specify keys of labels")
    parser.add_argument('-lv', '--labelvalue', action="store", dest="labelvalue", help="specify value of labels")
    return parser.parse_args()


class prismaGet():    
    def __init__(self):
        self.user = pUser
        self.pswd = pPass
        self.token = None
        self.base_url = f'https://australia-southeast1.cloud.twistlock.com/anz-3053678/api/{pVersion}/'
        self.consoleAddress = cAddr
        self.clusterName = args.clusterName
        self.proxy = args.proxy
        # self.orchestration = None
        self.orchestration = args.orchestration
        self.labelkey = args.labelkey
        self.labelvalue = args.labelvalue
        self.cri = False
            
    def Orchestration(self):
        
        choice = {"1" : "kubernetes" , "2" : "openshift"}
        select = input(f"select choice number {choice} : ")
        if choice[f"{select}"] == "kubernetes" :
            print(choice[f"{select}"])
            self.orchestration = choice[f"{select}"]
        elif choice[f"{select}"] == "openshift" :
            print(choice[f"{select}"])
            self.orchestration = choice[f"{select}"]
        if self.orchestration == 'openshift':
            self.cri = True
        return self.orchestration,self.cri
    
    def auth(self):
        headers = {"Content-Type": "application/json"}
        cred = {'username': self.user, 'password': self.pswd}
        r = requests.post(f"{self.base_url}authenticate", headers=headers, json=cred)
        res = r.json()
        self.token = res['token']
        return self.token
    
    def genyaml(self):
        # print(self.orchestration)
        if self.orchestration == 'openshift':
            self.cri = True
        if self.labelkey is None: 
            label = ""
        if self.labelkey:
            label = f"{self.labelkey}: {self.labelvalue}"
        print(self.cri)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        payload = {
                    "cluster": self.clusterName,
                    "collectPodLabels": True,
                    "consoleAddr": self.consoleAddress,
                    # "credentialID": "string",
                    "cri": self.cri,
                    # "dockerSocketPath": "/var/run/docker.sock",
                    # "gkeAutopilot": True,
                    # "image": "string",
                    # "istio": True,
                    "namespace": "twistlock-nforce",
                    "nodeSelector": label,
                    "orchestration": self.orchestration,
                    "privileged": False,
                    # "projectID": "string",
                    "proxy": {
                        "ca": "",
                        "httpProxy": self.proxy,
                        "noProxy": "",
                        "password": "",
                        "user": ""
                    },
                    # "region": "string",
                    # "secretsname": "string",
                    "selinux": True,
                    "serviceaccounts": True,
                    "uniqueHostname": True
                    }
        r = requests.post(f"{self.base_url}defenders/daemonset.yaml", headers=headers, json=payload)
        print(r.status_code)
        # datayaml = yaml.dump(r.text)
        daemonset_file = (f"daemonset-{self.clusterName}.yaml")
        headerline ='''apiVersion: project.openshift.io/v1
kind: Project
metadata:
  name: twistlock-nforce

---'''
        with open(daemonset_file, mode="w", newline="", encoding='utf-8') as data:
            data.write(headerline)
            data.write(r.text)
            
if __name__ == "__main__":
    args = parseArgs()
    pg = prismaGet()
    # pg.Orchestration()
    pg.auth()
    pg.genyaml()

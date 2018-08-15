class OSDPClass:

    def __init__(self):
        self.current_directory = os.getcwd()
        self.final_directory = os.path.join(self.current_directory, r"osdp/configuration")
        self.directory = 'osdp'
        self.my_file = Path(r"osdp/keys/private.bin")
        self.secret_code = ''
        self.encoded_key = ''
        self.linux = ['ubuntu', 'centos', 'debian', 'amazon', 'dcos-vagrant', 'xenial', 'docker', 'amazonlinux', 'docker-lambda']
        self.logger = setup_logging()
        self.REMOTE_SERVER = "www.github.com"
    def init(self):
        if is_connected(self.REMOTE_SERVER):
            try:
                if not os.path.exists(self.final_directory):
                    os.makedirs(self.final_directory)
                Repo.clone_from('https://github.com/james-knott/configuration.git', self.final_directory , branch="master", progress=MyProgressPrinter())
                self.logger.info("Downloaded the settings.yml file. Go to osdp/configuration/settings.yml to customize your environment!")
            except git.exc.GitCommandError as e:
                self.logger.info("Could not clone the repo. Folder may exist.!")
                if os.path.isfile('osdp/configuration/settings.yml'):
                    self.logger.info("Found the settings.yml file. It has already been downloaded!")
                else:
                    self.logger.info("Could not connect to Github to download the settings.yml file. Creating Dynamically!")
                    inp = """\
                    # Open Source Development Platform
                    osdp:
                      # details
                      linux: amazon   # So we can develop AWS Lambda with same python version
                      username: jknott
                      project: company
                      platform: docker # Currently supported docker and vagrant
                      runtime: python3.6
                      dockerhubusername: buildmystartup
                      dockerhubpassword: mypassword
                      imagename: buildmystartup/ghettolabs
                      pushto: ghettolabs/python
                      dockerdeveloperimage: buildmystartup/ghettolabs:python3.6
                    """
                    yaml = YAML()
                    code = yaml.load(inp)
                    #yaml.dump(code, sys.stdout) test what they dynamic file looks like
                    self.logger("Your new projecct name is", code['osdp']['project'])
                    if not os.path.exists(self.final_directory):
                        os.makedirs(self.final_directory)
                    with open('osdp/configuration/settings.yml', "w") as f:
                        yaml.dump(code, f)
        else:
            print("Network connection is down")

    def new(self):
        dataMap = self.get_settings()
        current_directory = os.getcwd()
        data_folder = Path("osdp")
        if dataMap['osdp']['platform'] == 'vagrant':
            file_to_open = data_folder / "projects" / dataMap['osdp']['project'] / "vagrant"
            final_directory = os.path.join(current_directory, file_to_open)
        elif dataMap['osdp']['platform'] == 'docker':
            file_to_open = data_folder / "projects" / dataMap['osdp']['project'] / "docker"
            final_directory = os.path.join(current_directory, file_to_open)
        if os.path.exists(final_directory):
            self.logger.info("A project with that name already exists!")
            self.backup()
            try:
                shutil.rmtree(final_directory, onerror=onerror)
                self.logger.info("The folder has been removed.!")
            except:
                self.logger.info("The folder could  not be removed.!")
        else:
            os.makedirs(final_directory)
        if dataMap['osdp']['linux'] not in self.linux:
            self.logger.info("The linux distro you selected is not supported yet!")
            self.logger.info("Go back into the settings.yml file and assign the linux key: ubuntu, centos, amazon, debian, dcos-vagrant !")
            sys.exit(1)
        url = "https://github.com/james-knott/" + dataMap['osdp']['linux'] + ".git"
        self.logger.info("Downloading project files!")
        Repo.clone_from(url, final_directory , branch="master")
        if dataMap['osdp']['platform'] == 'docker':
            IMG_SRC = dataMap['osdp']['dockerdeveloperimage']
            client = docker.Client()
            client.login(username=dataMap['osdp']['dockerhubusername'], password=dataMap['osdp']['dockerhubpassword'], registry="https://index.docker.io/v1/")
            client.pull(IMG_SRC)
            client.tag(image=dataMap['osdp']['dockerdeveloperimage'], repository=dataMap['osdp']['pushto'],tag=dataMap['osdp']['runtime'])



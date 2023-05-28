# This installation script is based of LInstall by @Heizkoerper (https://github.com/Heizkoerper/LInstall)

import os

# List of distros and package managers as tuples
distro_package_manager = [
    ("Ubuntu", "sudo apt-get install -y"),
    ("Debian", "sudo apt-get install -y"),
    ("Fedora", "sudo dnf install -y"),
    ("CentOS", "sudo yum install -y"),
    ("Arch", "sudo pacman -S --noconfirm"),
    ("Gentoo", "sudo emerge"),
    ("OpenSUSE", "sudo zypper install -y"),
    ("Red Hat Enterprise Linux", "sudo yum install -y"),
    ("Alpine", "sudo apk add"),
    ("Slackware", "sudo slackpkg install"),
    ("FreeBSD", "sudo pkg install -y"),
    ("NetBSD", "sudo pkgin -y install"),
    ("OpenBSD", "sudo pkg_add -I"),
    ("Mageia", "sudo urpmi --auto --no-verify-rpm"),
    ("Mandriva", "sudo urpmi --auto --no-verify-rpm"),
    ("Mint", "sudo apt-get install -y"),
    ("Oracle Linux", "sudo yum install -y"),
    ("PCLinuxOS", "sudo apt-get install -y"),
    ("Raspbian", "sudo apt-get install -y"),
    ("Scientific Linux", "sudo yum install -y"),
    ("SUSE Linux Enterprise", "sudo zypper install -y"),
    ("Xubuntu", "sudo apt-get install -y"),
    ("Zorin OS", "sudo apt-get install -y"),
    ("Kali", "sudo apt-get install -y"),
    ("Manjaro", "sudo pacman -S --noconfirm"),
    ("Parrot", "sudo apt-get install -y"),
    ("Solus", "sudo eopkg install -y"),
    ("EndeavourOS", "sudo pacman -S --noconfirm"),
    ("Pop!_OS", "sudo apt-get install -y"),
    ("MX Linux", "sudo apt-get install -y")
]



# Return the distro name
def get_distro():
    return os.popen("cat /etc/*-release | grep ^NAME | cut -d '=' -f 2").read()



# Return the package manager for the distro, if the distro is not supported return None
def get_package_manager(distro):

    for distro_name, package_manager in distro_package_manager:
        if distro_name in distro:
            return package_manager
    
    return None



# Return the requirements from requirements.txt as a list
def get_requirements():

    try:
        with open("requirements.txt", "r") as f:
            requirements = []
            for line in f:
                if not line.startswith('//'):
                    requirements.append(line.strip())

    except FileNotFoundError:
        exit("requirements.txt file could not found")
    

    return requirements



def install_requirements():

    distro = get_distro()
    package_manager = get_package_manager(distro)
    requirements = " ".join(get_requirements())

    # Check if the requirements are empty
    if requirements == "":
        exit("requirements.txt is empty")
    
    # Check with user that the distro was recognized correctly
    if str(input(f"Your distro is {distro.strip()}, is that correct? (y/n): ")).lower() != "y":
        exit("Automatic installation aborted by the user. Distro not recognized correctly.")

    # Check if the distro is represented in the list of distros and package managers
    if package_manager is None:
        exit("Your distro is not supported")

    # Ask the user if he wants to install the requirements
    print(f"The following requirements will be installed: {requirements.lstrip().replace(' ', ', ')}")
    if str(input("Do you want to install the requirements? (y/n): ")).lower() != "y":
        exit("Automatic installation aborted by the user")

    # Install the requirements
    os.system(f"{package_manager}{get_requirements()}")

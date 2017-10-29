import os, sys, shutil, subprocess, time

version = "0.1"
installName = 'Hover Practice'

# target is where we assemble our final install.
if os.path.isdir('target/'):
    shutil.rmtree('target/')
time.sleep(0.3)    
installDir = 'target/' + installName + '/'
os.mkdir('target/')
#os.mkdir(installDir)

os.chdir("src_bootstrapper")
subprocess.call("cxfreeze.py bootstrapper.py --base-name=Win32GUI --target-dir dist --icon ../boots.ico", shell=True, stdout=sys.stdout, stderr=sys.stderr)
os.chdir("..")

shutil.move('src_bootstrapper/dist/bootstrapper.exe', 'src_bootstrapper/dist/Hover Practice.exe') # Move the dist files to our target directory
shutil.move('src_bootstrapper/dist/', installDir)


os.chdir("src")
subprocess.call("cxfreeze.py hoverpractice.py --base-name=Win32GUI --target-dir dist --icon ../boots.ico", shell=True, stdout=sys.stdout, stderr=sys.stderr)
os.chdir("..")

shutil.copy('boots.png', 'src/dist/boots.png')
shutil.move('src/dist/', installDir + 'hover-lib/')

shutil.copy('LICENSE.txt', installDir)
shutil.copy('README.md', installDir + 'README.txt')
shutil.make_archive("target/" + installName + "-" + version, "zip", 'target', installName + "/")
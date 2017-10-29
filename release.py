import os, sys, shutil, subprocess

version = "0.1"
installName = 'Hover Practice'

# target is where we assemble our final install.
if os.path.isdir('target/'):
    shutil.rmtree('target/')
installDir = 'target/' + installName + '/'
os.mkdir('target/')
#os.mkdir(installDir)

os.chdir("src_bootstrapper")
subprocess.call("cxfreeze.py bootstrapper.py --base-name=Win32GUI --target-dir dist", shell=True, stdout=sys.stdout, stderr=sys.stderr)
os.chdir("..")

shutil.move('src_bootstrapper/dist/bootstrapper.exe', 'src_bootstrapper/dist/Hover Practice.exe') # Move the dist files to our target directory
shutil.move('src_bootstrapper/dist/', installDir)



subprocess.call("cxfreeze.py hoverpractice.py --base-name=Win32GUI --target-dir dist", shell=True, stdout=sys.stdout, stderr=sys.stderr)
shutil.copy('boots.png', 'dist/boots.png')
shutil.move('dist/', installDir + 'hover-lib/')

shutil.copy('LICENSE.txt', installDir)
shutil.copy('README.md', installDir + 'README.txt')
shutil.make_archive("target/" + installName + "-" + version, "zip", 'target', installName + "/")
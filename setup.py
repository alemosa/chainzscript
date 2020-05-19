from distutils.core import setup 
import py2exe 
 
setup(name="ChainZScript", 
 version="1.0", 
 description="ChainZ Script for getting data and logos of chainz", 
 author="Aleix Morte", 
 author_email="alemosa94@gmail.com", 
 url="smartdexsolutions.com", 
 license="Licencia privada", 
 scripts=["chainzscript.py"], 
 console=["chainzscript.py"], 
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None)
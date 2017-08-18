Here are some helpful hints for future maintainers of the JLab build of gemcWeb.

The directory structure is as follows:

```
$PROJ_DIR = /group/clas/www/gemc2017/html/gemcWeb

$CODE_DIR = /group/clas/www/gemc2017/html/gemcWeb/gemcWeb

/$PROJ_DIR
  -salt.txt
  /opt/jlab_software
  /users
  /components
  /upload
  /$CODE_DIR
    /static
    /templates
    -gemc.py
    -scripts.py
    -jlab-gemc.wsgi
```

To restart server:

```
sudo systemctl restart webserver
```

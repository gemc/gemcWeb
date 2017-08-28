Here are some helpful hints for future maintainers of the JLab build of gemcWeb.

To restart server:

```
sudo systemctl restart webserver
```

To use external git repos, launch bash and whitelist the following proxies by running:

```
export https_proxy=jprox.jlab.org:8081
export http_proxy=jprox.jlab.org:8081
```

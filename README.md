# Hosted AFL

**Name of project has yet to be determined...**

Web service that runs [AFL](http://lcamtuf.coredump.cx/afl/) on your projects. Built with Docker running on Kubernetes.

## Planning

### Stage 1

* Basic auth, probably using Mozilla Persona
* Run AFL on Rust programs for 10 minutes
* Rust programs will be submitted via crate name from crates.io index.
* Receive inputs that crash file, or indication that no crashes found`

### Stage 2

* Trigger builds upon pushes to GitHub
* Better statistics about AFL while it's running

### Stage N

* Go support
* Python support
* Longer than 10 minutes processes (paid?)

# Item Catalog
___
## Introduction
Item Catalog is a website that allows users to add, delete, and edit items in a database. Item Catalog enforces authentication for CRUD operations, and allows only the items owners to modify or delete items.

## Installation
Item Catalog is designed to run in a virtualbox. To install Item Catalog, please first install these dependencies.
#### Dependency Setup
First, you must have virtualbox installed. If you do not, you can download the version for your operating system [here](https://www.virtualbox.org/wiki/Downloads). 
Next, you must have vagrant installed. You can get that [here](https://www.vagrantup.com/downloads.html).
#### Item Catalog Installation
*These directions are for UNIX-like systems such as Linux and macOS*
1. Navigate to a directory where you want to save the source code
2. Clone this repository with:
   ```
   $ git clone https://github.com/jamesmanone/item-catalog.git
   ```
3. Create the guest system with:
   ```
   $ vagrant up
   ```
   This will create, provision, and setup the system. This will also handle database setup. Please be patient, this can take some time.
#### Run
From the installation directory, you can start the server with the following:
```
$ vagrant ssh
$ /vagrant/app.py
```
Now open a browser and navigate to [localhost:8000/](localhost:8000/)

**Enjoy!**

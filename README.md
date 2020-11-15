# Modules

## Installation

To install these modules run the following command:

~~~bash
git clone https://github.com/Pippo98/ownModules.git
cd ownModules
~~~

Then to install globally simply run:

~~~bash
./sync.sh
~~~

Now the modules are copied in ***/usr/lib/python3/dist-packages/***

If some of these modules are modified, to make the changes global rerun *sync.sh*


>If *./sync.sh* raise errors follow these steps:
>~~~bash
>python3
>~~~
>Next import sys module and print the environment path:
>~~~python
>import sys
>print(sys.path)
>~~~
>The printed list contains all the current paths that python use to >find modules, find a similar path to the one above, replace it in the >***sync.sh** script and rerun it.
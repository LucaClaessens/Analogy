

##Analogy: Platform-minded Publishing.

While Amazon has been claiming that the book is not dead, one would have some doubts saying the same about the publishing industry.

A paradigm shift is taking place and many, if not most publishers are struggling with the harsh reality of losing sovereignty. Is it still possible to run a sustainable business as an old school publisher? If so, for how long? Generally, publishers point fingers at the current winners in the information business: Google, Facebook, Spotify & co.

Although their complaints might be justified, we at Analogy believe that the problem also lies in the fact that most publishing enterprises stick to the old way of doing business. Writer’s write books, an editorial team does the editorial work, and an incredibly complex distribution chain sucks most of the revenue out of the final product.

When we created Analogy within the [PublishingLab](http://www.publishinglab.nl) incubator, we decided to look past this old regime of doing business and aim our energy at creating a more efficient and sustainable production model. We analyzed the strategies of the winners and extracted business concepts from their money making systems.

---

+ [Content creation](#user-content-content-creation)
+ [Production](#user-content-production) 
+ [Printing](#user-content-printing) 

# Content creation

## Installation

## System setup
You'll need to install the header files for Python 2.7 and the HDF5 library. On Ubuntu you should be able to install
like this:

```bash
sudo apt-get -y install python2.7-dev
sudo apt-get install libhdf5-dev
```

## Python setup
The preprocessing script is written in Python 2.7; its dependencies are in the file `preprocess_requirements.txt`.
You can install these dependencies in a virtual environment like this:

```bash
virtualenv .env                  # Create the virtual environment
source .env/bin/activate         # Activate the virtual environment
pip install -r preprocess_requirements.txt  # Install Python dependencies
# Work for a while ...
deactivate                       # Exit the virtual environment
```

## Lua setup
The main modeling code is written in Lua using [torch](http://torch.ch); you can find installation instructions
[here](http://torch.ch/docs/getting-started.html#_). You'll need the following Lua packages:

- [torch/torch7](https://github.com/torch/torch7)
- [torch/nn](https://github.com/torch/nn)
- [torch/optim](https://github.com/torch/optim)
- [lua-cjson](https://luarocks.org/modules/luarocks/lua-cjson)
- [torch-hdf5](https://github.com/deepmind/torch-hdf5)

After installing torch, you can install / update these packages by running the following:

```bash
# Install most things using luarocks
luarocks install torch
luarocks install nn
luarocks install optim
luarocks install lua-cjson

# We need to install torch-hdf5 from GitHub
git clone https://github.com/deepmind/torch-hdf5
cd torch-hdf5
luarocks make hdf5-0-0.rockspec
```

### CUDA support (Optional)
To enable GPU acceleration with CUDA, you'll need to install CUDA 6.5 or higher and the following Lua packages:
- [torch/cutorch](https://github.com/torch/cutorch)
- [torch/cunn](https://github.com/torch/cunn)

You can install / update them by running:

```bash
luarocks install cutorch
luarocks install cunn
```

## OpenCL support (Optional)
To enable GPU acceleration with OpenCL, you'll need to install the following Lua packages:
- [cltorch](https://github.com/hughperkins/cltorch)
- [clnn](https://github.com/hughperkins/clnn)

You can install / update them by running:

```bash
luarocks install cltorch
luarocks install clnn
```

## OSX Installation
Jeff Thompson has written a very detailed installation guide for OSX that you [can find here](http://www.jeffreythompson.org/blog/2016/03/25/torch-rnn-mac-install/).


Any RNN backend can be used, but with the relative speed and low memory footprint we've decided to with with **torch-rnn** over other character based RNN's.

after installing the frameworks needed to get your network up and running, you are almost ready to start running your network.
Before we can start generating content though, we need a place for the information to flow.

To train a model and use it to generate new text, you'll need to follow three steps.

## Step 1: Preprocess the data

Whilst you can use any text file for training models, Analogy ships with a pdf to text translation module, store the pdf files you want to use for your dataset in `text-processing-tools/data`; when you are happy with the content you've gathered, navigate to the `Analogy_App` folder and run the preprocessor script like this:

```bash
python Analogy.py pdfconvert
```

This will produce files `analogy.h5` and `analogy.json` in the `text-processing-tools` folder, you can move these to `Network/data`  to be picked up by the training script.

## Step 2: Train the model
After preprocessing the data, you'll need to train the model. This will be the slowest step. While training, move the the `Network` directory.

You can run the training script like this:

```bash
th train.lua
```


This will read the data stored in `analogy.h5` and `analogy.json`, run for a while, and save checkpoints to files with 
names like `checkpoints/analogy_cp_1000.t7`.

You can change the RNN model type, hidden state size, and number of RNN layers like this (from the `Network` directory):

```bash
th train.lua -input_h5 my_data.h5 -input_json my_data.json -model_type rnn -num_layers 3 -rnn_size 256
```

By default this will run in GPU mode using OpenCL; to run in CPU-only mode, add the flag `-gpu -1`.

To run with CUDA, add the flag `-gpu_backend cuda`.

## Step 3: Sample from the model
After training a model, you can generate new text.
if you don't want to tweak any settings, you can go to the `Network` directory of the project and run:

```bash
python model_to_DB.py --cycles 10
```

This will load the latest trained checkpoint from the previous step, sample it,
and print the results to the previously configured database.

Within the `model_to_DB.py` file, you can change the mySQL database you're connecting to, as well as the backend you're running the network on.

the `-c` flag controls how many cycles you will run, every cycle outputs 1 result to the database, during every cycle the script will send a random set of values together with a warmup sentence from  `primetext.txt` to the network, in an attempt to generate new text.

## Production

Since our interfaces are web based we decided to go with a simple MySQL database, in phpMyAdmin you can run the `create_analogy_database.sql` file, this should set up the database for you (empty). If you wish to prepopulate the database with some of our testing data, run `populate_analogy_database.sql`instead. 

To set up the production side of things, you can move the `web-tools` folder into your hosting environment. Once this is done, navigate to the `Network` folder and open the  `initialize_servers.py` file, please note that Analogy is preconfigured to run with MAMP, so if you're using another hosting environment please disable the `RUN_MAMP` flag. 

Set the `HOST_NAME` and `PORT_NUMBER` variables to your needs (note this file sets up a simple python webserver, so if you run things over the internet, move this file over to your server).

To set up the right database connections, please set up proper credentials in the `connect.php` file, located in `web-tools/Editing/php` if you're planning on using the network outside of a local environment. The file is preconfigured with a standard MAMP setup. (root/root)

on a local setup,it's now as simple as running:

```bash
python Analogy.py setup
```

on a remote setup you will have to activate the listening httpserver manually by running the `initialize_servers.py` file.

after setting up the servers, you can simply visit the address from any device and start editing away, all the edits will be captured in the database.

the editing pages will be located in `editing/selection.html` and `editing/image_selection.html`, from a MAMP perspective this would translate to http://localhost:8888/Analogy/web-tools/editing/selection.html

##Printing

once past a certain treshold of edits, you're ready to start printing, navigate to the `Printer` folder and run

```bash
python main_content_controller.py
```

Analogy is designed to work with a [Tiny Thermal Receipt Printer - TTL Serial / USB](https://www.adafruit.com/products/2751), you can interface with the printer either over a microcontroller such as a Raspberry Pi (even arduino, but you will have to port the controller code to arduino yourself, the C++ Adafruit_Thermal library can be found [here](https://github.com/adafruit/Adafruit-Thermal-Printer-Library)).

You can also control it straight from your computer after installing the PL2303 USB drivers:

[MacOSX 10.9 to 10.11](https://cdn-shop.adafruit.com/product-files/954/PL2303_MacOSX_1_6_0_20151022.zip) ,
[Windows XP/Vista/7/8](https://cdn-shop.adafruit.com/product-files/954/PL2303_Prolific_DriverInstaller_v1_12_0.zip)

depending on the way you're interfacing with the printer you want to comment/uncomment the right connection type in the header of the `main_content_controller.py` file.


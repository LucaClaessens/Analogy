

##Analogy: Platform-minded Publishing.

While Amazon has been claiming that the book is not dead, one would have some doubts saying the same about the publishing industry.

A paradigm shift is taking place and many, if not most publishers are struggling with the harsh reality of losing sovereignty. Is it still possible to run a sustainable business as an old school publisher? If so, for how long? Generally, publishers point fingers at the current winners in the information business: Google, Facebook, Spotify & co.

Although their complaints might be justified, we at Analogy believe that the problem also lies in the fact that most publishing enterprises stick to the old way of doing business. Writer’s write books, an editorial team does the editorial work, and an incredibly complex distribution chain sucks most of the revenue out of the final product.

When we created Analogy within the [PublishingLab](http://www.publishinglab.nl) incubator, we decided to look past this old regime of doing business and aim our energy at creating a more efficient and sustainable production model. We analyzed the strategies of the winners and extracted business concepts from their money making systems.

---

+ [Installation](#user-content-installation)
+ [Content creation](#user-content-content-creation)
+ [Production](#user-content-production) 
+ [Printing](#user-content-printing) 

# Installation

## Database setup

Since our interfaces are web based we decided to go with a simple MySQL database, Analogy is preconfigured to work with MAMP in a local environment, but if you want to run externally that's also possible.

For now, go to your preferred hosting environment and run the `create_analogy_database.sql` file in phpMyAdmin, this will set up the database for you (empty). If you wish to prepopulate the database with some of our testing data, run `populate_analogy_database.sql`instead.

Configuration of all variables can be done in the `analogy_config.ini` file, here you can also change your mySQL settings.

## System setup

#### OSX Installation
Jeff Thompson has written a very detailed installation guide for OSX that you [can find here](http://www.jeffreythompson.org/blog/2016/03/25/torch-rnn-mac-install/).

#### Ubuntu Installation
You'll need to install the header files for Python 2.7 and the HDF5 library. On Ubuntu you should be able to install
like this:

```bash
sudo apt-get -y install python2.7-dev
sudo apt-get install libhdf5-dev
```

## Python setup
The processing scripts are written in Python 2.7; it's dependencies are in the file `preprocess_requirements.txt`.
You can install these dependencies in a virtual environment like this:

```bash
virtualenv .env                  # Create the virtual environment
source .env/bin/activate         # Activate the virtual environment
pip install -r preprocess_requirements.txt  # Install Python dependencies
# Work for a while ...
deactivate                       # Exit the virtual environment
```

some packages will have to be installed ov

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


Any RNN backend can be used, but with the relative speed and low memory footprint we've decided to with with **torch-rnn** over other character based RNN's.

after installing the frameworks needed to get your network up and running, you are almost ready to start running your network.
Before we can start generating content though, we need a place for the information to flow.

To train a model and use it to generate new text, you'll need to follow three steps.

# Content creation

## Step 1: Preprocess the data

Whilst you can use any text file for training models, Analogy ships with a pdf to text translation module, store the pdf files you want to use for your dataset in `text-processing-tools/data`; when you are happy with the content you've gathered, navigate to the `Analogy_App` folder and run the preprocessor script like this:

```bash
python Analogy.py pdfconvert
```

If you prefer to work with textfiles, please merge all your text into one file and from `text-processing-tools` run

```bash
python preprocess.py --input_txt textfile.txt
```

This will produce files `analogy.h5` and `analogy.json` in the `text-processing-tools` folder, you can move these to `Network/data`  to be picked up by the training script.

## Step 2: Train the model
After preprocessing the data, you'll need to train the model. This will be the slowest step. While training, move the the `Network` directory.

before training, we will have to set some configurations in the `analogy_config.ini` file again, please choose whether or not to run in gpu mode by setting `cpu_only` to either `True` or `False` and set your backend to either `opencl` or `cuda`.

Now, you can run the training script like this:

```bash
th train.lua
```


This will read the data stored in `analogy.h5` and `analogy.json`, run for a while, and save checkpoints to files with 
names like `checkpoints/analogy_cp_1000.t7`.

You can change the RNN model type, hidden state size, and number of RNN layers like this (from the `Network` directory):

```bash
th train.lua -input_h5 my_data.h5 -input_json my_data.json -model_type rnn -num_layers 3 -rnn_size 256
```

## Step 3: Sample from the model
After training a model, you can generate new text, at a set interval, your training script will tell you a new checkpoint has been created, with additional information on training&validation loss.

please choose one of the checkpoints stored in the `checkpoints` folder and set it's name to the `checkpoint` variable in `analogy_config.ini`, the network will now sample from this checkpoint.

if you don't want to tweak any settings, you can go to the `Network` directory of the project and run:

```bash
python model_to_DB.py
```

This will load the checkpoint from the previous step, sample it,
and print the results to the previously configured database.

By default, the network will run 15 cycles and output them to the database, but the amount of cycles you want to run can also be changed in the configuration file.

The  `sample_cycles` setting controls how many cycles you will run. Every cycle outputs 1 result to the database, during every cycle the script will send a random set of values together with a warmup sentence from  `primetext.txt` to the network, in an attempt to generate new text.

## Production

To set up the production side of things, you can move the `web-tools` folder into your hosting environment. Once this is done, navigate to the `Network` folder and open the  `initialize_servers.py` file, please note that Analogy is preconfigured to run with MAMP, so if you're using another hosting environment please disable the `RUN_MAMP` flag. 

Set the `HOST_NAME` and `PORT_NUMBER` variables to your needs (note this file sets up a simple python webserver, so if you run things over the internet, move this file over to your server).

To set up the right database connections, please set up proper credentials in the `connect.php` file, located in `web-tools/Editing/php` if you're planning on using the network outside of a local environment. The file is preconfigured with a standard MAMP setup. (root/root)

on a local setup,it's now as simple as running:

```bash
python Analogy.py setup
```

on a remote setup you will have to activate the listening httpserver manually by running the `initialize_servers.py` file.

after setting up the servers, you can simply visit the address from any device and start editing away, all the edits will be captured in the database.

the editing pages will be located in `editing/selection.html` and `editing/image_selection.html`.

##Printing

once past a certain treshold of edits, you're ready to start printing, navigate to the `Printer` folder and run

```bash
python main_content_controller.py
```

Analogy is designed to work with a [Tiny Thermal Receipt Printer - TTL Serial / USB](https://www.adafruit.com/products/2751), you can interface with the printer either over a microcontroller such as a Raspberry Pi (even arduino, but you will have to port the controller code to arduino yourself, the C++ Adafruit_Thermal library can be found [here](https://github.com/adafruit/Adafruit-Thermal-Printer-Library)).

You can also control it straight from your computer after installing the PL2303 USB drivers:

[MacOSX 10.9 to 10.11](https://cdn-shop.adafruit.com/product-files/954/PL2303_MacOSX_1_6_0_20151022.zip) ,
[Windows XP/Vista/7/8](https://cdn-shop.adafruit.com/product-files/954/PL2303_Prolific_DriverInstaller_v1_12_0.zip)

depending on the way you're interfacing with the printer you want to set the preferred connection type by changing `use_serial` to either one of the subsequent serials set in the `analogy_config.ini` file.


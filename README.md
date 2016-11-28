

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

We generate content by using [torch-rnn](https://github.com/jcjohnson/torch-rnn) as the backbone of our system. For a detailed guide on installation for Ubuntu, please consult their repository for now. 

Any RNN backend can be used, but with the relative speed and low memory footprint we've decided to with with **torch-rnn** over other character based RNN's.

Jeff Thompson has written a very detailed installation guide for OSX that you [can find here](http://www.jeffreythompson.org/blog/2016/03/25/torch-rnn-mac-install/).

after installing the frameworks needed to get your network up and running, you can start generating content. To train a model and use it to generate new text, you'll need to follow three steps.

**PLEASE NOTICE: Analogy is constructed to be used from a fairly low level of expertise, if you have advanced programming experience please use the scripts the `Analogy.py` script is referencing towards directly, as this will grant you a plethora of extra arguments you can control the modules with.**

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
th sample.lua -checkpoint cv/analogy_cp_10000.t7 -length 2000
```

This will read the data stored in `analogy.h5` and `analogy.json`, run for a while, and save checkpoints to files with 
names like `cv/analogy_cp_1000.t7`.

You can change the RNN model type, hidden state size, and number of RNN layers like this:

```bash
th train.lua -input_h5 my_data.h5 -input_json my_data.json -model_type rnn -num_layers 3 -rnn_size 256
```

By default this will run in GPU mode using OpenCL; to run in CPU-only mode, add the flag `-gpu -1`.

To run with CUDA, add the flag `-gpu_backend cuda`.

## Step 3: Sample from the model
After training a model, you can generate new text.

```bash
python Analogy.py generate
```

This will load the latest trained checkpoint from the previous step, sample it,
and print the results to the previously configured database.

**TODO: Make sure this part of the system becomes maluable.**

By default this will run in GPU mode using OpenCL; to run in CPU-only mode, add the flag `-gpu -1`.

To run with CUDA, add the flag `-gpu_backend cuda`.

## Production


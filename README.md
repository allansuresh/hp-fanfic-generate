
# Crossovers Using GPT-3

This is a project that uses a finetuned model of OpenAI's GPT-3 to generate user-defined crossover scripts between DC and Marvel.

The model was finetuned using film scripts from the MCU and DCEU, formatted in the form of JSONL {"prompt":"<prev_dialogue>\n<Speaker>:","completion":"dialogue"} pairs.  Owing to limited data, this finetuning was limited to main characters, so it will work best with those characters.  Skip [here](#run) to try it.

## Setup

Set up a Python virtual environment using the following command in the root directory:

Windows:

```shell
$ python -m venv venv
$ venv\Scripts\activate
```

Mac / Linux:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
```


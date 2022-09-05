# Developing a tool for fair and reproducible use of paid crowdsourcing in the digital humanities

This repository contains the code for the paper *Developing a tool for fair and reproducible use of paid crowdsourcing in the digital humanities*, to be presented at the 6th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature (LaTeCH-CLfL 2022). 

The code demonstrates how the tool described in the paper may be used to create crowdsourcing pipelines on the [Toloka](https://toloka.ai) platform.

## Prerequisites

To run the example code contained in this repository, you first need to install the tool described in the paper. 

The tool is available on [PyPI](https://pypi.org/project/abulafia/), and may be installed by running the command `pip install abulafia`.

We recommend installing the tool and its dependencies into [a virtual environment](https://docs.python.org/3/library/venv.html).

## Codebase

The directory [`config`](config) contains YAML configuration files for each crowdsourcing task and action in the crowdsourcing pipeline.

The directory [`data`](data) contains the input data as a TSV file.

The directory [`instructions`](instructions) contains instructions for the crowdsourcing tasks as an HTML file.

## Running the pipeline

To run the crowdsourcing pipeline, execute the file `run_pipeline.py` from the command line using the following command:

```python
python3 run_pipeline.py -c path_to_credentials.json
```

As instructed in the [tool repository](https://github.com/thiippal/abulafia), you need to store your Toloka credentials into a JSON file and provide this file as input to the script in `run_pipeline.py`.

We recommend executing the file in the Toloka sandbox by setting the value of the variable `mode` to `SANDBOX`.

You can then register on the Toloka sandbox as a performer to view and complete the tasks in the pipeline.

## Contact

If you have questions about the pipeline, feel free to open an issue in this repository, or contact us via e-mail. Our e-mail addresses can be found in the conference publication.
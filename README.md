# text_augmentation
Augmentator for text datasets

## Getting Started

### Prerequisites
You should have python3 installed on your machine (we recommend Anaconda3 package) and modules listed in requirements.txt. If you do not have them, run in Terminal
```
pip3 install -r requirements.txt
```
Installing and Usage
Linux / MacOS
To install this project on your local machine, you should run the following commands in Terminal:
```
cd YOUR_FOLDER
git init
git clone  https://github.com/nsu-ai/text_augmentation.git
```
The project is now in YOUR_FOLDER.

To use this project, run
```
cd augmentator
from augmentator import augmentator
```
### Examples of using Augmentator:
```
>>> YOUR_FOLDER python3 augmentator.py data.csv 3 new_data.csv  30
```
you will get new csv file with increased in 4 times amount of sentences and 30% of words changed in each sentence

Running the test
```
python3 test.py
```
## Contributing
...

## Authors

Anna Mosolova

Ivan Bondarenko

Vadim Fomin


See also the list of [contributors](https://github.com/nsu-ai/text_augmentation/contributors) who participated in this project.

## License
## Acknowledgments

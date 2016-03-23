# the_crawler
Facebook crawler to defend children from bullying

## How to update the classifier
* To add offensive posts create txt file and put it in offensive_data/neg
* To add positive (normal) posts create txt file and put it in offensive_data/pos

To Generate new classifier write:
cd ./Required

python train_classifier.py --algorithm NaiveBayes --instances files --fraction 0.99  --show-most-informative 10 --filename=offensive.pickle --labels 'pos','neg' --min_score 3 --filter-stopwords english ../offensive_data

cp ./offensive.pickle Classifier/classifer.pickle
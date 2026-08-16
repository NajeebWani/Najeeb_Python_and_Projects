# Wine Classification

Given the chemical analysis of a wine (alcohol %, acidity, magnesium, color
intensity, etc), predict which of 3 cultivars it's from. Small, clean
dataset - good one for practicing classification and comparing a couple of
different algorithms without getting bogged down in data cleaning.

## Dataset

sklearn's built-in wine dataset - 178 samples, 13 numeric features, 3
classes. This is a well known UCI dataset.

## What I did

1. Loaded the data, checked class balance (fairly balanced, 59/71/48).
2. Made a correlation heatmap to see which features move together
   (flavanoids and total_phenols are pretty correlated, for example).
3. Scaled features with StandardScaler - matters a lot here since things
   like `proline` are in the hundreds while `hue` is under 2.
4. Trained KNN and an SVM (RBF kernel), compared accuracy.
5. Ran 5-fold cross validation on the SVM to make sure the good result
   wasn't just a lucky train/test split.

## Results

- KNN: ~93% accuracy
- SVM: 100% on the test split, ~98% average across 5-fold CV

SVM does a bit better here, probably because the classes are pretty
well separated once you scale the features. Cross-val confirms it's not
just overfitting to one split.

## Files

- `wine.py` - the full script
- `images/correlations.png`, `images/confusion_matrix.png`

## Running it

```
pip install pandas scikit-learn matplotlib seaborn
python wine.py
```

## Notes / things to try

- With such high accuracy already, PCA to visualize the classes in 2D
  would be a nice addition
- Try a simpler baseline (logistic regression) to see how much the fancier
  models are actually buying you
- This dataset is small enough that results can shift a bit between runs -
  cross validation is worth trusting more than a single test split

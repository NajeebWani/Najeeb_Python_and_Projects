# Titanic Survival Prediction

Classic beginner ML project - using passenger data from the Titanic to predict
who survived and who didn't. I picked this one because it's a good way to
practice the full workflow: cleaning messy data, doing a bit of EDA, and then
comparing a couple of models.

## Dataset

Using the built-in Titanic dataset that comes with seaborn (891 passengers).
Columns include class, sex, age, fare, number of siblings/parents aboard, and
whether they survived.

## What I did

1. Loaded the data and checked for missing values - `age` had a lot of them
   (177 missing), `deck` was mostly empty so I just dropped it.
2. Filled missing ages with the median, filled the 2 missing `embarked`
   values with the most common port.
3. Converted `sex` to 0/1 and one-hot encoded `embarked`.
4. Made two new features: `family_size` (siblings + parents + self) and
   `is_alone` (whether they were traveling solo) - figured family size might
   matter more than raw sibsp/parch numbers.
5. Trained a Logistic Regression model and a Random Forest, compared accuracy.
6. Looked at feature importance to see what actually drove survival.

## Results

- Logistic Regression: ~80% accuracy
- Random Forest: ~83% accuracy

Not surprising given what we know about the Titanic - `sex` and `pclass` were
by far the biggest predictors of survival (women and 1st class passengers had
much higher survival rates). You can see this clearly in the bar charts.

## Files

- `titanic.py` - full script, run it top to bottom
- `images/` - the plots it generates (survival by class/sex, feature
  importance, confusion matrix)

## Running it

```
pip install pandas numpy seaborn matplotlib scikit-learn
python titanic.py
```

## Ideas for improvement

- Try extracting titles from passenger names (Mr/Mrs/Miss/Master) - this
  usually helps a bit
- Tune the Random Forest hyperparameters instead of using defaults
- Try XGBoost, it usually does a bit better on this dataset

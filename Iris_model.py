from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import time

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

start = time.time()

y = model.predict([[6.0, 2.2, 4.0, 1.0]])

print(y)

end = time.time()
print("Model training duration:", end - start, "seconds")

#joblib.dump(model, "iris_model.pkl")
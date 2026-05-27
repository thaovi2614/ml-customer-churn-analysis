import pickle

features = pickle.load(open("model/features.pkl", "rb"))

print("TONG SO FEATURE:", len(features))
print("\nDANH SACH FEATURE:\n")

for i, f in enumerate(features, 1):
    print(f"{i}. {f}")
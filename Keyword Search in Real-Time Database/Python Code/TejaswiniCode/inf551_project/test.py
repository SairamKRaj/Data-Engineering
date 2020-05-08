import pandas as pd
# dfSalary = pd.read_csv("C:\\Users\\Tejaswini\\Downloads\\status\\status.csv")
# dary = dfSalary.drop ( columns=["dat

xl = pd.ExcelFile("C:\\Users\\Tejaswini\\Downloads\\status\\status.csv")
df = xl.parse("Sheet1")
df = df.drop(3, axis=1)

print (df)
